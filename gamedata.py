from dataclasses import dataclass
from enum import Enum

class MK8GhostType(Enum):
    """ Enumeration of all types of ghosts in Mario Kart 8 """
    STAFF_GHOST = "sg"
    PLAYER_GHOST = "gs"
    DOWNLOADED_GHOST = "dg"
    MKTV_REPLAY = "rp" # Different file format than a ghost

@dataclass
class MK8DLC:
    name: str

    def __str__(self):
        return self.name

DLC_ZELDA = MK8DLC("The Legend of Zelda × Mario Kart 8")
DLC_ANIMAL_CROSSING = MK8DLC("Animal Crossing × Mario Kart 8")
DLC_DELUXE = MK8DLC("Mario Kart 8 Deluxe")
DLC_BOOSTER_COURSE_1 = MK8DLC("Booster Course Pass (Wave 1)")
DLC_BOOSTER_COURSE_2 = MK8DLC("Booster Course Pass (Wave 2)")
DLC_BOOSTER_COURSE_3 = MK8DLC("Booster Course Pass (Wave 3)")
DLC_BOOSTER_COURSE_4 = MK8DLC("Booster Course Pass (Wave 4)")
DLC_BOOSTER_COURSE_5 = MK8DLC("Booster Course Pass (Wave 5)")
DLC_BOOSTER_COURSE_6 = MK8DLC("Booster Course Pass (Wave 6)")

@dataclass
class MK8Cup:
    name: str
    dlc: MK8DLC|None = None

    def __str__(self):
        return self.name

CUP_MUSHROOM = MK8Cup("Mushroom Cup")
CUP_FLOWER = MK8Cup("Flower Cup")
CUP_STAR = MK8Cup("Star Cup")
CUP_SPECIAL = MK8Cup("Special Cup")
CUP_SHELL = MK8Cup("Shell Cup")
CUP_BANANA = MK8Cup("Banana Cup")
CUP_LEAF = MK8Cup("Leaf Cup")
CUP_LIGHTNING = MK8Cup("Lightning Cup")
CUP_EGG = MK8Cup("Egg Cup", dlc=DLC_ZELDA)
CUP_TRIFORCE = MK8Cup("Triforce Cup", dlc=DLC_ZELDA)
CUP_CROSSING = MK8Cup("Crossing Cup", dlc=DLC_ANIMAL_CROSSING)
CUP_BELL = MK8Cup("Bell Cup", dlc=DLC_ANIMAL_CROSSING)
CUP_BATTLE_COURSES = MK8Cup("Battle Course", dlc=DLC_DELUXE)
CUP_GOLDEN_DASH = MK8Cup("Golden Dash Cup", dlc=DLC_BOOSTER_COURSE_1)
CUP_LUCKY_CAT = MK8Cup("Lucky Cat Cup", dlc=DLC_BOOSTER_COURSE_1)

@dataclass
class MK8Course:
    course_id: int
    name: str
    icon_index: int
    cup: MK8Cup

    def __str__(self):
        return self.name

