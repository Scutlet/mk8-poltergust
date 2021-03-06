import logging
import math
from tkinter import *
from tkinter import ttk
from typing import Iterable

from PIL import Image, ImageTk, ImageDraw

from poltergust.utils import PoltergustBlockingPopup, bind_tree, get_resource_path
from poltergust.widgets.lists import ScrollableTrackCanvas
from poltergust.widgets.misc import IconButton
from poltergust.widgets.trackframes import FramableTrack, MK8TrackFrameBig


class TrackListView(PoltergustBlockingPopup):
    """
        Displays a window of all cached CTs.
    """
    window_title = "Poltergust - Custom Track Database"
    window_width = 310
    window_height = 400

    def __init__(self, master: Toplevel, track_list: Iterable[FramableTrack], *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Top frame
        self._top_frame = Frame(self)
        self._top_frame.pack(padx=5, pady=6, fill=X)

        # Search Box
        search_widget = ttk.Entry(self._top_frame, width=25)
        search_widget.pack(side=RIGHT)

        # Search Icon
        self._search_img = PhotoImage(file=get_resource_path('resources/icons/magnifying-glass-solid.png'))
        canvas = Canvas(self._top_frame, width=10, height=10, borderwidth=0, highlightthickness=0)
        canvas.create_image(0, 0, image=self._search_img, anchor=NW)
        canvas.pack(side=RIGHT, padx=(0, 4))

        track_list_frame = Frame(self)
        track_list_frame.pack(fill=BOTH, expand=True)

        self.track_canvas = ScrollableTrackCanvas(track_list_frame, track_list=track_list, search_widget=search_widget, scrollable_region=self)
        self.track_canvas.pack(side=RIGHT, fill=BOTH, expand=True)

class TrackListManagerView(TrackListView):
    """ Displays a window of all cached custom tracks, and allows invoking the downloader. """
    def __init__(self, master: Toplevel, track_list: Iterable[FramableTrack], *args, **kwargs):
        super().__init__(master, track_list, *args, **kwargs)

        # Add CT Box
        self.add_button = IconButton(self._top_frame, text="Add a mod", image_path='resources/icons/plus-solid.png')
        self.add_button.pack(side=LEFT)

class TrackListSelectorView(TrackListView):
    """ Allows selecting a track from a list of FramableTracks """
    window_title = "Poltergust - Select Track"

    # SELECTION_COLOR = "light steel blue"
    SELECTION_COLOR = "light green"
    HOVER_COLOR = "lightblue"

    def __init__(self, master: Toplevel, *args, selected_track: FramableTrack|None=None, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.selected_track: FramableTrack|None = None
        self.selected_widget: MK8TrackFrameBig|None = None

        # Confirm button (disabled until a selection is made)
        self.select_button = Button(self, text="Confirm Selection", state=DISABLED)
        self.select_button.pack(side=BOTTOM, pady=(4, 4))
        self.bind('<Return>', lambda e: self.select_button.invoke())

        # Selection images
        self._selected_rect_img = self._get_polygon_as_image(MK8TrackFrameBig.TRACK_PREVIEW_SIZE, [
                (0, 0), (MK8TrackFrameBig.TRACK_PREVIEW_SIZE[0], 0), MK8TrackFrameBig.TRACK_PREVIEW_SIZE, (0, MK8TrackFrameBig.TRACK_PREVIEW_SIZE[1])
            ], "light green", alpha=150)
        self._selected_check_img = self._get_polygon_as_image((48, 48), [
                # (10, 28), (0, 18), (4, 14), (10, 20), (27, 3), (31, 7) -> (32 x 32)
                (15, 42), (0, 27), (6, 21), (15, 30), (41, 5), (47, 11)
            ], fill="green", alpha=175)
        self._selected_rect_draw = None
        self._selected_check_draw = None

        self._attach_selectors(selected_track)

    def attach_selectors_to_widget(self, track: FramableTrack, widget: MK8TrackFrameBig):
        """ Makes sure a FramableTrack and its corresponding widget can be clicked and hovered """
        bind_tree(widget, "<Button-1>",
            lambda e, track=track, widget=widget: self.on_track_select(e, track, widget)
        )
        # Binding to the frame itself is enough
        widget.bind("<Enter>",
            lambda e, track=track, widget=widget: self.activate_hover(e, track, widget)
        )
        widget.bind("<Leave>",
            lambda e, track=track, widget=widget: self.deactivate_hover(e, track, widget)
        )

    def _attach_selectors(self, selected_track: FramableTrack) -> None:
        """ Attaches the selectors to all the tracks/widgets of the view """
        for framable, widget in self.track_canvas.track_widgets:
            self.attach_selectors_to_widget(framable, widget)

            if framable == selected_track:
                self.on_track_select(None, selected_track, widget)

    def _get_polygon_as_image(self, size: tuple[int, int], points: list[int], fill="", outline="", alpha=255):
        """ Builds a polygon from a list of points and outputs it as an image. """
        if fill:
            fill = self.winfo_rgb(fill)
            fill = (math.floor(fill[0]/255), math.floor(fill[1]/255), math.floor(fill[2]/255))
            fill = fill + (alpha,)
        image = Image.new('RGBA', size, None)
        ImageDraw.Draw(image).polygon(points, fill=fill or None, outline=outline or None)
        return ImageTk.PhotoImage(image)

    def on_track_select(self, e: Event, track: FramableTrack, widget: MK8TrackFrameBig):
        """ Update the view when a different track is selected. """
        # Already selected
        if self.selected_track == track:
            return

        # Selected a track
        self.select_button.config(state=NORMAL)

        # Clear previous selection highlight
        if self.selected_widget is not None:
            self.selected_widget.set_color(None)
            self.selected_widget.canvas.delete(self._selected_rect_draw)
            self.selected_widget.canvas.delete(self._selected_check_draw)

        # Set and highlight selection
        self.selected_track = track
        self.selected_widget = widget
        widget.set_color(self.SELECTION_COLOR)

        # Highlight track preview
        self._selected_rect_draw = self.selected_widget.canvas.create_image(0, 0, image=self._selected_rect_img, anchor=NW)
        self._selected_check_draw = self.selected_widget.canvas.create_image(
            self.selected_widget.TRACK_PREVIEW_SIZE[0]/2, self.selected_widget.TRACK_PREVIEW_SIZE[1]/2,
            image=self._selected_check_img, anchor=CENTER
        )

        logging.info(f"Track selection changed to {track.sort_field}")

    def activate_hover(self, e: Event, track: FramableTrack, widget: MK8TrackFrameBig):
        """ Activate styling when the user hovers over the given track/widget """
        # Set highlight color
        if self.selected_track != track:
            widget.set_color(self.HOVER_COLOR)

    def deactivate_hover(self, e: Event, track: FramableTrack, widget: MK8TrackFrameBig):
        """ Deactivates styling when the user stops hovering over the given track/widget """
        # Clear highlight color
        if self.selected_track != track:
            widget.set_color(None)

class TrackListSelectorDownloaderView(TrackListManagerView, TrackListSelectorView):
    """ Allows selecting a track from a list of FramableTracks, and includes a button to access the downloader. """
