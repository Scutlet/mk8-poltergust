import binascii
import os


class MK8GhostFilenameDataMiiHandler:
    """ Class that can extract or replace Mii data from Mario Kart 8 ghost files """
    # Mii data offset from the start of a MK8 ghost file
    STAFF_MII_OFFSET = 0x244
    PLAYERGHOST_MII_OFFSET = 0x28c

    # Mii data length
    MII_GHOST_LENGTH = 0x5c
    ZERO_PADDING_LENGTH = 0x02
    CHECKSUM_LENGTH = 0x02

    # Mii Infos
    MII_NAME_OFFSET = 0x1a
    MII_NAME_LENGTH = 0x14

    def __init__(self, ghost_filename: str, has_header=False) -> None:
        self.filename = ghost_filename
        self.has_header = has_header

    def get_mii_offset(self):
        """ Returns the offset of the Mii in the ghost file """
        if self.has_header:
            # We have an additional 0x48 offset at the start of the file
            return self.PLAYERGHOST_MII_OFFSET
        return self.STAFF_MII_OFFSET

    def calculate_ghost_mii_checksum(self, mii_data: bytes) -> bytes:
        """ Calculates the CRC-16 XMODEM checksum of some Mii data (containing two trailing nul-bytes) """
        return binascii.crc_hqx(mii_data, 0x00).to_bytes(2, byteorder='big')

    def get_mii_data(self, strict=True) -> bytes:
        """
            Reads Mii data from the ghostfile. If invalid data is found
            and `strict=True`, an error will be thrown and no data will be exported.
        """
        # Offset depends on whether data was created in-game.
        offset = self.get_mii_offset()
        with open(self.filename, 'rb') as file:
            file.seek(offset, os.SEEK_SET)
            ghost_data = file.read(self.MII_GHOST_LENGTH)
            zeroes = file.read(self.ZERO_PADDING_LENGTH)
            checksum = file.read(self.CHECKSUM_LENGTH)

            # Verify Mii data; File might be invalid if this doesn't match
            if strict:
                # Check for the zero-byte padding. It's not actually used for Mii data though
                if zeroes != b'\x00\x00':
                    raise ValueError("MK8 Ghost Data Mii is missing a zero byte")

                # Verify the checksum of the Mii data is correct
                calculated_checksum = self.calculate_ghost_mii_checksum(ghost_data + zeroes)
                if checksum != calculated_checksum:
                    raise ValueError("MK8 Ghost Data Mii checksum is incorrect")

            return ghost_data

    def extract_mii_name(self) -> str:
        """ Extracts the mii name from the the attached ghost file """
        offset = self.get_mii_offset()
        with open(self.filename, 'rb') as file:
            file.seek(offset + self.MII_NAME_OFFSET, os.SEEK_SET)
            mii_name = file.read(self.MII_NAME_LENGTH)
            mii_name = mii_name.decode('utf-16-le')
            return mii_name

    def extract(self, output_filename: str) -> None:
        """ Extract the Mii from `self.ghost_filename`, and export the result to a given location """
        # Get Mii Data
        data = self.get_mii_data()

        # Write new file
        with open(output_filename, 'wb') as file:
            file.write(data)

    def replace(self, mii_file: str) -> None:
        """ Injects the Mii in `mii_file` into the current ghost file """
        with open(mii_file, 'rb') as file:
            new_mii_data = file.read()
            new_mii_data += b'\x00\x00'

        if self.has_header:
            # TODO: Handling for player ghosts (header CRC should change)
            raise ValueError("Replacing Miis in a ghost file with a header is unsupported at the moment.")

        # Offset depends on whether this is a staff ghost
        offset = self.get_mii_offset()

        with open(self.filename, 'rb+') as file:
            file.seek(offset, os.SEEK_SET)
            file.write(new_mii_data)
            file.write(self.calculate_ghost_mii_checksum(new_mii_data))
