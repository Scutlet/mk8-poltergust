from dataclasses import dataclass
from typing import ClassVar
from tkinter import Tk

from PIL import Image

from poltergust.models.mod_sites import MK8ModSite
from poltergust.widgets.widgets import FramableTrack, MK8TrackFrame


@dataclass
class MK8ModVersion:
    major: int
    minor: int
    patch: int = 0

    def __str__(self):
        return f"v{self.major}.{self.minor}.{self.patch}"

@dataclass
class MK8CustomTrack(FramableTrack):
    """ Dataclass for a Mario Kart 8 Custom Track """
    name: str
    mod_site: MK8ModSite
    mod_id: int

    author: str|None = None
    preview_image: str|None = None

    # Preview Image size
    PREVIEW_SIZE: ClassVar[tuple[int, int]] = (288, 162)

    _sort_field_name = "name"

    def __str__(self):
        return f"[{self.mod_site}] {self.name}"

    def __eq__(self, other):
        if isinstance(other, MK8CustomTrack):
            return self.mod_id == other.mod_id and self.mod_site == other.mod_site
        return False

    def frame(self, master: Tk, *args, **kwargs) -> MK8TrackFrame:
        track_name = self.name
        track_author = self.author or "Unknown Author"

        track_preview = None
        if self.preview_image is not None:
            try:
                track_preview = Image.open(self.preview_image).resize(size=self.TRACK_PREVIEW_SIZE)
            except FileNotFoundError as e:
                pass

        if track_preview is None:
            track_preview = self.mod_site.icon.resize(size=(24, 24))

        url_text = str(self.mod_id)
        url_icon = self.mod_site.icon
        url_link = self.mod_site.get_url_for_mod_id(self.mod_id)
        url_tooltip = f"{self.mod_site} - {url_link}"

        return MK8TrackFrame(master, track_name, track_author, track_preview, url_text, url_icon, url_link, url_tooltip, *args, **kwargs)
