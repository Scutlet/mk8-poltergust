from abc import ABC, abstractmethod

from PIL import Image

class MK8ImageAtlasMapper(ABC):
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

    @classmethod
    def index_to_image(cls, index: int | None, resize_to: tuple[int, int] | None = None) -> Image.Image:
        """ Given some index, extracts the icon at that index from the atlas and optionally resizes it """
        with Image.open(cls.image_name) as img:
            x, y, x_offset, y_offset = cls.get_coordinates(index)
            img = img.crop((x, y, x_offset, y_offset))
            if resize_to:
                img = img.resize(resize_to)
        return img

    @classmethod
    def get_coordinates(cls, index: int | None) -> tuple[int, int, int, int]:
        """ Obtains coordinates of the icon at a specific index in the atlas  """
        if index is None or index < 0 or index >= cls.num_icons:
            return (*cls.invalid_coordinates, cls.invalid_coordinates[0] + cls.icon_size[0], cls.invalid_coordinates[1] + cls.icon_size[1])

        column = index % cls.icons_per_row
        row = index // cls.icons_per_row

        x_offset = column*(cls.icon_size[0] + cls.image_xgap) + cls.image_xgap
        y_offset = row*(cls.icon_size[1] + cls.image_ygap) + cls.image_ygap

        return (x_offset + cls.x_offset,
            y_offset + cls.y_offset,
            x_offset + cls.icon_size[0] + cls.x_offset,
            y_offset + cls.icon_size[1] + cls.y_offset
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

    num_icons = 56
    icons_per_row = 8

    invalid_coordinates = (17, 1894)

class MK8VehiclePartImageMapper(MK8ImageAtlasMapper):
    """ Maps indices to MK8 Vehicle Part icons """
    image_name = "resources/mk8d-vehicle-parts.png"
    image_xgap = 1
    image_ygap = 14
    icon_size = (200, 128)

    num_icons = 448
    icons_per_row = 12

    invalid_coordinates = (805, 5268)