COURSE_IDS = {
    16: MK8Course(16, "Mario Circuit", 4, CUP_FLOWER),
    17: MK8Course(17, "Thwomp Ruins", 3, CUP_MUSHROOM),
    18: MK8Course(18, "Toad Harbor", 5, CUP_FLOWER),
    19: MK8Course(19, "Sweet Sweet Canyon", 2, CUP_MUSHROOM),
    20: MK8Course(20, "Twisted Mansion", 6, CUP_FLOWER),
    21: MK8Course(21, "Shy Guy Falls", 7, CUP_FLOWER),
    22: MK8Course(22, "Bone-Dry Dunes", 13, CUP_SPECIAL),
    23: MK8Course(23, "Cloudtop Cruise", 12, CUP_SPECIAL),
    24: MK8Course(24, "Mount Wario", 11, CUP_STAR),
    25: MK8Course(25, "Electrodrome", 10, CUP_STAR),
    26: MK8Course(26, "Sunshine Airport", 8, CUP_STAR),
    27: MK8Course(27, "Mario Kart Stadium", 0, CUP_MUSHROOM),
    28: MK8Course(28, "Water Park", 1, CUP_MUSHROOM),
    29: MK8Course(29, "Dolphin Shoals", 9, CUP_STAR),
    30: MK8Course(30, "Bowser's Castle", 14, CUP_SPECIAL),
    31: MK8Course(31, "Rainbow Road", 15, CUP_SPECIAL),
    32: MK8Course(32, "3DS DK Jungle", 23, CUP_BANANA),
    33: MK8Course(33, "Wii Moo Moo Meadows", 16, CUP_SHELL),
    34: MK8Course(34, "N64 Royal Raceway", 22, CUP_BANANA),
    35: MK8Course(35, "N64 Toad's Turnpike", 19, CUP_SHELL),
    36: MK8Course(36, "DS Cheep Cheep Beach", 18, CUP_SHELL),
    37: MK8Course(37, "GCN Sherbet Land", 25, CUP_LEAF),
    38: MK8Course(38, "GBA Mario Circuit", 17, CUP_SHELL),
    39: MK8Course(39, "3DS Music Park", 26, CUP_LEAF),
    40: MK8Course(40, "Wii Grumble Volcano", 30, CUP_LIGHTNING),
    41: MK8Course(41, "SNES Donut Plains 3", 21, CUP_BANANA),
    42: MK8Course(42, "GCN Dry Dry Desert", 20, CUP_BANANA),
    43: MK8Course(43, "3DS Piranha Plant Slide", 29, CUP_LIGHTNING),
    44: MK8Course(44, "DS Tick-Tock Clock", 28, CUP_LIGHTNING),
    45: MK8Course(45, "N64 Yoshi Valley", 27, CUP_LEAF),
    46: MK8Course(46, "DS Wario Stadium", 24, CUP_LEAF),
    47: MK8Course(47, "N64 Rainbow Road", 31, CUP_LIGHTNING),
    48: MK8Course(48, "Super Bell Subway", 46, CUP_BELL),
    49: MK8Course(49, "Mute City", 35, CUP_EGG),
    50: MK8Course(50, "Dragon Driftway", 34, CUP_EGG),
    51: MK8Course(51, "Hyrule Circuit", 39, CUP_TRIFORCE),
    52: MK8Course(52, "Animal Crossing (Summer)", 43, CUP_CROSSING),
    53: MK8Course(53, "Excitebike Arena", 33, CUP_EGG),
    54: MK8Course(54, "Wild Woods", 42, CUP_CROSSING),
    55: MK8Course(55, "Ice Ice Outpost", 38, CUP_TRIFORCE),
    56: MK8Course(56, "GCN Yoshi Circuit", 32, CUP_EGG),
    57: MK8Course(57, "Wii Wario's Goldmine", 36, CUP_TRIFORCE),
    58: MK8Course(58, "SNES Rainbow Road", 37, CUP_TRIFORCE),
    59: MK8Course(59, "GBA Ribbon Road", 45, CUP_BELL),
    60: MK8Course(60, "3DS Neo Bowser City", 44, CUP_BELL),
    61: MK8Course(61, "GCN Baby Park", 40, CUP_CROSSING),
    62: MK8Course(62, "GBA Cheese Land", 41, CUP_CROSSING),
    63: MK8Course(63, "Big Blue", 47, CUP_BELL),
    64: MK8Course(64, "Animal Crossing (Spring)", 43, CUP_CROSSING),
    65: MK8Course(65, "Animal Crossing (Autumn)", 43, CUP_CROSSING),
    66: MK8Course(66, "Animal Crossing (Winter)", 43, CUP_CROSSING),
    67: MK8Course(67, "Battle Stadium", 48, CUP_BATTLE_COURSES),
    68: MK8Course(68, "Sweet Sweet Kindom", 49, CUP_BATTLE_COURSES),
    69: MK8Course(69, "Dragon Palace", 50, CUP_BATTLE_COURSES),
    70: MK8Course(70, "Lunar Colony", 51, CUP_BATTLE_COURSES),
    71: MK8Course(71, "3DS Wuhu Town", 52, CUP_BATTLE_COURSES),
    72: MK8Course(72, "GCN Luigi's Mansion", 53, CUP_BATTLE_COURSES),
    73: MK8Course(73, "SNES Battle Course 1", 54, CUP_BATTLE_COURSES),
    74: MK8Course(74, "Urchin Underpass", 55, CUP_BATTLE_COURSES),
    75: MK8Course(75, "Tour Paris Promenade", 56, CUP_GOLDEN_DASH),
    76: MK8Course(76, "3DS Toad Circuit", 57, CUP_GOLDEN_DASH),
    77: MK8Course(77, "N64 Choco Mountain", 58, CUP_GOLDEN_DASH),
    78: MK8Course(78, "Wii Coconut Mall", 59, CUP_GOLDEN_DASH),
    79: MK8Course(79, "Tour Tokyo Blur", 60, CUP_LUCKY_CAT),
    80: MK8Course(80, "DS Shroom Ridge", 61, CUP_LUCKY_CAT),
    81: MK8Course(81, "GBA Sky Garden", 62, CUP_LUCKY_CAT),
    82: MK8Course(82, "Tour Ninja Hideway", 63, CUP_LUCKY_CAT),
}

