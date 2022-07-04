from dataclasses import dataclass, field
from itertools import count
from tkinter import *
from tkinter import ttk

from enum import Enum
from PIL import Image, ImageTk

from downloader import MK8CustomTrack, MK8ModSite, MOD_SITES
from utils import PoltergustPopup


class PoltergustCTManagerView(PoltergustPopup):
    """
        Displays a window of all cached CTs.
    """
    window_title = "Poltergust - Custom Track Manager"
    window_width = 300
    window_height = 200

    # Add mod sites
    mod_site_choices = {site.name: site for site in MOD_SITES}

    def __init__(self, master: Tk, track_list: list[MK8CustomTrack], *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Search Box
        self.search_value = StringVar()
        self.search_value.trace_add("write", lambda var, index, mode: self.reload_list())
        ttk.Entry(self, width=16, textvariable=self.search_value).pack()

        # Only canvas elements are scrollable
        self.canvas = Canvas(self, bd=0)
        vsb = Scrollbar(self, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)

        # Scrollbar
        vsb.pack(side=RIGHT, fill=Y)
        self.vsb = vsb
        self.canvas.pack(side=RIGHT, fill=BOTH, expand=True)

        # Track List
        self.track_frame = ttk.Frame(self.canvas)
        self.track_frame.pack()
        self.track_widgets = self._build_track_list(track_list)
        self.reload_list()

        # Make sure Tkinter knows what's scrollable
        self.canvas.create_window(0, 0, anchor="nw", window=self.track_frame, tags=("inner",))

        # Recalculate bounding box if the frame or window changes size
        self.canvas.bind("<Configure>", self._resize_inner_frame)
        self.track_frame.bind("<Configure>", self._reset_scrollregion)

        # Make the mouse wheel move the scrollbar
        self.canvas.bind_all("<MouseWheel>", self._set_scroll) # for Windows/MacOS
        self.canvas.bind_all("<Button-4>", self._set_scroll) # for Linux
        self.canvas.bind_all("<Button-5>", self._set_scroll) # for Linux

    def _set_scroll(self, event):
        """ Moves the scrollbar when the user scrolls the mouse wheel """
        start, end = self.vsb.get()
        if start <= 0 and end >= 1:
            # There's nothing to scroll; Scrollbar is disabled
            return

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
            ttk.Label(frame, wraplength=135, text=track.mod_site).pack(side=LEFT)
            ttk.Label(frame, wraplength=135, text=track.mod_id).pack(side=LEFT)
            track_widgets.append((track, frame))
        return track_widgets

    def reload_list(self):
        """ TODO """
        search_value = self.search_value.get().lower()
        for track, widget in self.track_widgets:
            widget.pack_forget()
            if not search_value or search_value in track.name.lower():
                widget.pack(fill='both', padx=(2, 5))
