

COURSE_NUMBERS = {
    0: 16, # Mario Circuit
    1: 17, # Thwomp Ruins
    2: 18, # Toad Harbour
    3: 19, # Sweet Sweet Canyon
    4: 20, # Twisted Mansion
    5: 21, # Shy Guy Falls
    6: 22, # Bone Dry Dunes
    7: 23, # Cloudtop Cruise
    8: 24, # Mount Wario
    9: 25, # Electrodrome
    10: 26, # Sunshine Airport
    11: 27, # Mario Kart Stadium
    12: 28, # Water Park
    13: 29, # Dolphin Shoals
    14: 30, # Bowser's Castle
    15: 31, # Rainbow Road
    16: 32, # 3DS DK Jungle
    17: 33, # Wii Moo Moo Meadows
    18: 34, # N64 Royal Raceway
    19: 35, # N64 Toad's Turnpike
    20: 36, # DS Cheep Cheep Beach
    21: 37, # GCN Sherbet Land
    22: 38, # GBA Mario Circuit
    23: 39, # 3DS Melody Motorway
    24: 40, # Wii Grumble Volcano
    25: 41, # SNES Donut Plains 3
    26: 42, # GCN Dry Dry Desert
    27: 43, # 3DS Piranha Plant Pipeway
    28: 44, # DS Tick-Tock Clock
    29: 45, # N64 Yoshi Valley
    30: 46, # DS Wario Stadium
    31: 47, # N64 Rainbow Road
    999: 56, # GCN Yoshi Circuit
    999: 53, # Excitebike Arena
    999: 50, # Dragon Driftway
    999: 49, # Mute City
    999: 57, # Wii Wario's Gold Mine
    999: 58, # SNES Rainbow Road
    999: 55, # Ice Ice Outpost
    999: 51, # Hyrule Circuit
    999: 61, # GCN Baby Park
    999: 62, # GBA Cheese Land
    999: 54, # Wild Woods
    999: 64, # Animal Crossing (Spring)
    999: 52, # Animal Crossing (Summer)
    999: 65, # Animal Crossing (Autumn)
    999: 66, # Animal Crossing (Winter)
    999: 60, # 3DS Neo Bowser City
    999: 59, # GBA Ribbon Road
    999: 48, # Super Bell Subway
    999: 63, # Big Blue
    -1: -1, # Battle Stadium (MK8D)
    -1: -1, # Sweet Sweet Kingdom (MK8D)
    -1: -1, # Dragon Palace (MK8D)
    -1: -1, # Lunar Colony (MK8D)
    -1: -1, # 3DS Wuhu Town (MK8D)
    -1: -1, # GCN Luigi's Mansion (MK8D)
    -1: -1, # SNES Battle Course 1 (MK8D)
    -1: -1, # Urchin Underpass (MK8D)
    -1: -1, # Tour Paris Promenade (MK8D DLC)
    -1: -1, # 3DS Toad Circuit (MK8D DLC)
    -1: -1, # N64 Choco Mountain (MK8D DLC)
    -1: -1, # Wii Coconut Mall (MK8D DLC)
    -1: -1, # Tour Tokyo Blur (MK8D DLC)
    -1: -1, # DS Shroom Ridge (MK8D DLC)
    -1: -1, # GBA Sky Garden (MK8D DLC)
    -1: -1, # Tour Ninja Hideaway (MK8D DLC)
}

COURSE_IDS = {
    27: ("Mario Kart Stadium", 0),
    28: ("Water Park", 8),
    19: ("Sweet Sweet Canyon", 16),
    17: ("Thwomp Ruins", 24),
    16: ("Mario Circuit", 1),
    18: ("Toad Harbour", 9),
    20: ("Twisted Mansion", 17),
    21: ("Shy Guy Falls", 25),
    26: ("Sunshine Airport", 2),
    29: ("Dolphin Shoals", 10),
    25: ("Electrodrome", 18),
    24: ("Mount Wario", 26),
    23: ("Cloudtop Cruise", 3),
    22: ("Bone Dry Dunes", 11),
    30: ("Bowser's Castle", 19),
    31: ("Rainbow Road", 27),
    33: ("Wii Moo Moo Meadows", 4),
    38: ("GBA Mario Circuit", 12),
    36: ("DS Cheep Cheep Beach", 20),
    35: ("N64 Toad's Turnpike", 28),
    42: ("GCN Dry Dry Desert", 5),
    41: ("SNES Donut Plains 3", 13),
    34: ("N64 Royal Raceway", 21),
    32: ("3DS DK Jungle", 29),
    46: ("DS Wario Stadium", 6),
    37: ("GCN Sherbet Land", 14),
    39: ("3DS Melody Motorway", 22),
    45: ("N64 Yoshi Valley", 30),
    44: ("DS Tick-Tock Clock", 7),
    43: ("3DS Piranha Plant Pipeway", 15),
    40: ("Wii Grumble Volcano", 23),
    47: ("N64 Rainbow Road", 31),
    56: ("GCN Yoshi Circuit", 32),
    53: ("Excitebike Arena", 36),
    50: ("Dragon Driftway", 40),
    49: ("Mute City", 44),
    57: ("Wii Wario's Gold Mine", 33),
    58: ("SNES Rainbow Road", 37),
    55: ("Ice Ice Outpost", 41),
    51: ("Hyrule Circuit", 45),
    61: ("GCN Baby Park", 34),
    62: ("GBA Cheese Land", 38),
    54: ("Wild Woods", 42),
    64: ("Animal Crossing (Spring)", 46),
    52: ("Animal Crossing (Summer)", 46),
    65: ("Animal Crossing (Autumn)", 46),
    66: ("Animal Crossing (Winter)", 46),
    60: ("3DS Neo Bowser City", 35),
    59: ("GBA Ribbon Road", 39),
    48: ("Super Bell Subway", 53),
    63: ("Big Blue", 47),
    -1: ("Battle Stadium", 48), # MK8D
    -1: ("Sweet Sweet Kingdom", 49), # MK8D
    -1: ("Dragon Palace", 50), # MK8D
    -1: ("Lunar Colony", 51), # MK8D
    -1: ("3DS Wuhu Town", 52), # MK8D
    -1: ("GCN Luigi's Mansion", 53), # MK8D
    -1: ("SNES Battle Course 1", 54), # MK8D
    -1: ("Urchin Underpass", 55), # MK8D
    -1: ("Tour Paris Promenade", None), # MK8D DLC
    -1: ("3DS Toad Circuit", None), # MK8D DLC
    -1: ("N64 Choco Mountain", None), # MK8D DLC
    -1: ("Wii Coconut Mall", None), # MK8D DLC
    -1: ("Tour Tokyo Blur", None), # MK8D DLC
    -1: ("DS Shroom Ridge", None), # MK8D DLC
    -1: ("GBA Sky Garden", None), # MK8D DLC
    -1: ("Tour Ninja Hideaway", None), # MK8D DLC
}

