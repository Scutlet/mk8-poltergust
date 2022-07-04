from dataclasses import dataclass, field
from itertools import count
from tkinter import *
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteCombobox

from enum import Enum
from PIL import Image, ImageTk

from gamedata import COURSE_IDS
from utils import AutocompleteKeyValueCombobox, PoltergustPopup, get_resource_path
from downloader import MOD_SITES


class PoltergustAddCTView(PoltergustPopup):
    """
        Displays a window to add a custom track to Poltergust's storage.
    """
    window_title = "Poltergust - Add Custom Track"
    window_width = 300
    window_height = 245

    mod_site_choices = {site.name: site for site in MOD_SITES}

    def __init__(self, master: Tk, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Info
        ttk.Label(self, text="Fetch Custom Track Info", font=14).pack(padx=5, pady=5)
        ttk.Label(self, wraplength=self.window_width, text="In order to link a ghost file to a mod, Poltergust first needs to add it to its local mod repository. To do so, enter the URL to the mod's (GameBanana or CT Wiki) page.").pack(fill=X, padx=5)
        ttk.Label(self, wraplength=self.window_width, text="Note: Mod information that was embedded earlier by Poltergust in Ghost Files is automatically added to Poltergust's mod repository.").pack(fill=X, padx=5)

        ttk.Separator(self, orient=HORIZONTAL).pack(fill=X, padx=4, pady=(8, 4))

        # Input
        self.ct_url = StringVar()
        ttk.Label(self, text="Custrom Track URL:").pack(fill=X, padx=5, pady=(5, 2))
        ttk.Entry(self, width=16, textvariable=self.ct_url).pack(fill=X, padx=5)

        self.fetch_button = Button(self, text="Fetch Mod Info")
        self.fetch_button.pack(pady=6)