AMIIBO_SUITS = [
    ("Mario Suit Male 1", 64), ("Mario Suit Female 1", 64),
    ("Mario Suit Male 2", 64), ("Mario Suit Female 2", 64),
    ("Mario Suit Male 3", 64), ("Mario Suit Female 3", 64),
    ("Mario Suit Male 4", 64), ("Mario Suit Female 4", 64),
    ("Luigi Suit Male 1", 64), ("Luigi Suit Female 1", 64),
    ("Luigi Suit Male 2", 64), ("Luigi Suit Female 2", 64),
    ("Luigi Suit Male 3", 64), ("Luigi Suit Female 3", 64),
    ("Luigi Suit Male 4", 64), ("Luigi Suit Female 4", 64),
    ("Yoshi Suit Male 1", 64), ("Yoshi Suit Female 1", 64),
    ("Yoshi Suit Male 2", 64), ("Yoshi Suit Female 2", 64),
    ("Yoshi Suit Male 3", 64), ("Yoshi Suit Female 3", 64),
    ("Yoshi Suit Male 4", 64), ("Yoshi Suit Female 4", 64),
    ("Peach Suit Male 1", 64), ("Peach Suit Female 1", 64),
    ("Peach Suit Male 2", 64), ("Peach Suit Female 2", 64),
    ("Peach Suit Male 3", 64), ("Peach Suit Female 3", 64),
    ("Peach Suit Male 4", 64), ("Peach Suit Female 4", 64),
    ("Toad Suit Male 1", 64), ("Toad Suit Female 1", 64),
    ("Toad Suit Male 2", 64), ("Toad Suit Female 2", 64),
    ("Toad Suit Male 3", 64), ("Toad Suit Female 3", 64),
    ("Toad Suit Male 4", 64), ("Toad Suit Female 4", 64),
    ("Donkey Kong Suit Male 1", 64), ("Donkey Kong Suit Female 1", 64),
    ("Donkey Kong Suit Male 2", 64), ("Donkey Kong Suit Female 2", 64),
    ("Donkey Kong Suit Male 3", 64), ("Donkey Kong Suit Female 3", 64),
    ("Donkey Kong Suit Male 4", 64), ("Donkey Kong Suit Female 4", 64),
    ("Bowser Suit Male 1", 64), ("Bowser Suit Female 1", 64),
    ("Bowser Suit Male 2", 64), ("Bowser Suit Female 2", 64),
    ("Bowser Suit Male 3", 64), ("Bowser Suit Female 3", 64),
    ("Bowser Suit Male 4", 64), ("Bowser Suit Female 4", 64),
    ("Wario Suit Male 1", 64), ("Wario Suit Female 1", 64),
    ("Wario Suit Male 2", 64), ("Wario Suit Female 2", 64),
    ("Wario Suit Male 3", 64), ("Wario Suit Female 3", 64),
    ("Wario Suit Male 4", 64), ("Wario Suit Female 4", 64),
    ("Captain Falcon Suit Male 1", 64), ("Captain Falcon Suit Female 1", 64),
    ("Captain Falcon Suit Male 2", 64), ("Captain Falcon Suit Female 2", 64),
    ("Captain Falcon Suit Male 3", 64), ("Captain Falcon Suit Female 3", 64),
    ("Captain Falcon Suit Male 4", 64), ("Captain Falcon Suit Female 4", 64),
    ("Fox Suit Male 1", 64), ("Fox Suit Female 1", 64),
    ("Fox Suit Male 2", 64), ("Fox Suit Female 2", 64),
    ("Fox Suit Male 3", 64), ("Fox Suit Female 3", 64),
    ("Fox Suit Male 4", 64), ("Fox Suit Female 4", 64),
    ("Varia Suit Male 1", 64), ("Varia Suit Female 1", 64),
    ("Varia Suit Male 2", 64), ("Varia Suit Female 2", 64),
    ("Varia Suit Male 3", 64), ("Varia Suit Female 3", 64),
    ("Varia Suit Male 4", 64), ("Varia Suit Female 4", 64),
    ("Hylian Suit Male 1", 64), ("Hylian Suit Female 1", 64),
    ("Hylian Suit Male 2", 64), ("Hylian Suit Female 2", 64),
    ("Hylian Suit Male 3", 64), ("Hylian Suit Female 3", 64),
    ("Hylian Suit Male 4", 64), ("Hylian Suit Female 4", 64),
    ("Inkling Suit Male 1", 64), ("Inkling Suit Female 1", 64), # MK8D
    ("Inkling Suit Male 2", 64), ("Inkling Suit Female 2", 64), # MK8D
    ("Inkling Suit Male 3", 64), ("Inkling Suit Female 3", 64), # MK8D
    ("Inkling Suit Male 4", 64), ("Inkling Suit Female 4", 64), # MK8D
    ("Kirby Suit Male 1", 64), ("Kirby Suit Female 1", 64),
    ("Kirby Suit Male 2", 64), ("Kirby Suit Female 2", 64),
    ("Kirby Suit Male 3", 64), ("Kirby Suit Female 3", 64),
    ("Kirby Suit Male 4", 64), ("Kirby Suit Female 4", 64),
    ("Rosalina Suit Male 1", 64), ("Rosalina Suit Female 1", 64),
    ("Rosalina Suit Male 2", 64), ("Rosalina Suit Female 2", 64),
    ("Rosalina Suit Male 3", 64), ("Rosalina Suit Female 3", 64),
    ("Rosalina Suit Male 4", 64), ("Rosalina Suit Female 4", 64),
    ("Pikmin Suit Male 1", 64), ("Pikmin Suit Female 1", 64),
    ("Pikmin Suit Male 2", 64), ("Pikmin Suit Female 2", 64),
    ("Pikmin Suit Male 3", 64), ("Pikmin Suit Female 3", 64),
    ("Pikmin Suit Male 4", 64), ("Pikmin Suit Female 4", 64),
    ("Animal Crossing Suit Male 1", 64), ("Animal Crossing Suit Female 1", 64),
    ("Animal Crossing Suit Male 2", 64), ("Animal Crossing Suit Female 2", 64),
    ("Animal Crossing Suit Male 3", 64), ("Animal Crossing Suit Female 3", 64),
    ("Animal Crossing Suit Male 4", 64), ("Animal Crossing Suit Female 4", 64),
    ("PAC-MAN Suit Male 1", 64), ("PAC-MAN Suit Female 1", 64),
    ("PAC-MAN Suit Male 2", 64), ("PAC-MAN Suit Female 2", 64),
    ("PAC-MAN Suit Male 3", 64), ("PAC-MAN Suit Female 3", 64),
    ("PAC-MAN Suit Male 4", 64), ("PAC-MAN Suit Female 4", 64),
    ("Mega Man Suit Male 1", 64), ("Mega Man Suit Female 1", 64),
    ("Mega Man Suit Male 2", 64), ("Mega Man Suit Female 2", 64),
    ("Mega Man Suit Male 3", 64), ("Mega Man Suit Female 3", 64),
    ("Mega Man Suit Male 4", 64), ("Mega Man Suit Female 4", 64),
    ("Sonic Suit Male 1", 64), ("Sonic Suit Female 1", 64),
    ("Sonic Suit Male 2", 64), ("Sonic Suit Female 2", 64),
    ("Sonic Suit Male 3", 64), ("Sonic Suit Female 3", 64),
    ("Sonic Suit Male 4", 64), ("Sonic Suit Female 4", 64),
]

