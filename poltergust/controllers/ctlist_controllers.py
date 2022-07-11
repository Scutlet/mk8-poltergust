from tkinter import Event, Toplevel
from typing import Iterable
from poltergust.controllers.ct_downloader import CTDownloaderController

from poltergust.models.game_models import MK8Course
from poltergust.models.mod_models import MK8CustomTrack
from poltergust.utils import Observable
from poltergust.views.ct_add import PoltergustAddCTView
from poltergust.views.ct_list import PoltergustCTManagerView, TrackListSelectorView
from poltergust.widgets.widgets import FramableTrack


class CTListController:
    """ TODO """

    def __init__(self, view: PoltergustCTManagerView, foo=5):
        self._view = view
        self._view.add_button.config(command=self.on_add_button_click)

    def on_add_button_click(self):
        """ TODO """
        ctdownloader_view = PoltergustAddCTView(self._view)
        downloader = CTDownloaderController(ctdownloader_view)
        downloader.add_listener(self.on_ct_added)

    def on_ct_added(self, mod: MK8CustomTrack) -> None:
        """ TODO """
        self._view.track_canvas.add_track(mod)


class CTListSelectorController(Observable[FramableTrack], CTListController):
    """ TODO """
    def __init__(self, view: TrackListSelectorView):
        super().__init__(view)
        self._view = view
        self._view.select_button.config(command=self.on_track_selection_made)

        self._selected_track = self._view.selected_track

    def on_track_selection_made(self) -> None:
        """ TODO """
        self._view.on_close()

        # Only notify listeners if track selection actually changed
        if self._selected_track != self._view.selected_track:
            self.notify_listeners(self._view.selected_track)
