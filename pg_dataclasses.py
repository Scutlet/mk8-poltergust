from dataclasses import dataclass
from tkinter import Tk
from downloader import GameBananaSite
from imagemapper import MK8TrackImageMapper

from widgets import FramableTrack, MK8TrackFrame


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
class MK8Course(FramableTrack):
    course_id: int
    name: str
    icon_index: int
    cup: MK8Cup

    _sort_field_name = "name"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, MK8Course):
            return self.course_id == other.course_id
        return False

    def frame(self, master: Tk, *args, **kwargs) -> MK8TrackFrame:
        icon_index = self.icon_index
        track_preview = MK8TrackImageMapper().index_to_image(icon_index, resize_to=self.TRACK_PREVIEW_SIZE)

        track_name = self.name
        track_author = self.cup
        url_text = str(self.course_id)
        url_icon = GameBananaSite.icon # TODO
        url_link = "https://www.mariowiki.com/Mario_Kart_8#Courses"
        url_tooltip = f"Super Mario Wiki - {url_link}"

        return MK8TrackFrame(master, track_name, track_author, track_preview, url_text, url_icon, url_link, url_tooltip, *args, **kwargs)
