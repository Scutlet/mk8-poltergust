from idlelib.tooltip import Hovertip
from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD, NORMAL as FONT_NORMAL
from poltergust.models.mod_models import MK8ModVersion

from poltergust.parsers.downloader import API_MOD_SITES, MK8CustomTrack
from poltergust.models.game_models import MK8Course
from poltergust.utils import PoltergustBlockingPopup
from poltergust.widgets.widgets import IconButton, IntEntry



class PoltergustChangeTrackView(PoltergustBlockingPopup):
    """
        Displays a window to change a ghost's track slot and/or assign a custom track ID.
        Supported CT IDs include those from the TockDom MK8 wiki or GameBanana.
    """
    window_title = "Poltergust - Change Ghost Track"
    window_width = 300
    window_height = 325

    FONT = ("Courier", 9, FONT_NORMAL)
    FONT_TITLE = ("TkDefaultfont", 14, BOLD)

    # Add mod sites
    mod_site_choices = {site.name: site for site in API_MOD_SITES}

    def __init__(self, master: Toplevel, current_track_slot: MK8Course, *args, current_mod: MK8CustomTrack|None=None, mod_version: MK8ModVersion|None=None, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Track slot selection
        self.track_slot = None
        # Custom track selection
        ttk.Label(self, text="Track Slot", font=self.FONT_TITLE).pack(pady=(0, 2))

        # Track Slot Buttons
        button_frame = Frame(self)
        button_frame.pack(fill=X)
        self.change_track_slot_button = IconButton(button_frame, text="Change Track", image_path="resources/icons/pen-solid.png")
        self.change_track_slot_button.pack(side=LEFT, padx=(4, 0))

        # Track Slot Preview
        self.static_track_frame = Frame(self)
        self.static_track_frame.pack(fill=X, padx=(4, 4), pady=(4, 4))
        self.set_track_slot(current_track_slot)

        ttk.Separator(self, orient=HORIZONTAL).pack(fill=X, padx=4, pady=(8, 4))

        # Custom track selection
        ttk.Label(self, text="Custom Track", font=self.FONT_TITLE).pack(pady=(0, 2))

        # Custom Track Buttons
        button_frame = Frame(self)
        button_frame.pack(fill=X)

        self.change_ct_button = IconButton(button_frame)
        self.change_ct_button.pack(side=LEFT, padx=(4, 0))

        self.clear_ct_button = IconButton(button_frame, text="Clear Track", image_path='resources/icons/trash-solid.png')
        self.clear_ct_button.pack(side=RIGHT, padx=(0, 4))

        # Custom Track Preview
        self.mod = None
        self.static_mod_frame = Frame(self)
        self.static_mod_frame.pack(fill=X, padx=(4, 4), pady=(4, 4))

        # Version frame
        self.version_frame = Frame(self)
        self.version_frame.pack(fill=X)
        ttk.Label(self.version_frame, text="Version").pack(side=LEFT, padx=(4, 4))
        Hovertip(self.version_frame, f"Version of the mod the ghost was recorded in: <major>.<minor>.<patch>", hover_delay=1000)

        # Version boxes
        self.ct_version_major = IntVar(value=1)
        self.ct_version_minor = IntVar(value=0)
        self.ct_version_patch = IntVar(value=0)

        ct_version_major_entry = IntEntry(self.version_frame, width=3, textvariable=self.ct_version_major, font=self.FONT)
        ct_version_minor_entry = IntEntry(self.version_frame, width=3, textvariable=self.ct_version_minor, font=self.FONT)
        ct_version_patch_entry = IntEntry(self.version_frame, width=3, textvariable=self.ct_version_patch, font=self.FONT)

        ct_version_major_entry.pack(side=LEFT)
        ttk.Label(self.version_frame, text=".").pack(side=LEFT)
        ct_version_minor_entry.pack(side=LEFT)
        ttk.Label(self.version_frame, text=".").pack(side=LEFT)
        ct_version_patch_entry.pack(side=LEFT)

        self.set_mod(current_mod)
        if mod_version is not None:
            self.set_mod_version(mod_version)

        # Save button
        self.save_button = IconButton(self, text=" Save Changes", image_path='resources/icons/floppy-disk-solid.png')
        self.save_button.pack(side=BOTTOM, pady=(8, 8))

        ttk.Separator(self, orient=HORIZONTAL).pack(side=BOTTOM, fill=X, padx=4)

    def set_track_slot(self, track: MK8Course) -> None:
        """ Changes the selected track slot """
        if self.track_slot is not None:
            self.static_track_frame.winfo_children()[0].destroy()

        track.frame(self.static_track_frame).pack(fill=X)
        self.track_slot = track

    def set_mod(self, mod: MK8CustomTrack) -> None:
        """ Changes the selected custom track """
        if self.mod is not None:
            self.static_mod_frame.winfo_children()[0].destroy()

        self.mod = mod
        if mod is None:
            self.clear_ct_button.config(state=DISABLED)
            self.change_ct_button.set_icon("resources/icons/plus-solid.png")
            self.change_ct_button.config(text=" Select Track")
            self.version_frame.pack_forget()
            return

        self.clear_ct_button.config(state=NORMAL)
        self.change_ct_button.set_icon("resources/icons/pen-solid.png")
        self.change_ct_button.config(text=" Change Track")
        self.version_frame.pack(fill=X)
        mod.frame(self.static_mod_frame).pack(fill=X)

    def set_mod_version(self, mod_version: MK8ModVersion) -> None:
        """ Changes the provided custom track version """
        self.ct_version_major.set(mod_version.major)
        self.ct_version_minor.set(mod_version.minor)
        self.ct_version_patch.set(mod_version.patch)


