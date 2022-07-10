import bisect
from tkinter import *
from tkinter import ttk

from utils import PoltergustBlockingPopup, get_resource_path
from widgets import FramableTrack, IconButton

class ScrollableTrackCanvas(Canvas):
    """ TODO """
    def __init__(self, master: Tk, track_list: list[FramableTrack], *args, search_widget:ttk.Entry|None=None, **kwargs):
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
        master.bind("<MouseWheel>", self._set_scroll) # for Windows/MacOS
        master.bind("<Button-4>", self._set_scroll) # for Linux
        master.bind("<Button-5>", self._set_scroll) # for Linux

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
        self.yview_scroll(amount, "units")

    def _reset_scrollregion(self, event):
        self.configure(scrollregion=self.bbox("all"))

    def _resize_inner_frame(self, event):
        self.itemconfig("inner", width=event.width)

    def _build_track_list(self, track_list: list[FramableTrack]) -> list[tuple[FramableTrack, Widget]]:
        """ TODO """
        track_widgets = []
        for track in sorted(track_list, key=lambda item: item.sort_field):
            track_widgets.append((track, track.frame(self.track_frame)))

        return track_widgets

    def reload_list(self) -> None:
        """ TODO """
        search_value = self.search_value.get().lower()
        for track, widget in self.track_widgets:
            widget.pack_forget()
            if not search_value or search_value in track.sort_field.lower():
                widget.pack(fill='both', padx=(2, 5), pady=(0, 5))

    def add_track(self, track: FramableTrack) -> None:
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


class PoltergustCTManagerView(PoltergustBlockingPopup):
    """
        Displays a window of all cached CTs.
    """
    window_title = "Poltergust - Custom Track Database"
    window_width = 310
    window_height = 400

    BASE_FONT = "TkDefaultFont"

    def __init__(self, master: Tk, track_list: list[FramableTrack], *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Top frame
        top = Frame(self)
        top.pack(padx=5, pady=6, fill=X)

        # Add CT Box
        self.add_button = IconButton(top, text="Add a mod", image_path='resources/icons/plus-solid.png')
        self.add_button.pack(side=LEFT)

        # Search Box
        search_widget = ttk.Entry(top, width=25)
        search_widget.pack(side=RIGHT)

        # Search Icon
        self._search_img = PhotoImage(file=get_resource_path('resources/icons/magnifying-glass-solid.png'))
        canvas = Canvas(top, width=10, height=10, borderwidth=0, highlightthickness=0)
        canvas.create_image(0, 0, image=self._search_img, anchor=NW)
        canvas.pack(side=RIGHT, padx=(0, 4))

        track_canvas = ScrollableTrackCanvas(self, track_list=track_list, search_widget=search_widget)
        track_canvas.pack(side=RIGHT, fill=BOTH, expand=True)
