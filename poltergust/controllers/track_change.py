

from tkinter import Toplevel
from poltergust.controllers.ctlist_controllers import CTListSelectorController
from poltergust.models.ct_storage import MK8CTStorage
from poltergust.models.game_models import MK8Course
from poltergust.models.gamedata import COURSE_IDS
from poltergust.models.mod_models import MK8CustomTrack

from poltergust.views.change_track import PoltergustChangeTrackView
from poltergust.views.ct_list import TrackListSelectorView


class TrackChangeController:
    """ TODO """
    SELECTABLE_TRACKS_SLOTS = filter(lambda track: track.course_id < 64, COURSE_IDS.values())

    def __init__(self, view: PoltergustChangeTrackView):
        super().__init__()
        self._view = view
        self._db = MK8CTStorage()

        self.track = self._view.track_slot
        self.mod = self._view.mod

        self._view.change_ct_button.config(command=self.on_change_ct_button_click)
        self._view.change_track_slot_button.config(command=self.on_change_track_slot_button_click)

    def on_change_track_slot_button_click(self) -> None:
        """ TODO """
        ctselector_view = TrackListSelectorView(self._view, self.SELECTABLE_TRACKS_SLOTS, selected_track=self.track)
        selector_controller = CTListSelectorController(ctselector_view)
        selector_controller.add_listener(self.on_track_slot_changed)

    def on_change_ct_button_click(self) -> None:
        """ TODO """
        ctselector_view = TrackListSelectorView(self._view, self._db.get_mods(), selected_track=self.mod)
        selector_controller = CTListSelectorController(ctselector_view)
        selector_controller.add_listener(self.on_ct_changed)

    def on_track_slot_changed(self, track: MK8Course) -> None:
        """ TODO """
        self.track = track
        self._view.set_track_slot(track)

    def on_ct_changed(self, mod: MK8CustomTrack) -> None:
        """ TODO """
        self.mod = mod
        self._view.set_mod(mod)

    def on_save_button_click(self) -> None:
        """ TODO """
