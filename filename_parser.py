from dataclasses import dataclass
from enum import Enum

from gamedata import MK8GhostType


class str_utf16be(str):
    """ Marker for utf-16-be encoded strings """
    pass

class int_lap(int):
    """ Marker for ints representing lap times """
    pass


class MK8GhostFilenameFormat:
    """ Format describing the structure of MK8 ghost files (Wii U) """
    # Data present in ghost files of all game versions
    format = [
        (2, "ghost_type", MK8GhostType),
        (2, "ghost_number", int),
        (2, "track_id", int),
        (2, "character_id", int),
        (2, "character_variant_id", int),
        (2, "mii_weight_class_id", int),
        (2, "kart_id", int),
        (2, "wheels_id", int),
        (2, "glider_id", int),
        (1, "total_minutes", int_lap),
        (2, "total_seconds", int_lap),
        (3, "total_ms", int_lap),
        (1, "lap1_minutes", int_lap),
        (2, "lap1_seconds", int_lap),
        (3, "lap1_ms", int_lap),
        (1, "lap2_minutes", int_lap),
        (2, "lap2_seconds", int_lap),
        (3, "lap2_ms", int_lap),
        (1, "lap3_minutes", int_lap),
        (2, "lap3_seconds", int_lap),
        (3, "lap3_ms", int_lap),
        (1, "lap4_minutes", int_lap),
        (2, "lap4_seconds", int_lap),
        (3, "lap4_ms", int_lap),
        (1, "lap5_minutes", int_lap),
        (2, "lap5_seconds", int_lap),
        (3, "lap5_ms", int_lap),
        (40, "playername", str_utf16be),
        (2, "flag_id", int),
        (2, "motion_control_flag", int),
        (4, None, None), # 0000 (or 00) Padding.
        (1, "lap6_minutes", int_lap),
        (2, "lap6_seconds", int_lap),
        (3, "lap6_ms", int_lap),
        (1, "lap7_minutes", int_lap),
        (2, "lap7_seconds", int_lap),
        (3, "lap7_ms", int_lap)
    ]

    class GameVersion(Enum):
        FILENAME_V3_NONSTANDARD = "v3 (non-standard)"
        FILENAME_V3 = "v3"
        FILENAME_V4 = "v4"

    class Length(Enum):
        FILENAME_V3_NONSTANDARD = 100
        FILENAME_V3 = 102
        FILENAME_V4 = 114

@dataclass
class MK8GhostFilenameData:
    """
        Dataclass containing all information present in the filename of a Mario Kart 8 ghost file.
    """
    game_version: MK8GhostFilenameFormat.GameVersion

    ghost_type: MK8GhostType
    playername: str
    flag_id: int
    motion_control_flag: int
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
    lap4_minutes: int
    lap4_seconds: int
    lap4_ms: int
    lap5_minutes: int
    lap5_seconds: int
    lap5_ms: int | None = None
    lap6_minutes: int | None = None
    lap6_seconds:  int | None = None
    lap6_ms:  int | None = None
    lap7_minutes:  int | None = None
    lap7_seconds:  int | None = None
    lap7_ms:  int | None = None