CHARACTERS = {
    0: ("Mario", 0),
    1: ("Luigi", 1),
    2: ("Peach", 2),
    3: ("Daisy", 3),
    4: ("Yoshi", [
        ("Green", 7), ("Red", 8), ("Blue", 9),
        ("Light Blue", 10), ("Yellow", 11), ("Pink", 12),
        ("Black", 13), ("White", 14), ("Orange", 15),
    ]),
    5: ("Toad", 16),
    6: ("Toadette", 28),
    7: ("Koopa Troopa", 17),
    8: ("Bowser", 41),
    9: ("Donkey Kong", 40),
    10: ("Wario", 38),
    11: ("Waluigi", 39),
    12: ("Rosalina", 4),
    13: ("Metal Mario", 35),
    14: ("Pink Gold Peach", 37),
    15: ("Lakitu", 27),
    16: ("Shy Guy", [
        ("Red", 18), ("Green", 19), ("Blue", 20),
        ("Light Blue", 21), ("Yellow", 22), ("Pink", 23),
        ("Black", 24), ("White", 25), ("Orange", 26),
    ]),
    17: ("Baby Mario", 30),
    18: ("Baby Luigi", 31),
    19: ("Baby Peach", 32),
    20: ("Baby Daisy", 33),
    21: ("Baby Rosalina", 34),
    23: ("Lemmy", 45),
    22: ("Larry", 46),
    24: ("Wendy", 47),
    25: ("Ludwig", 48),
    26: ("Iggy", 49),
    27: ("Roy", 50),
    28: ("Morton", 51),
    29: ("Mii", [
        ("Red Male", 63), ("Red Female", 63), ("Orange Male", 63), ("Orange Female", 63),
        ("Yellow Male", 63), ("Yellow Female", 63), ("Light Green Male", 63), ("Light Green Female", 63),
        ("Green Male", 63), ("Green Female", 63), ("Blue Male", 63), ("Blue Female", 63),
        ("Light Blue Male", 63), ("Light Blue Female", 63), ("Pink Male", 63), ("Pink Female", 63),
        ("Purple Male", 63), ("Purple Female", 63), ("Brown Male", 63), ("Brown Female", 63),
        ("White Male", 63), ("White Female", 63), ("Black Male", 63), ("Black Female", 63),
        *AMIIBO_SUITS,
    ]),
    30: ("Tanooki Mario", 5), # DLC
    34: ("Cat Peach", 6), # DLC
    35: ("Dry Bowser", 44), # DLC
    32: ("Villager (Male)", 60), # DLC
    36: ("Villager (Female)", 61), # DLC
    33: ("Isabelle", 62), # DLC
    31: ("Link", [("Standard", 58), ("Breath of the Wild", 59), ]), # DLC/MK8D
    40: ("King Boo", 29), # MK8D
    38: ("Dry Bones", 42), # MK8D
    39: ("Bowser Jr.", 43), # MK8D
    37: ("Gold Mario", 36), # MK8D
    41: ("Inkling Girl (Orange)", [("Orange", 52), ("Lime", 53), ("Magenta", 54), ]), # MK8D
    42: ("Inkling Boy (Blue)", [("Blue", 55), ("Purple", 56), ("Teal", 57), ]), # MK8D
}

