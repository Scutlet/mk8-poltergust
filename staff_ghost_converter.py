import os

from parser import MK8_GHOST_TYPES, MK8GhostData


class MK8StaffGhostConverter:
    """
        Class that can convert a player ghost or downloaded ghost to a staff ghost
        by removing their header. Staff Ghosts do not have this header.

        NOTE: Ghosts downloaded through the Nintendo Clients package do NOT
        have this header. Simply renaming the file already works directly!
    """
    GHOST_DATA_OFFSET = 0x48

    def __init__(self, ghost_file: str):
        """
            :param ghost_file: Ghost replay file to convert to a staff ghost.
        """
        self.ghost_file = ghost_file

    def convert(self, output_folder, remove_header=True):
        """
            Copies `self.ghost_data` into a new file in `output_folder`
            and converts it to a staff ghost
        """
        print(f"converting {output_folder}")

        # Read current ghost data
        with open(self.ghost_file, 'rb') as file:
            file.seek(self.GHOST_DATA_OFFSET, os.SEEK_SET)
            ghost_data = file.read()

        # Write new file
        with open(output_folder, 'wb') as file:
            file.write(ghost_data)

        return True
