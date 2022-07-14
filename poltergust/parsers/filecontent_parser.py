from dataclasses import dataclass
import os

from poltergust.models.game_models import MK8Course
from poltergust.models.mod_models import MK8CustomTrack, MK8ModVersion


@dataclass
class MK8GhostData:
    """
        Dataclass containing information present in Mario Kart 8 ghost files.
    """
    track_slot: MK8Course
    # mii_name: str # utf-16-le
    # player_name: str # utf-16-be

    # Poltergust-specific
    mod: MK8CustomTrack|None
    mod_version: MK8ModVersion|None


class MK8GhostDataSerializer:
    """ Serializes information from Mario Kart 8 Ghost Files """
    HEADER_PREFIX = "CTG0"
    HEADER_LENGTH = 0x48

    COURSE_ID_OFFSET = 0x17c # u4

    # Poltergust injects (located just before the Mii data)
    POLTERGUST_MOD_VERSION_OFFSET = 0x234 # u1 u1 u1
    POLTERGUST_MOD_SITE_OFFSET = 0x237 # u1
    POLTERGUST_MOD_ID_OFFSET = 0x238 # u4

    def _has_header(self) -> bool:
        """ Checks whether the player ghost header is present on a file """
        self.f.seek(0, os.SEEK_SET)
        return self.f.read(4) == self.HEADER_PREFIX.encode()

    def get_offset(self, offset_without_header: int) -> int:
        """ TODO """
        if self.has_header:
            return offset_without_header + self.HEADER_LENGTH
        return offset_without_header

    def seek(self, offset: int) -> None:
        """ TODO """
        self.f.seek(self.get_offset(offset), os.SEEK_SET)

    def serialize(self, output_file: str, data: MK8GhostData) -> str:
        """ Serializes ghost data into the file specified at `self.output_file` """
        with open(output_file, 'rb+') as f:
            self.f = f
            self.has_header = self._has_header()

            # Write track slot
            self.seek(self.COURSE_ID_OFFSET)
            course_id = data.track_slot.course_id.to_bytes(4, byteorder='big')
            f.write(course_id)

            # Linking to a mod is optional
            if data.mod is None:
                return

            # Inject mod version (for Poltergust)
            self.seek(self.POLTERGUST_MOD_VERSION_OFFSET)
            mod_version_major = data.mod_version.major.to_bytes(1, byteorder='big')
            f.write(mod_version_major)

            mod_version_minor = data.mod_version.minor.to_bytes(1, byteorder='big')
            f.write(mod_version_minor)

            mod_version_patch = data.mod_version.patch.to_bytes(1, byteorder='big')
            f.write(mod_version_patch)

            # Inject mod site (for Poltergust)
            self.seek(self.POLTERGUST_MOD_SITE_OFFSET)
            mod_site = data.mod.mod_site.id.to_bytes(1, byteorder='big')
            f.write(mod_site)

            # Inject mod_id (for Poltergust)
            self.seek(self.POLTERGUST_MOD_ID_OFFSET)
            mod_id = data.mod.mod_id.to_bytes(4, byteorder='big')
            f.write(mod_id)

            # TODO: Fix header

