from dataclasses import dataclass
from typing import ClassVar
from tkinter import Toplevel

from PIL import Image

from poltergust.models.mod_sites import MK8APIModSite, MK8ModSite
from poltergust.utils import get_resource_path
from poltergust.widgets.trackframes import FramableTrack, MK8TrackFrameBig


@dataclass
class MK8ModVersion:
    major: int
    minor: int
    patch: int = 0

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

@dataclass
class MK8CustomTrack(FramableTrack):
    """ Dataclass for a Mario Kart 8 Custom Track """
    name: str
    mod_site: MK8APIModSite
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

    def _get_frame_args(self, image_size: tuple[int, int]) -> tuple[str, str, Image.Image]:
        """ Gets a tuple of the custom track's name, author, and preview image """
        track_name = self.name
        track_author = self.author or "Unknown Author"

        track_preview = None
        if self.preview_image is not None:
            try:
                track_preview = Image.open(self.preview_image).resize(size=image_size)
            except FileNotFoundError as e:
                pass

        if track_preview is None:
            size = min(*image_size) / 2
            track_preview = self.mod_site.icon.resize(size=(size, size))

        return track_name, track_author, track_preview

    def frame(self, master: Toplevel, *args, **kwargs) -> MK8TrackFrameBig:
        track_name = self.name
        track_author = self.author or "Unknown Author"

        track_preview = None
        if self.preview_image is not None:
            try:
                track_preview = Image.open(self.preview_image).resize(size=MK8TrackFrameBig.TRACK_PREVIEW_SIZE)
            except FileNotFoundError as e:
                pass

        if track_preview is None:
            size = min(*MK8TrackFrameBig.TRACK_PREVIEW_SIZE) // 2
            track_preview = self.mod_site.icon.resize(size=(size, size))

        url_text = str(self.mod_id)
        url_icon = self.mod_site.icon
        url_link = self.mod_site.get_url_for_mod_id(self.mod_id)
        url_tooltip = f"{self.mod_site} - {url_link}"

        return MK8TrackFrameBig(master, track_name, track_preview, track_author, url_text, url_icon, url_link, url_tooltip, *args, **kwargs)

UNKNOWN_CUSTOM_TRACK = MK8CustomTrack("Unknown Custom Track", None, -1, None, get_resource_path("resources/unknown-track.png"))
