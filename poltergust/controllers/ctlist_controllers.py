from poltergust.controllers.ct_downloader import CTDownloaderController

from poltergust.utils import Observable
from poltergust.views.ct_add import PoltergustAddCTView
from poltergust.views.ct_list import TrackListManagerView, TrackListSelectorDownloaderView, TrackListView, TrackListSelectorView
from poltergust.widgets.widgets import FramableTrack, MK8TrackFrameBig


class CTListController:
    """ TODO """

    def __init__(self, view: TrackListView):
        self._view = view

    def on_ct_added(self, track: FramableTrack) -> MK8TrackFrameBig:
        """ Adds a Framabletrack """
        return self._view.track_canvas.add_track(track)

class CTListDownloaderController(CTListController):
    """ TODO """
    def __init__(self, view: TrackListManagerView):
        super().__init__(view)
        self._view: TrackListManagerView
        self._view.add_button.config(command=self.on_add_button_click)

    def on_add_button_click(self):
        """ TODO """
        ctdownloader_view = PoltergustAddCTView(self._view)
        downloader = CTDownloaderController(ctdownloader_view)
        downloader.add_listener(self.on_ct_added)

class CTListSelectorController(Observable[FramableTrack], CTListController):
    """ TODO """
    def __init__(self, view: TrackListSelectorView):
        super().__init__(view)
        self._view: TrackListSelectorView
        self._view.select_button.config(command=self.on_track_selection_made)

        self._selected_track = self._view.selected_track

    def on_track_selection_made(self) -> None:
        """ TODO """
        self._view.on_close()

        # Only notify listeners if track selection actually changed
        if self._selected_track != self._view.selected_track:
            self.notify_listeners(self._view.selected_track)

class CTListSelectorDownloaderController(CTListDownloaderController, CTListSelectorController):
    """ TODO """
    def __init__(self, view: TrackListSelectorView):
        super().__init__(view)
        self._view: TrackListSelectorDownloaderView

    def on_ct_added(self, track: FramableTrack) -> None:
        widget  = super().on_ct_added(track)
        self._view.attach_selectors_to_widget(track, widget)
