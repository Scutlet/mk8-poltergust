import os
from tkinter import *
from tkinter import messagebox
from ct_storage import MK8CTStorage
from downloader import PoltergustDownloader

from gamedata import MK8GhostType
from filename_parser import MK8GhostFilenameData, MK8GhostFilenameParser, MK8GhostFilenameSerializer
from ghost_converter import MK8GhostConverter
from ghost_file_parser import MK8GhostDataParser
from mii_handler import MK8GhostFilenameDataMiiHandler
from view_change_track import PoltergustChangeTrackView
from view_ct_add import PoltergustAddCTView
from view_ct_manager import PoltergustCTManagerView
from view_main import PoltergustMainView


class PoltergustController:
    """ Controller for the application. It invokes models/parsers and controls the view/UI state """

    def __init__(self, view: PoltergustMainView, db: MK8CTStorage):
        self.ghostfile: str = None
        self.filename_data: MK8GhostFilenameData = None
        self.ghost_has_header = None
        self.view = view
        self.db = db
        self.downloader = PoltergustDownloader()

        # Setup Menu callbacks
        self.view.menu_file.entryconfig(self.view.BTN_OPEN, command=self.open_ghostfile)
        self.view.menu_file.entryconfig(self.view.BTN_CLOSE, command=self.close_ghostfile)
        self.view.menu_file.entryconfig(self.view.BTN_RELOAD_FROM_DISK, command=self.update)

        # Setup Export callbacks
        self.view.menu_export.entryconfig(self.view.BTN_EXTRACT_MII, command=self.extract_mii)
        self.view.menu_export.entryconfig(self.view.BTN_EXPORT_AS_STAFF_GHOST, command=self.export_as_staff)
        for slot in range(16):
            self.view.menu_export_download.entryconfig(self.view.BTN_DOWNLOADED_GHOST_SLOT_PREFIX+str(slot), command=lambda bound_slot=slot: self.export_as_downloaded(bound_slot))

        # Setup Edit callbacks
        # self.view.menu_edit.entryconfig(self.view.BTN_REPLACE_MII, command=self.replace_mii)
        self.view.menu_edit.entryconfig(self.view.BTN_CHANGE_TRACK, command=self.add_ct)
        # self.view.menu_edit.entryconfig(self.view.BTN_CHANGE_TRACK, command=lambda: PoltergustChangeTrackView(self.view.root))

        # CT Manager
        self.view.menubar.entryconfig(self.view.BTN_CT_MANAGER, command=lambda: PoltergustCTManagerView(self.view.root, self.db.get_mods()))

        self.close_ghostfile()

    def open_ghostfile(self):
        """ Invokes the view to select a ghost file, and loads its data """
        filename = self.view.select_ghost_file()
        # Selection is empty if it was aborted
        if not filename:
            return

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
        self.view.menu_file.entryconfig(self.view.BTN_CLOSE, state=DISABLED)
        self.view.menu_file.entryconfig(self.view.BTN_RELOAD_FROM_DISK, state=DISABLED)
        self.view.menu_export.entryconfig(self.view.BTN_EXPORT_AS_STAFF_GHOST, state=DISABLED)
        self.view.menu_export.entryconfig(self.view.BTN_EXPORT_AS_DOWNLOADED_GHOST, state=DISABLED)
        self.view.menu_export.entryconfig(self.view.BTN_EXTRACT_MII, state=DISABLED)
        # self.view.menu_edit.entryconfig(self.view.BTN_REPLACE_MII, state=DISABLED)
        # self.view.menu_edit.entryconfig(self.view.BTN_CHANGE_TRACK, state=DISABLED)
        self.view.lb_ghostfile.config(text="No ghost data loaded")

        # Remove Preview
        self.view.dataframe.grid_remove()

    def add_ct(self):
        """ Opens up a new UI to fetch a new CT """
        ct_view = PoltergustAddCTView(self.view.root)
        ct_view.fetch_button.config(command=lambda: self.downloader.download(ct_view.ct_url.get()))
        # TODO: Get <Enter> key to work
        # self.view.root.bind('<Return>', lambda: self.downloader.download(ct_view.ct_url.get()))

    def parse_filename(self, filepath: str):
        """ Invokes a parser to read ghost data from a ghost's filename """
        filename = filepath.rpartition("/")[2].rpartition(".")[0]
        self.filename_data = MK8GhostFilenameParser().parse(filename)
        self.ghost_has_header = MK8GhostDataParser().check_header(filepath)

    def extract_mii(self):
        """ Invokes the Mii handler and extracts the Mii from the currently loaded ghost file """
        filepath = self.view.select_mii_output_folder(f"mii-{self.filename_data.playername}")
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

        new_mii = self.view.select_mii_file()

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
        output_folder = self.view.select_conversion_staff_output_folder()
        if output_folder is None:
            # Operation cancelled
            return
        converter = MK8GhostConverter()
        output_file = converter.export_as_staff(self.ghostfile, self.filename_data, self.ghost_has_header, output_folder)

        messagebox.showinfo("Staff Ghost Exported", f"Staff Ghost data was exported successfully! It can be found under {output_file}")

    def export_as_downloaded(self, ghost_slot: int = 0) -> None:
        """ Exports the currently loaded ghostfile as a downloaded ghost """
        assert self.ghostfile is not None
        output_folder = self.view.select_conversion_download_output_folder()
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
        self.view.menu_file.entryconfig(self.view.BTN_CLOSE, state=NORMAL)
        self.view.menu_file.entryconfig(self.view.BTN_RELOAD_FROM_DISK, state=NORMAL)
        self.view.menu_export.entryconfig(self.view.BTN_EXPORT_AS_STAFF_GHOST, state=NORMAL)
        self.view.menu_export.entryconfig(self.view.BTN_EXPORT_AS_DOWNLOADED_GHOST, state=NORMAL)
        self.view.menu_export.entryconfig(self.view.BTN_EXTRACT_MII, state=NORMAL)
        # self.view.menu_edit.entryconfig(self.view.BTN_REPLACE_MII, state=NORMAL)
        self.view.menu_edit.entryconfig(self.view.BTN_CHANGE_TRACK, state=NORMAL)
        self.view.menu_edit.entryconfig(self.view.BTN_CHANGE_TRACK, state=NORMAL)

        # Enable all download ghost slots
        for i in range(16):
            self.view.menu_export_download.entryconfig(self.view.BTN_DOWNLOADED_GHOST_SLOT_PREFIX + str(i), state=NORMAL)

        # Name of opened file (truncate it)
        file_str = "Loaded File: " + self.ghostfile.rpartition("/")[2][:40]
        if len(self.ghostfile) > 40:
            file_str += "..."
        self.view.lb_ghostfile.config(text=file_str)

        # Parse file
        self.parse_filename(self.ghostfile)

        # Update ghostinfos
        self.view.game_version.config(text=f"Game version {self.filename_data.game_version.value}")
        self.view.set_ghost_type(self.filename_data.ghost_type, self.filename_data.ghost_number, self.ghost_has_header)

        # Update Images
        self.view.set_flag(self.filename_data.flag_id)
        self.view.set_character(self.filename_data.character_id, self.filename_data.character_variant_id, self.filename_data.mii_weight_class_id)
        self.view.set_vehicle_parts(self.filename_data.kart_id, self.filename_data.wheels_id, self.filename_data.glider_id)

        # Update track preview image
        track_id = self.filename_data.track_id
        if self.filename_data.ghost_type != MK8GhostType.DOWNLOADED_GHOST and self.filename_data.track_id - 16 != self.filename_data.ghost_number:
            # Track ID - 16 matches ghost number, but only for non-download ghosts
            track_id = None
        self.view.set_track(track_id, self.filename_data.ghost_number)

        # Update text
        self.view.playername.set(self.filename_data.playername)
        self.view.total_min.set(self.filename_data.total_minutes)
        self.view.total_sec.set(f"{self.filename_data.total_seconds:02d}")
        self.view.total_ms.set(f"{self.filename_data.total_ms:03d}")

        # Set lap splits
        for i, lap in enumerate(self.view.lap_splits):
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
        self.view.dataframe.grid()




