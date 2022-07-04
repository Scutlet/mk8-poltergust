from tkinter import *
from tkinter import ttk

from downloader import MOD_SITES
from gamedata import COURSE_IDS
from utils import AutocompleteKeyValueCombobox, PoltergustPopup



class PoltergustChangeTrackView(PoltergustPopup):
    """
        Displays a window to change a ghost's track slot and/or assign a custom track ID.
        Supported CT IDs include those from the TockDom MK8 wiki or GameBanana.
    """
    window_title = "Poltergust - Change Ghost Track"
    window_width = 300
    window_height = 200