CHARACTERS = {
    0: ("Mario", 0),
    1: ("Luigi", 1),
    2: ("Peach", 2),
    3: ("Daisy", 3),
    4: ("Yoshi (Green)", 7),
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
    16: ("Shy Guy (Red)", 18),
    17: ("Baby Mario", 30),
    18: ("Baby Luigi", 31),
    19: ("Baby Peach", 32),
    20: ("Baby Daisy", 33),
    21: ("Baby Rosalina", 34),
    23: ("Lemmy", 45),
    22: ("Larry", 46),
    24: ("Wendy", 47),
    25: ("Ludwig von Koopa", 48),
    26: ("Iggy", 49),
    27: ("Roy", 50),
    28: ("Morton", 51),
    29: ("Mii (Standard)", 63),
    999: ("Mii (Amiibo Suit)", 64), # Update
    999: ("Yoshi (Red)", 8), # DLC
    999: ("Yoshi (Dark Blue)", 9), # DLC
    999: ("Yoshi (Light Blue)", 10), # DLC
    999: ("Yoshi (Yellow)", 11), # DLC
    999: ("Yoshi (Pink)", 12), # DLC
    999: ("Yoshi (Black)", 13), # DLC
    999: ("Yoshi (White)", 14), # DLC
    999: ("Yoshi (Orange)", 15), # DLC
    999: ("Shy Guy (Green)", 19), # DLC
    999: ("Shy Guy (Dark Blue)", 20), # DLC
    999: ("Shy Guy (Light Blue)", 21), # DLC
    999: ("Shy Guy (Yellow)", 22), # DLC
    999: ("Shy Guy (Pink)", 23), # DLC
    999: ("Shy Guy (Black)", 24), # DLC
    999: ("Shy Guy (White)", 25), # DLC
    999: ("Shy Guy (Orange)", 26), # DLC
    999: ("Tanooki Mario", 5), # DLC
    999: ("Cat Peach", 6), # DLC
    999: ("Dry Bowser", 44), # DLC
    999: ("Villager (Boy)", 60), # DLC
    999: ("Villager (Girl)", 61), # DLC
    999: ("Isabelle", 62), # DLC
    999: ("Link (Standard)", 58), # DLC
    -1: ("Link (Breath of the Wild)", 59), # MK8D
    -1: ("King Boo", 29), # MK8D
    -1: ("Dry Bones", 42), # MK8D
    -1: ("Bowser Jr.", 43), # MK8D
    -1: ("Golden Mario", 36), # MK8D
    -1: ("Inkling Girl (Orange)", 52), # MK8D
    -1: ("Inkling Girl (Green)", 53), # MK8D
    -1: ("Inkling Girl (Pink)", 54), # MK8D
    -1: ("Inkling Boy (Dark Blue)", 55), # MK8D
    -1: ("Inkling Boy (Purple)", 56), # MK8D
    -1: ("Inkling Boy (Light Blue)", 57), # MK8D
}

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
    999: ("GLA", 156), # DLC
    999: ("W 25 Silver Arrow", 165), # DLC
    999: ("300 SL Roadster", 166), # DLC
    999: ("Blue Falcon", 137), # DLC
    999: ("Tanooki Kart", 138), # DLC
    999: ("B Dasher", 139), # DLC
    999: ("Streetle", 140), # DLC
    999: ("P-Wing", 141), # DLC
    999: ("City Tripper", 252), # DLC
    999: ("Bone Rattler", 326), # DLC
    999: ("Master Cycle", 250), # DLC
    -1: ("Master Cycle Zero", 251), # MK8D
    -1: ("Koopa Clown", 168), # MK8D
    -1: ("Splat Buggy", 327), # MK8D
    -1: ("Inkstriker", 336), # MK8D
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
    999: ("GLA Wheels", 366), # DLC
    999: ("Triforce Tyres", 367), # DLC
    999: ("Leaf Tyres", 368), # DLC
    -1: ("Ancient Tyres", 369), # MK8D
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
    999: ("Hylian Kite", 445), # DLC
    999: ("Paper Glider", 446), # DLC
    -1: ("Paraglider", 447), # MK8D
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
