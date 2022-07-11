import logging
import os
from select import select
from tkinter import *
from tkinter import messagebox
from typing import Callable
from poltergust.controllers.ctlist_controllers import CTListController
from poltergust.controllers.track_change import TrackChangeController
from poltergust.models.ct_storage import MK8CTStorage
from poltergust.parsers.downloader import MK8CustomTrack, ModDownloadException, PoltergustDownloader

from poltergust.models.gamedata import COURSE_IDS
from poltergust.models.game_models import MK8GhostType
from poltergust.parsers.filename_parser import MK8GhostFilenameData, MK8GhostFilenameParser, MK8GhostFilenameSerializer
from poltergust.parsers.ghost_converter import MK8GhostConverter
from poltergust.parsers.ghost_file_parser import MK8GhostDataParser
from poltergust.parsers.mii_handler import MK8GhostFilenameDataMiiHandler
from poltergust.views.change_track import PoltergustChangeTrackView
from poltergust.views.ct_add import PoltergustAddCTView
from poltergust.views.ct_list import PoltergustCTManagerView, TrackListSelectorView
from poltergust.views.main import PoltergustMainView


class PoltergustController:
    """ Controller for the application. It invokes models/parsers and controls the view/UI state """

    def __init__(self, view: PoltergustMainView):
        self.ghostfile: str = None
        self.filename_data: MK8GhostFilenameData = None
        self.ghost_has_header = None
        self._view = view
        self._db = MK8CTStorage()

        # Setup Menu callbacks
        self._view.menu_file.entryconfig(self._view.BTN_OPEN, command=self.open_ghostfile)
        self._view.menu_file.entryconfig(self._view.BTN_CLOSE, command=self.close_ghostfile)
        self._view.menu_file.entryconfig(self._view.BTN_RELOAD_FROM_DISK, command=self.update)

        # Setup Export callbacks
        self._view.menu_export.entryconfig(self._view.BTN_EXTRACT_MII, command=self.extract_mii)
        self._view.menu_export.entryconfig(self._view.BTN_EXPORT_AS_STAFF_GHOST, command=self.export_as_staff)
        for slot in range(16):
            self._view.menu_export_download.entryconfig(self._view.BTN_DOWNLOADED_GHOST_SLOT_PREFIX+str(slot), command=lambda bound_slot=slot: self.export_as_downloaded(bound_slot))

        # Setup Edit callbacks
        # self.view.menu_edit.entryconfig(self.view.BTN_REPLACE_MII, command=self.replace_mii)
        self._view.menu_edit.entryconfig(self._view.BTN_CHANGE_TRACK, command=self.change_ct)

        # CT Manager
        self._view.menubar.entryconfig(self._view.BTN_CT_MANAGER, command=self.open_ct_manager)

        self.close_ghostfile()

    def open_ghostfile(self, filename=None):
        """ Invokes the view to select a ghost file, and loads its data """
        if filename is None:
            filename = self._view.select_ghost_file()

        # Selection is empty if it was aborted
        if not filename:
            return

        logging.info(f"Opened ghost file: {filename}")

        self.ghostfile = filename
        self.filename_data = None
        self.update()

    def close_ghostfile(self):
        """ Closes the currently loaded ghostfile, and cleans up its data """
        # Discard filename_data
        self.ghostfile = None
        self.filename_data = None
        self.ghost_has_header = None

        # Disable buttons
        self._view.menu_file.entryconfig(self._view.BTN_CLOSE, state=DISABLED)
        self._view.menu_file.entryconfig(self._view.BTN_RELOAD_FROM_DISK, state=DISABLED)
        self._view.menu_export.entryconfig(self._view.BTN_EXPORT_AS_STAFF_GHOST, state=DISABLED)
        self._view.menu_export.entryconfig(self._view.BTN_EXPORT_AS_DOWNLOADED_GHOST, state=DISABLED)
        self._view.menu_export.entryconfig(self._view.BTN_EXTRACT_MII, state=DISABLED)
        # self.view.menu_edit.entryconfig(self.view.BTN_REPLACE_MII, state=DISABLED)
        # self.view.menu_edit.entryconfig(self.view.BTN_CHANGE_TRACK, state=DISABLED)
        self._view.lb_ghostfile.config(text="No ghost data loaded")

        # Remove Preview
        self._view.dataframe.grid_remove()

    def open_ct_changer(self):
        """ TODO """


    def change_ct(self):
        """ TODO """
        current_track_slot = COURSE_IDS[42]
        current_ct = next(self._db.get_mods())

        trackchange_view = PoltergustChangeTrackView(self._view.root, current_track_slot, current_mod=current_ct)
        trackchange_controller = TrackChangeController(trackchange_view)

    def open_ct_manager(self):
        """ TODO """
        ctmanager_view = PoltergustCTManagerView(self._view.root, self._db.get_mods())
        CTListController(ctmanager_view)

    def parse_filename(self, filepath: str):
        """ Invokes a parser to read ghost data from a ghost's filename """
        filename = filepath.rpartition("/")[2].rpartition(".")[0]
        self.filename_data = MK8GhostFilenameParser().parse(filename)
        self.ghost_has_header = MK8GhostDataParser().check_header(filepath)

    def extract_mii(self):
        """ Invokes the Mii handler and extracts the Mii from the currently loaded ghost file """
        filepath = self._view.select_mii_output_folder(f"mii-{self.filename_data.playername}")
        if not filepath:
            # Operation cancelled
            return

        handler = MK8GhostFilenameDataMiiHandler(self.ghostfile, self.ghost_has_header)

        try:
            handler.extract(filepath)
        except Exception as e:
            print(e)
            messagebox.showerror("Invalid Mii Data", "This ghost file contained invalid Mii data; it could not be extracted.")
            return

        messagebox.showinfo("Mii extracted!", f"The Mii for this ghost file was extracted successfully to {filepath}")

    def replace_mii(self):
        """ Invokes the Mii handler and replaces the Mii from the currently loaded ghost file """
        assert self.ghostfile is not None

        new_mii = self._view.select_mii_file()

        if not new_mii:
            # Operation cancelled
            return

        handler = MK8GhostFilenameDataMiiHandler(self.ghostfile, self.ghost_has_header)

        try:
            handler.replace(new_mii)
        except Exception as e:
            print(e)
            messagebox.showerror("Invalid Mii Data", "This Mii file contained invalid Mii data; it could not be injected.")
            return

        # Generate new filename
        mii_name = handler.extract_mii_name()
        self.filename_data.playername = mii_name
        serializer = MK8GhostFilenameSerializer()
        new_name = serializer.serialize(self.filename_data)

        # Rename file
        current_folder = self.ghostfile.rpartition("/")[0]
        new_file = current_folder + "/" + new_name
        os.rename(self.ghostfile, new_file)

        self.ghostfile = new_file

        messagebox.showinfo("Mii replaced!", f"The Mii for this ghost file was successfully replaced!")

    def export_as_staff(self) -> None:
        """ Exports the currently loaded ghostfile as a staff ghost """
        assert self.ghostfile is not None
        output_folder = self._view.select_conversion_staff_output_folder()
        if output_folder is None:
            # Operation cancelled
            return
        converter = MK8GhostConverter()
        output_file = converter.export_as_staff(self.ghostfile, self.filename_data, self.ghost_has_header, output_folder)

        messagebox.showinfo("Staff Ghost Exported", f"Staff Ghost data was exported successfully! It can be found under {output_file}")

    def export_as_downloaded(self, ghost_slot: int = 0) -> None:
        """ Exports the currently loaded ghostfile as a downloaded ghost """
        assert self.ghostfile is not None
        output_folder = self._view.select_conversion_download_output_folder()
        if not output_folder:
            # Operation cancelled
            return

        converter = MK8GhostConverter()
        output_file = converter.export_as_downloaded(self.ghostfile, self.filename_data, self.ghost_has_header, output_folder, ghost_slot)

        messagebox.showinfo("Downloaded Ghost Exported", f"Downloaded Ghost data was exported successfully! It can be found under {output_file}")

    def update(self):
        """ Updates the UI contents based on the loaded ghostfile """
        assert self.ghostfile is not None

        # Enable buttons if a file is open
        self._view.menu_file.entryconfig(self._view.BTN_CLOSE, state=NORMAL)
        self._view.menu_file.entryconfig(self._view.BTN_RELOAD_FROM_DISK, state=NORMAL)
        self._view.menu_export.entryconfig(self._view.BTN_EXPORT_AS_STAFF_GHOST, state=NORMAL)
        self._view.menu_export.entryconfig(self._view.BTN_EXPORT_AS_DOWNLOADED_GHOST, state=NORMAL)
        self._view.menu_export.entryconfig(self._view.BTN_EXTRACT_MII, state=NORMAL)
        # self.view.menu_edit.entryconfig(self.view.BTN_REPLACE_MII, state=NORMAL)
        self._view.menu_edit.entryconfig(self._view.BTN_CHANGE_TRACK, state=NORMAL)
        self._view.menu_edit.entryconfig(self._view.BTN_CHANGE_TRACK, state=NORMAL)

        # Enable all download ghost slots
        for i in range(16):
            self._view.menu_export_download.entryconfig(self._view.BTN_DOWNLOADED_GHOST_SLOT_PREFIX + str(i), state=NORMAL)

        # Name of opened file (truncate it)
        file_str = "Loaded File: " + self.ghostfile.rpartition("/")[2][:40]
        if len(self.ghostfile) > 40:
            file_str += "..."
        self._view.lb_ghostfile.config(text=file_str)

        # Parse file
        self.parse_filename(self.ghostfile)

        # Update ghostinfos
        self._view.game_version.config(text=f"Game version {self.filename_data.game_version.value}")
        self._view.set_ghost_type(self.filename_data.ghost_type, self.filename_data.ghost_number, self.ghost_has_header)

        # Update Images
        self._view.set_flag(self.filename_data.flag_id)
        self._view.set_character(self.filename_data.character_id, self.filename_data.character_variant_id, self.filename_data.mii_weight_class_id)
        self._view.set_vehicle_parts(self.filename_data.kart_id, self.filename_data.wheels_id, self.filename_data.glider_id)

        # Update track preview image
        track_id = self.filename_data.track_id
        if self.filename_data.ghost_type != MK8GhostType.DOWNLOADED_GHOST and self.filename_data.track_id - 16 != self.filename_data.ghost_number:
            # Track ID - 16 matches ghost number, but only for non-download ghosts
            track_id = None
        self._view.set_track(track_id, self.filename_data.ghost_number)

        # Update text
        self._view.playername.set(self.filename_data.playername)
        self._view.total_min.set(self.filename_data.total_minutes)
        self._view.total_sec.set(f"{self.filename_data.total_seconds:02d}")
        self._view.total_ms.set(f"{self.filename_data.total_ms:03d}")

        # Set lap splits
        for i, lap in enumerate(self._view.lap_splits):
            lap_mins = getattr(self.filename_data, f'lap{i+1}_minutes')
            if lap_mins is not None:
                lap['min'][0].set(lap_mins)
                lap['sec'][0].set(f"{getattr(self.filename_data, f'lap{i+1}_seconds'):02d}")
                lap['ms'][0].set(f"{getattr(self.filename_data, f'lap{i+1}_ms'):03d}")
            else:
                lap['min'][0].set("9")
                lap['sec'][0].set("59")
                lap['ms'][0].set("999")

        # Show Preview
        self._view.dataframe.grid()




