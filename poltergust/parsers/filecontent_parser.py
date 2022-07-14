from abc import ABC
from dataclasses import dataclass
import os
from poltergust.models.ct_storage import MK8CTStorage

from poltergust.models.game_models import MK8Course
from poltergust.models.gamedata import COURSE_IDS
from poltergust.models.mod_models import MK8CustomTrack, MK8ModVersion
from poltergust.models.mod_sites import API_MOD_SITES


@dataclass
class MK8GhostData:
    """
        Dataclass containing information present in Mario Kart 8 ghost files.
    """
    has_header: bool
    track_slot: MK8Course
    # mii_name: str # utf-16-le
    # player_name: str # utf-16-be

    # Poltergust-specific
    mod: MK8CustomTrack|None
    mod_version: MK8ModVersion|None

class MK8GhostDataOffsetInfos(ABC):
    """ TODO """
    HEADER_PREFIX = "CTG0"
    HEADER_LENGTH = 0x48

    COURSE_ID_OFFSET = 0x17c # u4

    # Poltergust injects (located just before the Mii data)
    POLTERGUST_MOD_VERSION_OFFSET = 0x234 # u1 u1 u1
    POLTERGUST_MOD_SITE_OFFSET = 0x237 # u1
    POLTERGUST_MOD_ID_OFFSET = 0x238 # u4

    def _has_header(self) -> bool:
        """ Checks whether the player ghost header is present on a file. Requires `self.f to be set` """
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

class MK8GhostDataParser(MK8GhostDataOffsetInfos):
    """ Parses information from Mario Kart 8 Ghost Files """
    def parse(self, input_file: str) -> MK8GhostData:
        """ Parses ghost data from the given file """
        with open(input_file, 'rb') as f:
            self.f = f
            self.has_header = self._has_header()

            track_slot = None
            mod = None
            mod_version = None

            # Read track slot
            self.seek(self.COURSE_ID_OFFSET)
            course_id = f.read(4)
            course_id = int.from_bytes(course_id, byteorder='big')

            track_slot = COURSE_IDS.get(course_id, None)

            if track_slot is None:
                raise ValueError(f"Found invalid track slot in ghost file: {course_id}")

            # Parse mod_id (Poltergust injection)
            self.seek(self.POLTERGUST_MOD_ID_OFFSET)
            mod_id = f.read(4)
            mod_id = int.from_bytes(mod_id, byteorder='big')

            if mod_id != 0:
                # Parse mod version (Poltergust injection)
                self.seek(self.POLTERGUST_MOD_VERSION_OFFSET)
                mod_version_major = f.read(1)
                mod_version_major = int.from_bytes(mod_version_major, byteorder='big')

                mod_version_minor = f.read(1)
                mod_version_minor = int.from_bytes(mod_version_minor, byteorder='big')

                mod_version_patch = f.read(1)
                mod_version_patch = int.from_bytes(mod_version_patch, byteorder='big')

                mod_version = MK8ModVersion(mod_version_major, mod_version_minor, mod_version_patch)

                # Parse mod site (Poltergust injection)
                self.seek(self.POLTERGUST_MOD_SITE_OFFSET)
                mod_site_id = f.read(1)
                mod_site_id = int.from_bytes(mod_site_id, byteorder='big')
                print(mod_site_id)

                mod_site = API_MOD_SITES[mod_site_id]

                db = MK8CTStorage()
                mod = db.find_mod(mod_id, mod_site)
                if mod is None:
                    # Not found in database
                    # TODO; Download data
                    pass

            return MK8GhostData(self.has_header, track_slot, mod, mod_version)

class MK8GhostDataSerializer(MK8GhostDataOffsetInfos):
    """ Serializes information from Mario Kart 8 Ghost Files """

    def serialize(self, output_file: str, data: MK8GhostData) -> str:
        """ Serializes ghost data into the given file """
        with open(output_file, 'rb+') as f:
            self.f = f
            self.has_header = self._has_header()

            # Write track slot
            self.seek(self.COURSE_ID_OFFSET)
            course_id = data.track_slot.course_id.to_bytes(4, byteorder='big')
            f.write(course_id)

            # Linking to a mod is optional
            if data.mod is None:
                # Clean up
                self.seek(self.POLTERGUST_MOD_VERSION_OFFSET)
                f.write(int(0).to_bytes(3, byteorder='big'))

                self.seek(self.POLTERGUST_MOD_SITE_OFFSET)
                f.write(int(0).to_bytes(1, byteorder='big'))

                self.seek(self.POLTERGUST_MOD_ID_OFFSET)
                f.write(int(0).to_bytes(4, byteorder='big'))
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
