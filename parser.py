from enum import Enum
from dataclasses import dataclass


class MK8_GHOST_TYPES(Enum):
    """ Enumeration of all types of ghosts in Mario Kart 8 """
    STAFF_GHOST = "sg"
    PLAYER_GHOST = "gs"
    DOWNLOADED_GHOST = "dg"
    MKTV_REPLAY = "rp" # Different file format than a ghost

@dataclass
class MK8GhostData:
    """
        Dataclass containing all information present in the filename of a Mario Kart 8 ghost file.
        Includes additional information on game version, and whether the data
        was created in-game (player ghost, or downloaded in-game).
    """
    game_version: str
    created_in_game: bool # False for Staff Ghosts and ghosts downloaded through the Nintendo Clients package

    ghost_type: MK8_GHOST_TYPES
    playername: str
    flag_id: int
    ghost_number: int
    track_id: int
    character_id: int
    character_variant_id: int
    mii_weight_class_id: int
    kart_id: int
    wheels_id: int
    glider_id: int
    total_minutes: int
    total_seconds: int
    total_ms: int

    # Lap times
    lap1_minutes: int
    lap1_seconds: int
    lap1_ms: int
    lap2_minutes: int
    lap2_seconds: int
    lap2_ms: int
    lap3_minutes: int
    lap3_seconds: int
    lap3_ms: int
    lap4_minutes: int | None = None
    lap4_seconds: int | None = None
    lap4_ms: int | None = None
    lap5_minutes: int | None = None
    lap5_seconds: int | None = None
    lap5_ms: int | None = None
    lap6_minutes: int | None = None
    lap6_seconds:  int | None = None
    lap6_ms:  int | None = None
    lap7_minutes:  int | None = None
    lap7_seconds:  int | None = None
    lap7_ms:  int | None = None


class MK8_UNICODE_HELPER:
    """ Allows translation between Mario Kart 8-specific characters and unicode """
    master_dict = {
        0x5: "★",
    }
    rev_master_dict = dict(map(reversed, master_dict.items()))

    @classmethod
    def translate(cls, val):
        # Use a questionmark-box if we cannot fetch a translation so we can at least display something
        return cls.master_dict.get(val, "�")

    @classmethod
    def encode(cls, val, default):
        return cls.rev_master_dict.get(val, default)

    @classmethod
    def parse(cls, hex: str, left=False) -> str:
        """ Parses a string as a hexadecimal number and converts those in their corresponding unicode characters """
        name = ""
        for i in range(0, len(hex), 4):
            hex_val = hex[i:i+2] if left else hex[i+2:i+4]
            val = int(hex_val, 16)
            if val == 0:
                # End of playername reached
                return name
            elif val < 32 or 127 <= val < 160:
                # Unicode control characters; Some have a Nintendo-specific font
                name += cls.translate(val)
            else:
                # Standard character found
                name += chr(val)
        return name

    @classmethod
    def serialize(cls, name: str) -> str:
        """ Serializes a string into hexadecimal ASCII format """
        assert 0 < len(name) <= 10
        ascii_name = ""
        for char in name:
            char = ord(char)
            char = cls.encode(char, f"{char:0x}")
            ascii_name += str(char).zfill(4)
        ascii_name = ascii_name.ljust(10*4, "0")
        return ascii_name

