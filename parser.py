from enum import Enum


class MK8_GHOST_TYPES(Enum):
    STAFF_GHOST = "sg"
    PLAYER_GHOST = "gs"
    DOWNLOADED_GHOST = "dg"
    MKTV_REPLAY = "rp" # Different file format than a ghost

class MK8_UNICODE_HELPER:
    """ TODO """
    master_dict = {
        0x5: "★",
    }
    rev_master_dict = dict(map(reversed, master_dict.items()))

    @classmethod
    def translate(cls, val):
        # Use a questionmark-box if we cannot fetch a translation so we can at least display something
        return cls.master_dict.get(val, "�")

    @classmethod
    def encode(cls, val):
        return cls.rev_master_dict.get(val, 0x0)

class MK8GhostFilenameParser:
    """ TODO """

    def parse_plain(hex):
        return hex

    def parse_hex(hex):
        return int(hex, 16)

    def parse_playername(hex):
        name = ""
        for i in range(0, len(hex), 4):
            val = int(hex[i+2:i+4], 16)
            if val == 0:
                return name
            elif val < 32 or 127 <= val < 160:
                # Unicode control characters; Some have a Nintendo-specific font
                name += MK8_UNICODE_HELPER.translate(val)
            else:
                name += chr(val)
        return name

    base_data = [
        (2, "ghost_type", parse_plain),
        (2, "track_number", parse_hex),
        (2, "track_id", parse_hex),
        (2, "character", parse_hex),
        (4, None, None), # 0000 Padding
        (2, "kart", parse_hex),
        (2, "wheels", parse_hex),
        (2, "glider", parse_hex),
        (1, "total_minutes", parse_hex),
        (2, "total_seconds", parse_hex),
        (3, "total_ms", parse_hex),
        (1, "lap1_minutes", parse_hex),
        (2, "lap1_seconds", parse_hex),
        (3, "lap1_ms", parse_hex),
        (1, "lap2_minutes", parse_hex),
        (2, "lap2_seconds", parse_hex),
        (3, "lap2_ms", parse_hex),
        (1, "lap3_minutes", parse_hex),
        (2, "lap3_seconds", parse_hex),
        (3, "lap3_ms", parse_hex),
    ]

    playerdata = [
        (40, "playername", parse_playername),
        (2, "flag", parse_hex),
        (6, None, None), # 000000 Padding.
    ]

    # Filename pattern for ghost files as of v3 of the game
    filename_length_v3 = 102
    filename_pattern_v3 = base_data + [(12, None, None)] + playerdata # 93b3e793b3e7 Padding

    # Filename pattern for ghost files as of v4 of the game
    filename_length_v4 = filename_length_v3 + 12
    filename_pattern_v4 = base_data + [
            (1, "lap4_minutes", parse_hex), # Just for GCN Baby Park; 9:99.999 if laps don't exist
            (2, "lap4_seconds", parse_hex),
            (3, "lap4_ms", parse_hex),
            (1, "lap5_minutes", parse_hex),
            (2, "lap5_seconds", parse_hex),
            (3, "lap5_ms", parse_hex)
        ] + playerdata + [
            (1, "lap6_minutes", parse_hex), # Just for GCN Baby Park
            (2, "lap6_seconds", parse_hex),
            (3, "lap6_ms", parse_hex),
            (1, "lap7_minutes", parse_hex),
            (2, "lap7_seconds", parse_hex),
            (3, "lap7_ms", parse_hex)
        ]

    def __init__(self, filename):
        self.filename = filename

    def parse(self, use_v4=True):
        filename_len = len(self.filename)
        pattern = self.filename_pattern_v4 if use_v4 else self.filename_pattern_v3

        if filename_len == self.filename_length_v3 and use_v4:
            raise ValueError("Filename was too long for v1-v3 of the game. Did you attempt to parse a filename for v4+ of the game?")
        elif filename_len == self.filename_length_v4 and not use_v4:
            raise ValueError("Filename was too short for v4+ of the game. Did you attempt to parse a filename for v1-v3 of the game?")
        elif filename_len not in [self.filename_length_v3, self.filename_length_v4]:
            raise ValueError(f"Filename was of incorrect length. Expected {self.filename_length_v3} (v1-v3) or {self.filename_length_v4} (v4+), but got {filename_len}")

        i = 0
        results = {}
        for num_chars, identifier, parse_method in pattern:
            if identifier is not None:
                val = self.filename[i:i+num_chars]
                results[identifier] = parse_method(val)
            i += num_chars

        return results

if __name__ == '__main__':
    filename = "sg1121030000130c0012e0630230fd0231950231b993b3e793b3e7004e0069006e26050043006800720069007300006e000000"
    parser = MK8GhostFilenameParser(filename)
    res = parser.parse(use_v4=False)
    print(res)
