from dataclasses import dataclass, field
from itertools import count
from tkinter import *
from tkinter import ttk

from enum import Enum
from PIL import Image, ImageTk

from utils import PoltergustPopup
from view_change_track import MK8ModSite, MOD_SITES

@dataclass
class MK8ModVersion:
    major: int
    minor: int
    patch: int = 0

    def __str__(self):
        return f"v{self.major}.{self.minor}.{self.patch}"

@dataclass
class MK8CustomTrack:
    name: str
    mod_version: MK8ModVersion
    mod_site: MK8ModSite
    mod_id: str

TEMP_TRACKS = (
    MK8CustomTrack(name="Wii Dry Dry Ruins (Scutlet)", mod_version=MK8ModVersion(1, 0, 0), mod_site=MOD_SITES[0], mod_id="180"),
    MK8CustomTrack(name="Cavi Cape Cliffside", mod_version=MK8ModVersion(1, 0, 0), mod_site=MOD_SITES[0], mod_id="181"),
    MK8CustomTrack(name="Rosalina's Crystal Lagoon", mod_version=MK8ModVersion(1, 0, 0), mod_site=MOD_SITES[0], mod_id="182"),
    MK8CustomTrack(name="Wario Circuit", mod_version=MK8ModVersion(1, 0, 0), mod_site=MOD_SITES[0], mod_id="189"),
    MK8CustomTrack(name="Tour Ninja Hideaway (voidsource)", mod_version=MK8ModVersion(1, 0, 0), mod_site=MOD_SITES[0], mod_id="188"),
)



class PoltergustCTManagerView(PoltergustPopup):
    """
        Displays a window of all cached CTs.
    """
    window_title = "Poltergust - Custom Track Manager"
    window_width = 300
    window_height = 200

    # Add mod sites
    mod_site_choices = {site.name: (site.id, site.domain, site.api_endpoint) for site in MOD_SITES}

    def __init__(self, master: Tk, track_list: list[MK8CustomTrack], *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Search Box
        self.search_value = StringVar()
        self.search_value.trace_add("write", lambda var, index, mode: self.reload_list())
        ttk.Entry(self, width=16, textvariable=self.search_value).pack()

        # Scrollbar


        # Track list





        self.canvas = Canvas(self, bd=0)
        vsb = Scrollbar(self, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side=RIGHT, fill=Y)
        self.vsb = vsb
        self.canvas.pack(side=RIGHT, fill=BOTH, expand=True)

        self.track_frame = ttk.Frame(self.canvas)

        self.track_frame.pack()
        self.track_widgets = self._build_track_list(track_list)

        self.reload_list()

        self.canvas.create_window(0, 0, anchor="nw", window=self.track_frame, tags=("inner",))

        self.canvas.bind("<Configure>", self._resize_inner_frame)
        self.track_frame.bind("<Configure>", self._reset_scrollregion)



        self.canvas.bind_all("<MouseWheel>", self._set_scroll)
        self.canvas.bind_all("<Button-4>", self._set_scroll)
        self.canvas.bind_all("<Button-5>", self._set_scroll)


    def _set_scroll(self, event):
        """ Moves the scrollbar when the user scrolls the mouse wheel """
        amount = -1
        if event.num == 5 or event.delta < 0:
            # Scrolling down instead
            amount = 1
        self.canvas.yview_scroll(amount, "units")

    def _reset_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_inner_frame(self, event):
        self.canvas.itemconfig("inner", width=event.width)


    def _build_track_list(self, track_list: list[MK8CustomTrack]) -> list[tuple[MK8CustomTrack, Widget]]:
        """ TODO """
        track_widgets = []

        for track in sorted(track_list, key=lambda item: item.name):
            frame = ttk.LabelFrame(self.track_frame)
            ttk.Label(frame, wraplength=135, text=track.name).pack(side=TOP, fill='x')
            ttk.Label(frame, wraplength=135, text=track.mod_version).pack(side=LEFT)
            ttk.Label(frame, wraplength=135, text=track.mod_site).pack(side=LEFT)
            ttk.Label(frame, wraplength=135, text=track.mod_id).pack(side=LEFT)
            track_widgets.append((track, frame))
        return track_widgets

    def reload_list(self):
        """ TODO """
        search_value = self.search_value.get().lower()
        print("reloading track list")
        for track, widget in self.track_widgets:
            widget.pack_forget()
            if not search_value or search_value in track.name.lower():
                widget.pack(fill='both', padx=(2, 5))
                # widget.pack()