class MK8GhostFilenameParser:
    """ Class that is able to extract information from Mario Kart 8 ghost files """

    def parse_ghosttype(val: str) -> MK8_GHOST_TYPES:
        """ Translates a string to its corresponding ghost type  """
        if val == "sg":
            return MK8_GHOST_TYPES.STAFF_GHOST
        elif val == "gs":
            return MK8_GHOST_TYPES.PLAYER_GHOST
        elif val == "dg":
            return MK8_GHOST_TYPES.DOWNLOADED_GHOST
        return MK8_GHOST_TYPES.MKTV_REPLAY

    def serialize_ghosttype(val: MK8_GHOST_TYPES) -> str:
        """ Seralizes a ghost type into a string """
        return val.value

    def parse_plain(val: str) -> str:
        """ identify function """
        return val

    def parse_hex(hex: str) -> int:
        """ Interprets a string as a hexadecimal number """
        return int(hex, 16)

    def serialize_hex(hex: int) -> str:
        """ Serializes an integer into a hexadecimal number in string form """
        return f"{hex:0x}"



    # Data present in ghost files of all game versions
    base_data = [
        (2, "ghost_type", parse_ghosttype, serialize_ghosttype),
        (2, "ghost_number", parse_hex, serialize_hex),
        (2, "track_id", parse_hex, serialize_hex),
        (2, "character_id", parse_hex, serialize_hex),
        (2, "character_variant_id", parse_hex, serialize_hex),
        (2, "mii_weight_class_id", parse_hex, serialize_hex),
        (2, "kart_id", parse_hex, serialize_hex),
        (2, "wheels_id", parse_hex, serialize_hex),
        (2, "glider_id", parse_hex, serialize_hex),
        (1, "total_minutes", parse_hex, serialize_hex),
        (2, "total_seconds", parse_hex, serialize_hex),
        (3, "total_ms", parse_hex, serialize_hex),
        (1, "lap1_minutes", parse_hex, serialize_hex),
        (2, "lap1_seconds", parse_hex, serialize_hex),
        (3, "lap1_ms", parse_hex, serialize_hex),
        (1, "lap2_minutes", parse_hex, serialize_hex),
        (2, "lap2_seconds", parse_hex, serialize_hex),
        (3, "lap2_ms", parse_hex, serialize_hex),
        (1, "lap3_minutes", parse_hex, serialize_hex),
        (2, "lap3_seconds", parse_hex, serialize_hex),
        (3, "lap3_ms", parse_hex, serialize_hex),
    ]

    # Data for a player present in ghost data for all game versions
    playerdata = [
        (40, "playername", MK8_UNICODE_HELPER.parse, MK8_UNICODE_HELPER.serialize),
        (2, "flag_id", parse_hex, serialize_hex),
        (6, None, None, None), # 000000 Padding.
    ]

    # Filename pattern for ghost files as of v3 of the game
    filename_length_v3 = 102
    filename_pattern_v3 = base_data + [(12, "_padding", None, lambda v: "93b3e793b3e7")] + playerdata # 93b3e793b3e7 Padding

    # Filename pattern for ghost files as of v4 of the game
    filename_length_v4 = filename_length_v3 + 12
    filename_pattern_v4 = base_data + [
            (1, "lap4_minutes", parse_hex, serialize_hex), # Just for GCN Baby Park; 9:99.999 if laps don't exist
            (2, "lap4_seconds", parse_hex, serialize_hex),
            (3, "lap4_ms", parse_hex, serialize_hex),
            (1, "lap5_minutes", parse_hex, serialize_hex),
            (2, "lap5_seconds", parse_hex, serialize_hex),
            (3, "lap5_ms", parse_hex, serialize_hex)
        ] + playerdata + [
            (1, "lap6_minutes", parse_hex, serialize_hex), # Just for GCN Baby Park
            (2, "lap6_seconds", parse_hex, serialize_hex),
            (3, "lap6_ms", parse_hex, serialize_hex),
            (1, "lap7_minutes", parse_hex, serialize_hex),
            (2, "lap7_seconds", parse_hex, serialize_hex),
            (3, "lap7_ms", parse_hex, serialize_hex)
        ]

    def __init__(self, filename) -> None:
        assert filename is not None
        self.filename = filename

    def parse(self) -> MK8GhostData:
        """ Parses the filename of the attached file"""
        if self.filename.startswith(MK8_GHOST_TYPES.MKTV_REPLAY.value):
            # MKTV ghosts have a different file format
            raise NotImplementedError("MKTV Replay files are not supported.")

        filename_len = len(self.filename)

        # Santity check filename length
        if filename_len != self.filename_length_v4 and filename_len != self.filename_length_v3:
            raise ValueError(f"Filename was of incorrect length. Expected {self.filename_length_v3} (v1-v3) or {self.filename_length_v4} (v4+), but got {filename_len}")

        # Obtain filename pattern based on game version
        pattern = self.filename_pattern_v3
        game_version = "3"
        if filename_len == self.filename_length_v4:
            pattern = self.filename_pattern_v4
            game_version = "4"

        # Parse contents
        i = 0
        results = {}
        for num_chars, identifier, parse_fn, _ in pattern:
            if parse_fn is not None:
                val = self.filename[i:i+num_chars]
                results[identifier] = parse_fn(val)
            i += num_chars

        return MK8GhostData(game_version, created_in_game=False, **results)

    @classmethod
    def serialize_filename(cls, data: MK8GhostData) -> str:
        """ Serializes ghost data into a filename as expected by the game """
        # Obtain filename pattern based on game version

        pattern = cls.filename_pattern_v3 if data.game_version == "3" else cls.filename_pattern_v4

        output = ""
        for num_chars, identifier, _, serialize_fn in pattern:
            if serialize_fn is not None:
                hex_str: str = serialize_fn(getattr(data, identifier, None))
                output += hex_str.zfill(num_chars)
            else:
                output += "0" * num_chars
        return output + ".dat"



if __name__ == '__main__':
    filename = "sg1121030000130c0012e0630230fd0231950231b993b3e793b3e7004e0069006e26050043006800720069007300006e000000"
    parser = MK8GhostFilenameParser(filename)
    res = parser.parse()
    print(res)