MII_WEIGHT_CLASSES = ("Light", "Medium", "Heavy")

KARTS = {
    0: ("Standard Kart", 0),
    1: ("Pipe Frame", 60),
    2: ("Mach 8", 120),
    3: ("Steel Driver", 121),
    4: ("Cat Cruiser", 122),
    5: ("Circuit Special", 123),
    6: ("Tri-Speeder", 127),
    7: ("Badwagon", 128),
    8: ("Prancer", 129),
    9: ("Buggybud", 132),
    10: ("Landship", 144),
    11: ("Bounder", 152),
    12: ("Sports Coupé", 130),
    13: ("Gold Kart", 131),
    14: ("Standard Bike", 180),
    15: ("Comet", 240),
    16: ("Sport Bike", 241),
    17: ("The Duke", 244),
    18: ("Flame Rider", 245),
    19: ("Varmint", 246),
    20: ("Mr Scooty", 247),
    21: ("Jet Bike", 248),
    22: ("Yoshi Bike", 249),
    23: ("Standard Quad", 264),
    24: ("Wild Wiggler", 324),
    25: ("Teddy Buggy", 325),
    26: ("GLA", 156), # DLC
    27: ("W 25 Silver Arrow", 165), # DLC
    28: ("300 SL Roadster", 166), # DLC
    29: ("Blue Falcon", 137), # DLC
    30: ("Tanooki Kart", 138), # DLC
    31: ("B Dasher", 139), # DLC
    35: ("Streetle", 140), # DLC (33 for MK8D)
    36: ("P-Wing", 141), # DLC (34 for MK8D)
    37: ("City Tripper", 252), # DLC (35 MK8D)
    38: ("Bone Rattler", 326), # DLC (36 MK8D)
    32: ("Master Cycle", 250), # DLC
    -1: ("Master Cycle Zero", 251), # MK8D 0x28?
    -1: ("Koopa Clown", 168), # MK8D 37
    -1: ("Splat Buggy", 327), # MK8D 38
    -1: ("Inkstriker", 336), # MK8D 39
}

