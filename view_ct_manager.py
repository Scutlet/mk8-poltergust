import bisect
from idlelib.tooltip import Hovertip
from tkinter import *
from tkinter import ttk
from tkinter.font import Font, ITALIC
import webbrowser

from PIL import Image, ImageTk

from downloader import MK8CustomTrack, MOD_SITES
from utils import PoltergustBlockingPopup, WrappingLabel, get_resource_path
from widgets import IconButton, MK8CustomTrackFrame


class PoltergustCTManagerView(PoltergustBlockingPopup):
    """
        Displays a window of all cached CTs.
    """
    window_title = "Poltergust - Custom Track Database"
    window_width = 310
    window_height = 400

    BASE_FONT = "TkDefaultFont"

    # Add mod sites
    mod_site_choices = {site.name: site for site in MOD_SITES}

    def __init__(self, master: Tk, track_list: list[MK8CustomTrack], *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.ITALICS_FONT = Font(font=self.BASE_FONT)
        self.ITALICS_FONT.config(slant=ITALIC)

        # Cache mod site icons so they're not garbage collected
        self._mod_site_image_cache = [ImageTk.PhotoImage(site.icon) for site in MOD_SITES]

        # Top frame
        top = Frame(self)
        top.pack(padx=5, pady=6, fill=X)

        # Add CT Box
        self.add_button = IconButton(top, text="Add a mod", image_path='resources/icons/plus-solid.png')
        self.add_button.pack(side=LEFT)

        # Search Box
        self.search_value = StringVar()
        self.search_value.trace_add("write", lambda var, index, mode: self.reload_list())
        ttk.Entry(top, width=25, textvariable=self.search_value).pack(side=RIGHT)

        # Search Icon
        self._search_img = PhotoImage(file=get_resource_path('resources/icons/magnifying-glass-solid.png'))
        canvas = Canvas(top, width=10, height=10, borderwidth=0, highlightthickness=0)
        canvas.create_image(0, 0, image=self._search_img, anchor=NW)
        canvas.pack(side=RIGHT, padx=(0, 4))

        # Only canvas elements are scrollable
        self.canvas = Canvas(self, bd=0, borderwidth=0, highlightthickness=0)
        vsb = Scrollbar(self, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)

        # Scrollbar
        vsb.pack(side=RIGHT, fill=Y)
        self.vsb = vsb
        self.canvas.pack(side=RIGHT, fill=BOTH, expand=True)

        # Track List
        self.track_frame = ttk.Frame(self.canvas)
        self.track_frame.pack()
        self._track_previews = []

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
            track_widgets.append((track, MK8CustomTrackFrame(self.track_frame, track)))
        return track_widgets

    def reload_list(self) -> None:
        """ TODO """
        search_value = self.search_value.get().lower()
        for track, widget in self.track_widgets:
            widget.pack_forget()
            if not search_value or search_value in track.name.lower():
                widget.pack(fill='both', padx=(2, 5), pady=(0, 5))

    def add_mod(self, mod: MK8CustomTrack) -> None:
        """ Adds a mod to the view """
        # Remove existing mod from the list if the mod_id matches
        indx = None
        for i, (existing_mod, widget) in enumerate(self.track_widgets):
            if mod.mod_site.id == existing_mod.mod_site.id and mod.mod_id == existing_mod.mod_id:
                indx = i
                widget.destroy()
                break
        if indx is not None:
            del self.track_widgets[indx]

        # Insert into sorted list
        mod_widget = MK8CustomTrackFrame(self.track_frame, mod)
        bisect.insort(self.track_widgets, (mod, mod_widget), key=lambda pair: pair[0].name)
        self.reload_list()
