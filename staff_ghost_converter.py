import os

from parser import MK8_GHOST_TYPES, MK8GhostData


class MK8StaffGhostConverter:
    """ Class that can convert a normal ghost to a staff ghost """
    GHOST_DATA_OFFSET = 0x48

    def __init__(self, ghost_data: MK8GhostData, ghost_file: str):
        """
            :param ghost_data: Ghost data to convert to a staff ghost.
            :param ghost_file: Ghost replay file to use as a base.
        """
        self.ghost_data = ghost_data
        self.ghost_file = ghost_file

    def convert(self, output_folder):
        """
            Copies `self.ghost_data` into a new file in `output_folder`
            and converts it to a staff ghost
        """
        print(f"converting {output_folder}")
        assert self.ghost_data.ghost_type != MK8_GHOST_TYPES.STAFF_GHOST

        # Read current ghost data
        with open(self.ghost_file, 'rb') as file:
            file.seek(self.GHOST_DATA_OFFSET, os.SEEK_SET)
            ghost_data = file.read()

        # Write new file
        with open(os.path.join(output_folder, "teststaffghost.dat"), 'wb') as file:
            file.write(ghost_data)

        return True