WHEELS = {
    0: ("Normal", 348),
    1: ("Monster", 349),
    2: ("Roller", 350),
    3: ("Slim", 351),
    4: ("Slick", 352),
    5: ("Metal", 353),
    6: ("Button", 354),
    7: ("Off-Road", 355),
    8: ("Sponge", 356),
    9: ("Wooden", 357),
    10: ("Cushion", 358),
    11: ("Normal Blue", 359),
    12: ("Funky Monster", 360),
    13: ("Azure Roller", 361),
    14: ("Crimson Slim", 362),
    15: ("Cyber Slick", 363),
    16: ("Retro Off-Road", 364),
    17: ("Gold Wheels", 365),
    18: ("GLA Wheels", 366), # DLC
    19: ("Triforce Tyres", 367), # DLC
    20: ("Leaf Tyres", 368), # DLC
    -1: ("Ancient Tyres", 369), # MK8D 0x15?
}

GLIDERS = {
    0: ("Super Glider", 372),
    1: ("Cloud Glider", 432),
    2: ("Wario Wing", 433),
    3: ("Waddle Wing", 434),
    4: ("Peach Parasol", 435),
    5: ("Parachute", 438),
    6: ("Parafoil", 439),
    7: ("Flower Glider", 440),
    8: ("Bowser Kite", 441),
    9: ("Plane Glider", 442),
    10: ("MKTV Parafoil", 443),
    11: ("Gold Glider", 444),
    12: ("Hylian Kite", 445), # DLC
    13: ("Paper Glider", 446), # DLC
    -1: ("Paraglider", 447), # MK8D 0x0e?
}

