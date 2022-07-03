
class MK8GhostDataParser:
    """ Parser for (staff) ghost data files from Mario Kart 8 (Wii U) """
    HEADER_PREFIX = "CTG0"

    def check_header(self, filepath: str) -> bool:
        with open(filepath, 'rb') as f:
            prefix = f.read(4)
            return prefix == self.HEADER_PREFIX.encode()
