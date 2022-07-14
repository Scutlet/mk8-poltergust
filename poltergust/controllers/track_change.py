

from tkinter import Toplevel, messagebox
from poltergust.controllers.ctlist_controllers import CTListSelectorController
from poltergust.models.ct_storage import MK8CTStorage
from poltergust.models.game_models import MK8Course
from poltergust.models.gamedata import COURSE_IDS
from poltergust.models.mod_models import MK8CustomTrack, MK8ModVersion
from poltergust.utils import Observable

from poltergust.views.change_track import PoltergustChangeTrackView
from poltergust.views.ct_list import TrackListSelectorView


class TrackChangeController(Observable[tuple[MK8Course, MK8CustomTrack, MK8ModVersion]]):
    """ TODO """
    SELECTABLE_TRACKS_SLOTS = list(filter(lambda track: track.course_id < 64, COURSE_IDS.values()))

    def __init__(self, view: PoltergustChangeTrackView):
        super().__init__()
        self._view = view
        self._db = MK8CTStorage()

        self.track = self._view.track_slot
        self.mod = self._view.mod
        self.mod_version = MK8ModVersion(self._view.ct_version_major.get(), self._view.ct_version_minor.get(), self._view.ct_version_patch.get())

        self._view.change_ct_button.config(command=self.on_change_ct_button_click)
        self._view.clear_ct_button.config(command=self.on_clear_ct_button_click)
        self._view.change_track_slot_button.config(command=self.on_change_track_slot_button_click)
        self._view.save_button.config(command=self.on_save_button_click)

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

    def on_clear_ct_button_click(self) -> None:
        """ TODO """
        self.on_ct_changed(None)

    def on_track_slot_changed(self, track: MK8Course) -> None:
        """ TODO """
        self.track = track
        self._view.set_track_slot(track)

    def on_ct_changed(self, mod: MK8CustomTrack) -> None:
        """ TODO """
        self.mod = mod
        self.mod_version.major = 1
        self.mod_version.minor = 0
        self.mod_version.patch = 0
        self._view.set_mod_version(self.mod_version)
        self._view.set_mod(mod)

    def on_save_button_click(self) -> None:
        """ TODO """
        self.mod_version.major = self._view.ct_version_major.get()
        self.mod_version.minor = self._view.ct_version_minor.get()
        self.mod_version.patch = self._view.ct_version_patch.get()

        extra_str = "* Custom Track: None\n"
        if self.mod is not None:
            extra_str = "* Custom Track: {self.mod.name}\n* Version {self.mod_version}\n"

        is_ok = messagebox.askokcancel("Overwrite Warning", f"The currently loaded ghostfile will be overwritten with the following information:\n* Track Slot: {self.track}\n{extra_str}\nThis operation cannot be undone. Is this okay?", parent=self._view)

        if is_ok:
            self.notify_listeners((self.track, self.mod, self.mod_version))
            self._view.on_close()
