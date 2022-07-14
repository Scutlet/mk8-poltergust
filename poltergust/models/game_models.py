from dataclasses import dataclass
from enum import Enum
from tkinter import Toplevel

from PIL import Image

from poltergust.models.imagemapper import MK8TrackImageMapper
from poltergust.models.mod_sites import GameBananaSite, MarioWikiSite
from poltergust.widgets.widgets import MK8TrackFrameBig, MK8TrackFrameSmall, MiniFramableTrack


class MK8GhostType(Enum):
    """ Enumeration of all types of ghosts in Mario Kart 8 """
    STAFF_GHOST = "sg"
    PLAYER_GHOST = "gs"
    DOWNLOADED_GHOST = "dg"
    MKTV_REPLAY = "rp" # Different file format than a ghost

@dataclass
class MK8DLC:
    name: str

    def __str__(self):
        return self.name

@dataclass
class MK8Cup:
    name: str
    dlc: MK8DLC|None = None

    def __str__(self):
        return self.name

@dataclass
class MK8Course(MiniFramableTrack):
    course_id: int
    name: str
    icon_index: int
    cup: MK8Cup
    url: str

    _sort_field_name = "name"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, MK8Course):
            return self.course_id == other.course_id
        return False

    def _get_frame_kwargs(self, master: Toplevel, preview_size: tuple[int, int]) -> tuple[str, Image.Image]:
        """ TODO """
        icon_index = self.icon_index
        track_preview = MK8TrackImageMapper().index_to_image(icon_index, resize_to=preview_size)

        track_name = self.name
        return track_name, track_preview

    def frame(self, master: Toplevel, *args, **kwargs) -> MK8TrackFrameBig:
        track_name, track_preview = self._get_frame_kwargs(master, MK8TrackFrameBig.TRACK_PREVIEW_SIZE)

        track_author = self.cup
        url_text = str(self.course_id)
        url_icon = MarioWikiSite.icon
        url_link = self.url
        url_tooltip = f"Super Mario Wiki - {url_link}"

        return MK8TrackFrameBig(master, track_name, track_preview, track_author, url_text, url_icon, url_link, url_tooltip, *args, **kwargs)

    def miniframe(self, master: Toplevel, *args, **kwargs) -> MK8TrackFrameSmall:
        track_name, track_preview = self._get_frame_kwargs(master, MK8TrackFrameSmall.TRACK_PREVIEW_SIZE)
        track_name = f"Replaces {track_name}"
        return MK8TrackFrameSmall(master, track_name, track_preview, *args, **kwargs)


UNKNOWN_COURSE = MK8Course(-1, "Unknown Track", -1, MK8Cup("Unknown Cup"), url="https://github.com/Scutlet/mk8-poltergust")