class MK8GhostFilenameParser:
    """ Parses information from the filename of Mario Kart 8 Ghost Files """

    def parse_MK8GhostType(self, val: str) -> MK8GhostType:
        """ Parses a string as a MK8GhostType """
        ghost_type = MK8GhostType(val)

        # MKTV ghosts have a different file format
        if ghost_type == MK8GhostType.MKTV_REPLAY.value:
            raise NotImplementedError("MKTV Replay files are not supported.")
        return ghost_type

    def parse_int(self, hex: str) -> int:
        """ Parses a string as a hexadecimal number """
        return int(hex, 16)

    def parse_int_lap(self, hex: str) -> int:
        """ Parses a string as a laptime """
        return self.parse_int(hex)

    def parse_str_utf16be(self, hex: str) -> str:
        """ Parses a utf-16-be encoded string """
        return bytes.fromhex(hex).split(b'\x00\x00', 1)[0].decode('utf-16-be')

    def parse_game_version(self, filename: str) -> str:
        """ Parses game version from filename """
        # Santity check filename length
        filename_len = len(filename)
        valid_filename_lens = [item.value for item in MK8GhostFilenameFormat.Length]
        if filename_len not in valid_filename_lens:
            raise ValueError(f"Filename was of incorrect length. Expected one of {', '.join(map(str, valid_filename_lens))}.")

        if filename_len == MK8GhostFilenameFormat.Length.FILENAME_V4.value:
            return MK8GhostFilenameFormat.GameVersion.FILENAME_V4
        elif filename_len == MK8GhostFilenameFormat.Length.FILENAME_V3.value:
            return MK8GhostFilenameFormat.GameVersion.FILENAME_V3
        return MK8GhostFilenameFormat.GameVersion.FILENAME_V3_NONSTANDARD

    def parse(self, filename: str) -> MK8GhostFilenameData:
        """ Parses the filename of the attached file"""
        game_version = self.parse_game_version(filename)

        # Parse contents
        i = 0
        results = {}
        for num_chars, identifier, data_type in MK8GhostFilenameFormat.format:
            if data_type is not None:
                val = filename[i:i+num_chars]
                if i + num_chars > len(filename):
                    # Nothing left to parse
                    break
                results[identifier] = getattr(self, f"parse_{data_type.__name__}")(val)
            i += num_chars
        return MK8GhostFilenameData(game_version, **results)

class MK8GhostFilenameSerializer:
    """ Serializes information from the filename of Mario Kart 8 Ghost Files """

    def serialize_MK8GhostType(self, ghost_type: MK8GhostType, num_chars: int) -> str:
        """ Serializes a MK8GhostType """
        return ghost_type.value

    def serialize_int(self, num: str, num_chars: int) -> int:
        """ Serializes a hex number """
        return f"{num:x}".rjust(num_chars, "0")

    def serialize_int_lap(self, lap_time: str, num_chars: int) -> int:
        """ Serializes a laptime """
        if lap_time is not None:
            return self.serialize_int(lap_time, num_chars)
        if num_chars == 1:
            return format(9, "x")
        elif num_chars == 2:
            return format(59, "x")
        return format(999, "x")

    def serialize_str_utf16be(self, val: str, num_chars: int) -> str:
        """ Serializes utf-16-be encoded string """
        return (val.encode('utf-16-be').hex()).ljust(num_chars, "0")

    def serialize(self, data: MK8GhostFilenameData) -> str:
        """ Serializes ghost data into a filename as expected by the game """
        # Obtain filename pattern based on game version
        output = ""
        chars_remaining = MK8GhostFilenameFormat.Length[data.game_version.name].value
        for num_chars, identifier, data_type in MK8GhostFilenameFormat.format:
            if data_type is not None:
                output += getattr(self, f"serialize_{data_type.__name__}")(getattr(data, identifier, None), num_chars)
            else:
                # Cannot seralize; fill with zeroes
                output += "0" * min(num_chars, chars_remaining)

            chars_remaining -= num_chars
            if chars_remaining <= 0:
                # Nothing left to serialize
                break
        return output + ".dat"


if __name__ == '__main__':
    filename = "sg1121030000130c0012e0630230fd0231950231b993b3e793b3e7004e0069006e26050043006800720069007300006e000000"
            #   sg1121030000130c0012e0630230fd0231950231b993b3e793b3e7004e0069006e26050043006800720069007300006e000000
    parser = MK8GhostFilenameParser()
    res = parser.parse(filename)
    print(res)

    serializer = MK8GhostFilenameSerializer()
    name = serializer.serialize(res)
    print(name)
    print(name == f"{filename}.dat")
