from dataclasses import dataclass, field
from itertools import count
from tkinter import *
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteCombobox

from enum import Enum
from PIL import Image, ImageTk

from gamedata import COURSE_IDS
from utils import AutocompleteKeyValueCombobox, PoltergustPopup, get_resource_path

@dataclass
class MK8ModSite:
    id: int = field(default_factory=count().__next__, init=False)
    name: str
    domain: str
    api_endpoint: str
    icon: Image.Image|None = None

    def __str__(self):
        return self.name

MOD_SITES = (
    MK8ModSite(name="CT Wiki", domain="mk8.tockdom.com", api_endpoint="mk8.tockdom.com/%s"),
    MK8ModSite(name="GameBanana", domain="gamebanana.com", api_endpoint="gamebanana.com/mods/%s"),
)
