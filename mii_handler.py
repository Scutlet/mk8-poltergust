import binascii
import os


class MK8GhostDataMiiHandler:
    """ Class that can extract or replace Mii data from Mario Kart 8 ghost files """
    # Mii data offset from the start of a MK8 ghost file
    STAFF_MII_OFFSET = 0x244
    PLAYERGHOST_MII_OFFSET = 0x28c

    # Mii data length
    MII_GHOST_LENGTH = 0x5c
    ZERO_PADDING_LENGTH = 0x02
    CHECKSUM_LENGTH = 0x02


    def __init__(self, ghost_filename: str, is_staff_ghost=False) -> None:
        self.filename = ghost_filename
        self.is_staff_ghost = is_staff_ghost

    def get_mii_data(self, strict=True) -> bytes:
        """
            Reads Mii data from the ghostfile. If invalid data is found
            and `strict=True`, an error will be thrown and no data will be exported.
        """
        # Offset depends on whether this is a staff ghost
        offset = self.STAFF_MII_OFFSET if self.is_staff_ghost else self.PLAYERGHOST_MII_OFFSET
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
                calculated_checksum = binascii.crc_hqx(ghost_data + zeroes, 0x00).to_bytes(2, byteorder='big')
                if checksum != calculated_checksum:
                    raise ValueError("MK8 Ghost Data Mii checksum is incorrect")

            return ghost_data

    def extract(self, output_filename: str) -> None:
        """ Extract the Mii from `self.ghost_filename`, and export the result to a given location """
        # Get Mii Data
        data = self.get_mii_data()

        # Write new file
        with open(output_filename, 'wb') as file:
            file.write(data)

