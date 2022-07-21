import bisect
from tkinter import RIGHT, Y, Canvas, Event, Scrollbar, StringVar, Toplevel, Widget, ttk
from typing import Iterable

from poltergust.widgets.trackframes import FramableTrack, MK8TrackFrameBig


class ScrollableTrackCanvas(Canvas):
    """ A scrollable canvas that shows a list of FrameableTracks """
    def __init__(self, master: Toplevel, track_list: Iterable[FramableTrack], *args, search_widget:ttk.Entry|None=None, scrollable_region: Widget|None=None, **kwargs):
        super().__init__(master, *args, bd=0, borderwidth=0, highlightthickness=0, **kwargs)

        # Link search box
        self.search_value = StringVar()
        if search_widget is not None:
            self.search_value.trace_add("write", lambda var, index, mode: self.reload_list())
            search_widget.config(textvariable=self.search_value)

        # Scrollbar (only Canvas elements are scrollable)
        self.vsb = Scrollbar(master, command=self.yview)
        self.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side=RIGHT, fill=Y)

        # Track List
        self.track_frame = ttk.Frame(self)
        self.track_frame.pack()

        self.track_widgets = self._build_track_list(track_list)
        self.reload_list()

        # Make sure Tkinter knows what's scrollable
        self.create_window(0, 0, anchor="nw", window=self.track_frame, tags=("inner",))

        # Recalculate bounding box if the frame or window changes size
        self.bind("<Configure>", self._resize_inner_frame)
        self.track_frame.bind("<Configure>", self._reset_scrollregion)

        # Make the mouse wheel move the scrollbar
        scrollable_region = scrollable_region or master
        scrollable_region.bind("<MouseWheel>", self._set_scroll) # for Windows/MacOS
        scrollable_region.bind("<Button-4>", self._set_scroll) # for Linux
        scrollable_region.bind("<Button-5>", self._set_scroll) # for Linux

    def _set_scroll(self, event: Event):
        """ Moves the scrollbar when the user scrolls the mouse wheel """
        start, end = self.vsb.get()
        if start <= 0 and end >= 1:
            # There's nothing to scroll; Scrollbar is disabled
            return

        amount = -1
        if event.num == 5 or event.delta < 0:
            # Scrolling down instead
            amount = 1
        self.yview_scroll(amount, "units")

    def _reset_scrollregion(self, event: Event):
        self.configure(scrollregion=self.bbox("all"))

    def _resize_inner_frame(self, event: Event):
        self.itemconfig("inner", width=event.width)

    def _build_track_list(self, track_list: Iterable[FramableTrack]) -> list[tuple[FramableTrack, MK8TrackFrameBig]]:
        """ Constructs the track list by framing the provided FramableTracks """
        track_widgets = []
        for track in sorted(track_list, key=lambda item: item.sort_field):
            frame = track.frame(self.track_frame)
            track_widgets.append((track, frame))

        return track_widgets

    def reload_list(self) -> None:
        """ Reloads the FramableTrack list """
        search_value = self.search_value.get().lower()
        for track, widget in self.track_widgets:
            widget.pack_forget()
            if not search_value or search_value in track.sort_field.lower():
                widget.pack(fill='both', padx=(2, 5), pady=(0, 5))

    def add_track(self, track: FramableTrack) -> MK8TrackFrameBig:
        """ Adds a track to the view """
        # Remove existing track from the list if the id field matches
        indx = None
        for i, (existing_track, widget) in enumerate(self.track_widgets):
            if track == existing_track:
                indx = i
                widget.destroy()
                break
        if indx is not None:
            del self.track_widgets[indx]

        # Insert into sorted list
        mod_widget = track.frame(self.track_frame)
        bisect.insort(self.track_widgets, (track, mod_widget), key=lambda pair: pair[0].sort_field)
        self.reload_list()

        return mod_widget
