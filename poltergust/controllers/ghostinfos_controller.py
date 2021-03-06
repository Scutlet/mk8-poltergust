import logging
import os
from tkinter import *
from tkinter import messagebox
from poltergust.controllers.ctlist_controllers import CTListController, CTListDownloaderController
from poltergust.controllers.track_change import TrackChangeController
from poltergust.models.ct_storage import MK8CTStorage
from poltergust.models.mod_models import MK8ModVersion
from poltergust.parsers.downloader import MK8CustomTrack

from poltergust.models.game_models import UNKNOWN_COURSE, MK8Course, MK8GhostType
from poltergust.parsers.filecontent_parser import MK8GhostData, MK8GhostDataParser, MK8GhostDataSerializer
from poltergust.parsers.filename_parser import MK8GhostFilenameData, MK8GhostFilenameParser, MK8GhostFilenameSerializer
from poltergust.parsers.ghost_converter import MK8GhostConverter
from poltergust.parsers.mii_handler import MK8GhostFilenameDataMiiHandler
from poltergust.views.track_change_view import PoltergustChangeTrackView
from poltergust.views.ct_list_view import TrackListManagerView
from poltergust.views.main_view import PoltergustMainView


class PoltergustController:
    """ Controller for the application. It invokes models/parsers and controls the view/UI state """

    def __init__(self, view: PoltergustMainView):
        self.ghostfile: str = None
        self.filename_data: MK8GhostFilenameData = None
        self.ghost_data: MK8GhostData = None
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
        self._view.menu_edit.entryconfig(self._view.BTN_CHANGE_TRACK, command=self.open_ct_changer)

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
        self.ghost_data = None

        # Disable buttons
        self._view.menu_file.entryconfig(self._view.BTN_CLOSE, state=DISABLED)
        self._view.menu_file.entryconfig(self._view.BTN_RELOAD_FROM_DISK, state=DISABLED)
        self._view.menu_export.entryconfig(self._view.BTN_EXPORT_AS_STAFF_GHOST, state=DISABLED)
        self._view.menu_export.entryconfig(self._view.BTN_EXPORT_AS_DOWNLOADED_GHOST, state=DISABLED)
        self._view.menu_export.entryconfig(self._view.BTN_EXTRACT_MII, state=DISABLED)
        # self.view.menu_edit.entryconfig(self.view.BTN_REPLACE_MII, state=DISABLED)
        self._view.menu_edit.entryconfig(self._view.BTN_CHANGE_TRACK, state=DISABLED)
        self._view.lb_ghostfile.config(text="No ghost data loaded")

        # Remove Preview
        self._view.dataframe.grid_remove()

    def open_ct_changer(self):
        """ Initialises the popup that allows assigning a different track slot or custom track to the loaded ghost """
        current_track_slot = self.ghost_data.track_slot
        current_ct = self.ghost_data.mod
        current_mod_version = self.ghost_data.mod_version

        trackchange_view = PoltergustChangeTrackView(self._view.root, current_track_slot, current_mod=current_ct, mod_version=current_mod_version)
        trackchange_controller = TrackChangeController(trackchange_view)
        trackchange_controller.add_listener(self.on_track_change)

    def on_track_change(self, track_data: tuple[MK8Course, MK8CustomTrack|None, MK8ModVersion]):
        """ Changes the track slot and/or custom track assigned to the loaded ghostfile. """
        (track_slot, mod, mod_version) = track_data

        # Fix filename
        self.filename_data.track_id = track_slot.course_id
        if self.filename_data.ghost_type != MK8GhostType.DOWNLOADED_GHOST:
            self.filename_data.ghost_number = track_slot.course_id - 16

        serializer = MK8GhostFilenameSerializer()
        new_name = serializer.serialize(self.filename_data)

        # Rename file
        current_folder = self.ghostfile.rpartition("/")[0]
        new_file = current_folder + "/" + new_name
        os.rename(self.ghostfile, new_file)

        self.ghostfile = new_file

        # Inject ghost contents
        ghostdata = MK8GhostData(self.ghost_data.has_header, track_slot, mod, mod_version)
        filedata_serializer = MK8GhostDataSerializer()
        filedata_serializer.serialize(new_file, ghostdata)

        messagebox.showinfo("Track Change successful!", "Track data was successfully replaced.", parent=self._view.root)

        # Update view (reloads from disk)
        self.update()

    def open_ct_manager(self):
        """ Initialises the custom track manager """
        ctmanager_view = TrackListManagerView(self._view.root, self._db.get_mods())
        CTListDownloaderController(ctmanager_view)

    def parse_filename(self, filepath: str):
        """ Invokes a parser to read ghost data from a ghost's filename """
        filename = filepath.rpartition("/")[2].rpartition(".")[0]
        self.filename_data = MK8GhostFilenameParser().parse(filename)

    def parse_file_contents(self, filepath: str) -> None:
        """ Invokes the ghost data parser and stores its results """
        self.ghost_data = MK8GhostDataParser().parse(filepath)

    def extract_mii(self):
        """ Invokes the Mii handler and extracts the Mii from the currently loaded ghost file """
        filepath = self._view.select_mii_output_folder(f"mii-{self.filename_data.playername}")
        if not filepath:
            # Operation cancelled
            return

        handler = MK8GhostFilenameDataMiiHandler(self.ghostfile, self.ghost_data.has_header)

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

        handler = MK8GhostFilenameDataMiiHandler(self.ghostfile, self.ghost_data.has_header)

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
        output_file = converter.export_as_staff(self.ghostfile, self.filename_data, self.ghost_data.has_header, output_folder)

        messagebox.showinfo("Staff Ghost Exported", f"Staff Ghost data was exported successfully! It can be found under {output_file}")

    def export_as_downloaded(self, ghost_slot: int = 0) -> None:
        """ Exports the currently loaded ghostfile as a downloaded ghost """
        assert self.ghostfile is not None
        output_folder = self._view.select_conversion_download_output_folder()
        if not output_folder:
            # Operation cancelled
            return

        converter = MK8GhostConverter()
        output_file = converter.export_as_downloaded(self.ghostfile, self.filename_data, self.ghost_data.has_header, output_folder, ghost_slot)

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
        self.parse_file_contents(self.ghostfile)

        # Update ghostinfos
        self._view.game_version.config(text=f"Game version {self.filename_data.game_version.value}")
        self._view.set_ghost_type(self.filename_data.ghost_type, self.filename_data.ghost_number, self.ghost_data.has_header)

        # Update Images
        self._view.set_motion_control(self.filename_data.motion_control_flag)
        self._view.set_flag(self.filename_data.flag_id)
        self._view.set_character(self.filename_data.character_id, self.filename_data.character_variant_id, self.filename_data.mii_weight_class_id)
        self._view.set_vehicle_parts(self.filename_data.kart_id, self.filename_data.wheels_id, self.filename_data.glider_id)

        # Update track preview image
        track_id = self.filename_data.track_id
        if self.filename_data.ghost_type != MK8GhostType.DOWNLOADED_GHOST and self.filename_data.track_id - 16 != self.filename_data.ghost_number:
            # Track ID - 16 matches ghost number, but only for non-download ghosts
            logging.warning(f"Found corrupted filename data! Track ID: {self.filename_data.track_id}, Ghost Type: {self.filename_data.ghost_type}, Ghost Number: {self.filename_data.ghost_number}")
            messagebox.showwarning("Corrupted filename!", "The trackID in the ghost's filename was corrupted. You can fix this by manually assigning a track to this ghost under 'Edit -> Change Track'.")
            track_id = None

        if track_id is not None and track_id != self.ghost_data.track_slot.course_id:
            logging.warning(f"Track ID in filename and in ghost file did not match up! Filename: {self.filename_data.track_id}, Content: {self.ghost_data.track_slot.course_id}")
            messagebox.showwarning("Corrupted filename or ghost file!", "The trackID in the ghost's filename and file contents did not match up. You can fix this by manually assigning a track to this ghost under 'Edit -> Change Track'.")
            track_id = None

        track = self.ghost_data.track_slot
        if track_id is None:
            track = UNKNOWN_COURSE

        mod = self.ghost_data.mod
        self._view.set_track(track, mod, self.ghost_data.mod_version)

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




