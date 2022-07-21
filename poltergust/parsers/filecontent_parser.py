from abc import ABC
import binascii
from dataclasses import dataclass
import logging
import os
from tkinter import messagebox
from poltergust.models.ct_storage import MK8CTStorage

from poltergust.models.game_models import MK8Course
from poltergust.models.gamedata import COURSE_IDS
from poltergust.models.mod_models import UNKNOWN_CUSTOM_TRACK, MK8CustomTrack, MK8ModVersion
from poltergust.models.mod_sites import API_MOD_SITES, ModDownloadException
from poltergust.parsers.downloader import PoltergustDownloader


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
    """ Offets for information embedded in ghost files """
    HEADER_PREFIX = "CTG0" # Identifier of the player ghost header
    HEADER_LENGTH = 0x48
    CRC32_OFFSET = 0x38

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
        """ Gets the correct offset, based on whether the player ghost header is present """
        if self.has_header:
            return offset_without_header + self.HEADER_LENGTH
        return offset_without_header

    def seek(self, offset: int) -> None:
        """ Shortcut to seek at an offset relative to the player ghost header """
        self.f.seek(self.get_offset(offset), os.SEEK_SET)

class MK8GhostDataParser(MK8GhostDataOffsetInfos):
    """ Parses information from Mario Kart 8 Ghost Files """
    def _download_modinfos(self, mod_id: int, mod_site_id: int) -> MK8CustomTrack|None:
        """ Downloads a the info of a mod from a given site with a given id """
        try:
            mod_site = API_MOD_SITES[mod_site_id]

            mod_site.mod_id_url

            downloader = PoltergustDownloader()
            db = MK8CTStorage()

            mod = downloader.download(mod_site, str(mod_id))
            if mod.preview_image is not None:
                # Download image
                preview_path = db.MOD_PREVIEW_PATH % {'mod_id': mod_id, 'mod_site_id': mod_site_id}
                downloader.download_preview_image(mod.preview_image, preview_path)
                mod.preview_image = preview_path

            # Add downloaded info to the db
            db.add_or_update_mod(mod)
            db.commit()
            messagebox.showinfo("Download Complete!", f"Mod information was downloaded successfully!\nName: {mod.name}\nAuthor(s): {mod.author}\nSite: {mod.mod_site}")
            return mod
        except ModDownloadException as e:
            logging.error(e)
            messagebox.showerror("Download Error!", str(e))
        return None

    def _get_mod_infos_for_id(self, mod_id: int) -> tuple[MK8CustomTrack, MK8ModVersion]|tuple[None, None]:
        """ Gets info of a mod for a given id """
        # Parse mod version (Poltergust injection)
        self.seek(self.POLTERGUST_MOD_VERSION_OFFSET)
        mod_version_major = self.f.read(1)
        mod_version_major = int.from_bytes(mod_version_major, byteorder='big')

        mod_version_minor = self.f.read(1)
        mod_version_minor = int.from_bytes(mod_version_minor, byteorder='big')

        mod_version_patch = self.f.read(1)
        mod_version_patch = int.from_bytes(mod_version_patch, byteorder='big')

        mod_version = MK8ModVersion(mod_version_major, mod_version_minor, mod_version_patch)

        # Parse mod site (Poltergust injection)
        self.seek(self.POLTERGUST_MOD_SITE_OFFSET)
        mod_site_id = self.f.read(1)
        mod_site_id = int.from_bytes(mod_site_id, byteorder='big')

        if mod_site_id < 0 or mod_site_id >= len(API_MOD_SITES):
            # Invalid data
            messagebox.showerror("Ghost data corrupted!", f"Found unknown mod site {mod_site_id}! This does not break the ghost, and likely means something went wrong internally in Poltergust.")
            return None

        db = MK8CTStorage()
        mod = db.find_mod(mod_id, mod_site_id)
        if mod is None:
            # Not found in database
            should_download = messagebox.askyesno("Download Custom Track Info?", "This ghost file is associated with a custom track. Would you like to download this track's information?\n\nNote: An internet connection is required.")
            if should_download:
                mod = self._download_modinfos(mod_id, mod_site_id)
            else:
                mod = UNKNOWN_CUSTOM_TRACK
                mod.mod_site = API_MOD_SITES[mod_site_id]
                mod.mod_id = mod_id
        return mod, mod_version


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
                mod, mod_version = self._get_mod_infos_for_id(mod_id)

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

            if self.has_header:
                # Need to fix the CRC-32
                crc = self.calculate_crc()

                logging.info("Recalculating CRC-32 for player ghost header.")
                self.f.seek(self.CRC32_OFFSET, os.SEEK_SET)
                self.f.write(crc)

    def calculate_crc(self):
        """ Calculate the CRC-32 over everything after the header """
        # Read everything after the header
        self.seek(0)

        return binascii.crc32(self.f.read()).to_bytes(4, byteorder='big')




