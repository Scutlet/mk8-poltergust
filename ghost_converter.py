import os

from filename_parser import MK8GhostFilenameData, MK8GhostFilenameSerializer
from gamedata import MK8GhostType


class MK8GhostConverter:
    """
        Class that can convert between various Mario Kart 8 Ghost Formats by
        removing or injecting a player ghost header. Staff Ghosts do not have
        this header. Downloaded Ghosts may optionally have this header.

        NOTE: Ghosts downloaded through the Nintendo Clients package do NOT
        have this header. Simply renaming the file already works directly!
    """
    PLAYER_GHOST_HEADER_SIZE = 0x48

    def export_as_staff(self, source_file: str, filename_data: MK8GhostFilenameData, ghost_has_header: bool, output_folder: str) -> str:
        """ Exports a given ghostfile as a staff ghost """
        # Temporarily change ghost type for the serializer
        old_ghost_type = filename_data.ghost_type
        old_ghost_number = filename_data.ghost_number
        filename_data.ghost_type = MK8GhostType.STAFF_GHOST
        # Restore special handling for trackID in case we're converting from a downloaded ghost
        filename_data.ghost_number = filename_data.track_id - 16
        serializer = MK8GhostFilenameSerializer()
        output_filename = serializer.serialize(filename_data)

        # Restore ghost type
        filename_data.ghost_type = old_ghost_type
        filename_data.ghost_number = old_ghost_number

        # Write file
        output_file = os.path.join(output_folder, output_filename)
        self._copy_to_new_file(source_file, output_file, remove_header=ghost_has_header)
        return output_file

    def export_as_downloaded(self, source_file: str, filename_data: MK8GhostFilenameData, ghost_has_header: bool, output_folder: str, ghost_slot: int = 0) -> str:
        """ Exports the currently loaded ghostfile as a downloaded ghost """
        # Temporarily change ghost type for the serializer
        old_ghost_type = filename_data.ghost_type
        old_ghost_number = filename_data.ghost_number
        filename_data.ghost_type = MK8GhostType.DOWNLOADED_GHOST
        filename_data.ghost_number = ghost_slot
        serializer = MK8GhostFilenameSerializer()
        output_filename = serializer.serialize(filename_data)

        # Restore ghost type
        filename_data.ghost_type = old_ghost_type
        filename_data.ghost_number = old_ghost_number

        # Write file
        output_file = os.path.join(output_folder, output_filename)
        self._copy_to_new_file(source_file, output_file, remove_header=ghost_has_header)
        return output_file

    def _copy_to_new_file(self, source_file, output_file, remove_header=True) -> None:
        """
            Copies a ghost into another file, optionally removing its header.
            TODO: Add code to reconstruct the header
        """
        print(f"converting {source_file} to {output_file}")
        # Offset changes if the header needs to be removed.
        copy_offset = 0
        if remove_header:
            copy_offset = self.PLAYER_GHOST_HEADER_SIZE

        # Read current ghost data
        with open(source_file, 'rb') as file:
            file.seek(copy_offset, os.SEEK_SET)
            ghost_data = file.read()

        # Write new file
        with open(output_file, 'wb') as file:
            file.write(ghost_data)
