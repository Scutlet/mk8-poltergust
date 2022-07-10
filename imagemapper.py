from abc import ABC
import logging

from PIL import Image

from utils import SingletonABCMeta, get_resource_path


class MK8ImageAtlasMapper(ABC, metaclass=SingletonABCMeta):
    """ Class that can extract a single icon at a specific index from an icon atlas """
    image_name: str = None
    image_xgap: int
    image_ygap: int
    icon_size: tuple[int, int]

    num_icons: int
    icons_per_row: int

    # Image to show if passed an invalid index
    invalid_coordinates: tuple[int, int]

    x_offset: int = 0
    y_offset: int = 0

    # Cached image atlas
    _atlas_cache: Image.Image

    def __init__(self):
        # Load Atlas in memory when initialised
        logging.info(f"{self.__class__.__name__} cached its icon atlas: {self.image_name}.")
        self._atlas_cache = Image.open(get_resource_path(self.image_name))

    def index_to_image(self, index: int | None, resize_to: tuple[int, int] | None = None) -> Image.Image:
        """ Given some index, extracts the icon at that index from the atlas and optionally resizes it """
        x, y, x_offset, y_offset = self.get_coordinates(index)
        img = self._atlas_cache.crop((x, y, x_offset, y_offset))
        if resize_to:
            img = img.resize(resize_to)
        return img

    def get_coordinates(self, index: int | None) -> tuple[int, int, int, int]:
        """ Obtains coordinates of the icon at a specific index in the atlas  """
        if index is None or index < 0 or index >= self.num_icons:
            return (*self.invalid_coordinates, self.invalid_coordinates[0] + self.icon_size[0], self.invalid_coordinates[1] + self.icon_size[1])

        column = index % self.icons_per_row
        row = index // self.icons_per_row

        x_offset = column*(self.icon_size[0] + self.image_xgap) + self.image_xgap
        y_offset = row*(self.icon_size[1] + self.image_ygap) + self.image_ygap

        return (x_offset + self.x_offset,
            y_offset + self.y_offset,
            x_offset + self.icon_size[0] + self.x_offset,
            y_offset + self.icon_size[1] + self.y_offset
        )

class MK8FlagImageMapper(MK8ImageAtlasMapper):
    """ Maps indices to MK8 Country Flags """
    image_name = "resources/mk8-flags.png"
    image_xgap = 5
    image_ygap = 4
    icon_size = (60, 40)

    num_icons = 71
    icons_per_row = 10

    invalid_coordinates = (590, 312)

class MK8CharacterImageMapper(MK8ImageAtlasMapper):
    """ Maps indices to MK8 Character icons """
    image_name = "resources/mk8d-characters.png"
    image_xgap = 1
    image_ygap = 1
    icon_size = (128, 128)

    num_icons = 65
    icons_per_row = 12

    invalid_coordinates = (646, 646)

class MK8TrackImageMapper(MK8ImageAtlasMapper):
    """ Maps indices to MK8 Track icons """
    image_name = "resources/mk8d-course-previews.png"
    image_xgap = 17
    image_ygap = 95
    icon_size = (288, 162)

    num_icons = 64
    icons_per_row = 8

    invalid_coordinates = (17, 2151)

class MK8VehiclePartImageMapper(MK8ImageAtlasMapper):
    """ Maps indices to MK8 Vehicle Part icons """
    image_name = "resources/mk8d-vehicle-parts.png"
    image_xgap = 1
    image_ygap = 14
    icon_size = (200, 128)

    num_icons = 448
    icons_per_row = 12

    invalid_coordinates = (805, 5268)
