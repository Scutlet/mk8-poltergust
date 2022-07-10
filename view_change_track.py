from idlelib.tooltip import Hovertip
from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD, NORMAL as FONT_NORMAL

from downloader import MOD_SITES, MK8CustomTrack
from pg_dataclasses import MK8Course
from utils import PoltergustBlockingPopup
from widgets import IconButton, IntEntry



class PoltergustChangeTrackView(PoltergustBlockingPopup):
    """
        Displays a window to change a ghost's track slot and/or assign a custom track ID.
        Supported CT IDs include those from the TockDom MK8 wiki or GameBanana.
    """
    window_title = "Poltergust - Change Ghost Track"
    window_width = 300
    window_height = 250

    FONT = ("Courier", 9, FONT_NORMAL)
    FONT_TITLE = ("TkDefaultfont", 14, BOLD)

    # Add mod sites
    mod_site_choices = {site.name: site for site in MOD_SITES}

    def __init__(self, master: Tk, current_track_slot_index: MK8Course, *args, current_mod: MK8CustomTrack|None=None, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Track slot selection
        ttk.Label(self, wraplength=135, text="Track Slot").pack()
        track_slot_frame = current_track_slot_index.frame(self)
        track_slot_frame.pack(fill=X, padx=(4, 4), pady=(4, 4))

        ttk.Separator(self, orient=HORIZONTAL).pack(fill=X, padx=4, pady=(8, 4))

        # Custom track selection
        ttk.Label(self, text="Custom Track", font=self.FONT_TITLE).pack()

        # Buttons
        button_frame = Frame(self)
        button_frame.pack(fill=X)

        self.clear_button = IconButton(button_frame, text="Clear Track", image_path='resources/icons/trash-solid.png')
        self.clear_button.pack(side=RIGHT, padx=(0, 4))

        change_kwargs = {
            "text": "Change Track",
            "image_path": "resources/icons/pen-solid.png"
        }
        if current_mod is None:
            self.clear_button.config(state=DISABLED)
            change_kwargs["text"] = "Select Track"
            change_kwargs["image_path"] = "resources/icons/plus-solid.png"

        self.change_button = IconButton(button_frame, **change_kwargs)
        self.change_button.pack(side=LEFT, padx=(4, 0))

        # CT Preview
        mod_frame = current_mod.frame(self)
        mod_frame.pack(fill=X, padx=(4, 4), pady=(4, 4))

        # Version frame
        version_frame = Frame(self)
        version_frame.pack(fill=X)
        ttk.Label(version_frame, text="Version").pack(side=LEFT, padx=(4, 4))
        Hovertip(version_frame, f"Version of the mod the ghost was recorded in: <major>.<minor>.<patch>", hover_delay=1000)

        # Version boxes
        self.ct_version_major = IntVar()
        self.ct_version_minor = IntVar()
        self.ct_version_patch = IntVar()

        ct_version_major_entry = IntEntry(version_frame, width=3, textvariable=self.ct_version_major, font=self.FONT)
        ct_version_minor_entry = IntEntry(version_frame, width=3, textvariable=self.ct_version_minor, font=self.FONT)
        ct_version_patch_entry = IntEntry(version_frame, width=3, textvariable=self.ct_version_patch, font=self.FONT)

        ct_version_major_entry.pack(side=LEFT)
        ttk.Label(version_frame, text=".").pack(side=LEFT)
        ct_version_minor_entry.pack(side=LEFT)
        ttk.Label(version_frame, text=".").pack(side=LEFT)
        ct_version_patch_entry.pack(side=LEFT)