FLAGS = [
   (None, None),
   ("JP", 0),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   ("AI", 41),
   ("AG", 60),
   ("AR", 53),
   ("AW", 70),
   ("BS", 17),
   ("BB", 31),
   ("BZ", 46),
   ("BO", 64),
   ("BR", 10),
   ("VG", 25),
   ("CA", 39),
   ("KY", None),
   ("CL", 52),
   ("CO", 69),
   ("CR", 16),
   ("DM", 30),
   ("DO", 45),
   ("EC", 63),
   ("SV", 9),
   ("GF", None),
   ("GD", 38),
   ("GP", None),
   ("GT", 51),
   ("GY", 68),
   ("HT", 15),
   ("HN", 29),
   ("JM", 44),
   ("MQ", None),
   ("MX", 8),
   ("MS", 24),
   ("AN", 37),
   ("NI", 58),
   ("PA", 50),
   ("PY", 67),
   ("PE", 14),
   ("KN", 28),
   ("LC", 43),
   ("VC", 62),
   ("SR", 7),
   ("TT", 23),
   ("TC", 36),
   ("US", 57),
   ("UY", 49),
   ("VI", 66),
   ("VE", 13),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   ("AL", None),
   ("AU", 61),
   ("AT", 6),
   ("BE", 22),
   ("BA", None),
   ("BW", None),
   ("BG", 48),
   ("HR", 65),
   ("CY", 12),
   ("CZ", 27),
   ("DK", 42),
   ("EE", None),
   ("FI", 5),
   ("FR", 21),
   ("DE", 35),
   ("GR", 56),
   ("HU", 47),
   ("IS", None),
   ("IE", 11),
   ("IT", 26),
   ("LV", None),
   ("LS", None),
   ("LI", None),
   ("LT", None),
   ("LU", 33),
   ("MK", None),
   ("MT", None),
   ("ME", None),
   ("MZ", None),
   ("NA", None),
   ("NL", 40),
   ("NZ", 59),
   ("NO", 2),
   ("PL", 20),
   ("PT", 32),
   ("RO", 55),
   ("RU", 4),
   ("RS", None),
   ("SK", 34),
   ("SI", None),
   ("ZA", None),
   ("ES", 19),
   ("SZ", None),
   ("SE", 54),
   ("CH", 1),
   ("TR", 18),
   ("GB", 3),
   ("ZM", None),
   ("ZW", None),
   ("AZ", None),
   ("MR", None),
   ("ML", None),
   ("NE", None),
   ("TD", None),
   ("SD", None),
   ("ER", None),
   ("DJ", None),
   ("SO", None),
   ("AD", None),
   ("GI", None),
   ("GG", None),
   ("IM", None),
   ("JE", None),
   ("MC", None),
   ("TW", None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   ("KR", None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   ("HK", None),
   ("MO", None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   ("ID", None),
   ("SG", None),
   ("TH", None),
   ("PH", None),
   ("MY", None),
   (None, None),
   (None, None),
   (None, None),
   ("CN", None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   ("AE", None),
   (None, None),
   ("EG", None),
   ("OM", None),
   ("QA", None),
   ("KW", None),
   ("SA", None),
   ("SY", None),
   ("BH", None),
   ("JO", None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   ("SM", None),
   ("VA", None),
   ("BM", None),
   ("IN", None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   ("NG", None),
   ("AO", None),
   ("GH", None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
   (None, None),
]
