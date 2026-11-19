from __future__ import annotations

TRAINER_LOCATIONS: dict[str, tuple[int, int | None, str | None, tuple[int, int] | None]] = {
    # Abundant Shrine
    'Abundant Shrine - Trainer: Youngster Jaye below shrine': (810557, 2077, 'Abundant Shrine', None),
    'Abundant Shrine - Trainer: Lass Lurleen in west': (810558, 2078, 'Abundant Shrine', None),
    'Abundant Shrine - Trainer: Youngster Wes north of house': (810559, 2079, 'Abundant Shrine', None),
    'Abundant Shrine - Trainer: Twins Rae & Ula west of house': (810560, 2080, 'Abundant Shrine', None),

    # Aspertia City
    'Aspertia City - Trainer: PkMn Trainer Hugh': (810161, 1681, 'Aspertia City', None, (1682, 1683)),

    # Aspertia Gym
    'Aspertia Gym - Trainer: Gym Leader Cheren': (810156, 1676, 'Aspertia Gym', None, (2284,)),
    'Aspertia Gym - Trainer: Youngster Pedro': (810171, 1691, 'Aspertia Gym', None),
    'Aspertia Gym - Trainer: Lass Serena': (810172, 1692, 'Aspertia Gym', None),

    # Castelia Gym
    'Castelia Gym - Trainer: Gym Leader Burgh': (810154, 1674, 'Castelia Gym', None, (2286,)),
    'Castelia Gym - Trainer: Harlequin Clarence': (810734, 2254, 'Castelia Gym', None),
    'Castelia Gym - Trainer: Harlequin Jack': (810735, 2255, 'Castelia Gym', None),
    'Castelia Gym - Trainer: Harlequin Gary': (810736, 2256, 'Castelia Gym', None),
    'Castelia Gym - Trainer: Harlequin Anders': (810737, 2257, 'Castelia Gym', None),

    # Castelia City
    'Castelia City - Trainer: Castelia Street - GAME FREAK Morimoto at Game Freak': (810140, 1660, 'Castelia City', None, ()),
    'Castelia City - Trainer: Castelia Street - GAME FREAK Nishino at Game Freak': (810357, 1877, 'Castelia City', None, ()),
    'Castelia City - Trainer: Castelia Street - Clerk (M) Clemens at Battle Company 47F': (810501, 2021, 'Castelia City', None),
    'Castelia City - Trainer: Castelia Street - Clerk (M) Warren at Battle Company 47F)': (810502, 2022, 'Castelia City', None),
    'Castelia City - Trainer: Castelia Street - School Kid Neil at Battle Company 55F': (810503, 2023, 'Castelia City', None),
    'Castelia City - Trainer: Castelia Street - GAME FREAK Nishino at Game Freak (Post-HoF)': (810591, 2111, 'Castelia City', None, ()),
    'Castelia City - Trainer: Castelia Street - GAME FREAK Morimoto at Game Freak (Post-HoF)': (810592, 2112, 'Castelia City', None, ()),
    'Castelia City - Trainer: Castelia Street - Clerk (F) Britney at Battle Company 47F': (810691, 2211, 'Castelia City', None),
    'Castelia City - Trainer: Castelia Street - Clerk (M) Gilligan at Battle Company 47F': (810692, 2212, 'Castelia City', None),
    'Castelia City - Trainer: Back alley accessible from sewers - Roughneck Ricky (Spring/Summer, Surf)': (810754, 2274, 'Castelia City', None),
    'Castelia City - Trainer: Back alley accessible from sewers - Dancer Jean-Paul (Spring/Summer, Surf)': (810755, 2275, 'Castelia City', None),
    'Castelia City - Trainer: Back alley accessible from sewers - Guitarist Tina (Spring/Summer, Surf)': (810756, 2276, 'Castelia City', None),

    # Castelia Sewers
    'Castelia Sewers - Trainer: Team Plasma Grunt 1 near Relic Passage': (810342, 1862, 'Castelia Sewers', None),
    'Castelia Sewers - Trainer: Team Plasma Grunt 2 near Relic Passage': (810356, 1876, 'Castelia Sewers', None),
    'Castelia Sewers - Trainer: Janitor Felix in east': (810461, 1981, 'Castelia Sewers', None),
    'Castelia Sewers - Trainer: Janitor Brady in north (Spring/Summer, Surf)': (810462, 1982, 'Castelia Sewers', None),
    'Castelia Sewers - Trainer: Scientist Clarke in southeast (Spring/Summer, Surf)': (810463, 1983, 'Castelia Sewers', None),
    'Castelia Sewers - Trainer: Scientist Caroline in centre-northeast (Autumn/Winter)': (810464, 1984, 'Castelia Sewers', None),
    'Castelia Sewers - Trainer: Worker Zack in centre': (810465, 1985, 'Castelia Sewers', None),
    'Castelia Sewers - Trainer: Worker Scott in west (Autumn/Winter or Spring/Summer, Surf)': (810466, 1986, 'Castelia Sewers', None),
    'Castelia Sewers - Trainer: Doctor Heath in centre-north': (810679, 2199, 'Castelia Sewers', None),

    # Celestial Tower
    'Celestial Tower - Trainer: School Kid Alberta 2F': (810455, 1975, 'Celestial Tower', None),
    'Celestial Tower - Trainer: Waitress Jan 1F after starting quest in Humilau': (810457, 1977, 'Celestial Tower', None),
    'Celestial Tower - Trainer: Nursery Aide Ilse 2F after starting quest in Humilau': (810458, 1978, 'Celestial Tower', None),
    'Celestial Tower - Trainer: Clerk (F) Lana 3F after starting quest in Humilau': (810459, 1979, 'Celestial Tower', None),
    'Celestial Tower - Trainer: Maid Tammy 4F after starting quest in Humilau': (810460, 1980, 'Celestial Tower', None),
    'Celestial Tower - Trainer: Pokéfan Jude 2F, northeast': (810549, 2069, 'Celestial Tower', None),
    'Celestial Tower - Trainer: Pokéfan Georgia 3F northwest': (810550, 2070, 'Celestial Tower', None),
    'Celestial Tower - Trainer: Gentleman Daniel 4F, centre': (810551, 2071, 'Celestial Tower', None),
    'Celestial Tower - Trainer: Socialite Grace 4F, southwest': (810552, 2072, 'Celestial Tower', None),
    'Celestial Tower - Trainer: Psychic Micki 3F centre': (810553, 2073, 'Celestial Tower', None),
    'Celestial Tower - Trainer: Psychic Joyce 2F southwest': (810554, 2074, 'Celestial Tower', None),
    'Celestial Tower - Trainer: Psychic Bryce 3F east': (810555, 2075, 'Celestial Tower', None),
    'Celestial Tower - Trainer: Psychic Sarah 4F east': (810556, 2076, 'Celestial Tower', None),
    'Celestial Tower - Trainer: Nurse Dixie 3F southeast': (810673, 2193, 'Celestial Tower', None),

    # Chargestone Cave
    'Chargestone Cave - Trainer: Guitarist Anna 1F northwest': (810537, 2057, 'Chargestone Cave', None),
    'Chargestone Cave - Trainer: Guitarist Beverly B2F northwest': (810538, 2058, 'Chargestone Cave', None),
    'Chargestone Cave - Trainer: Hiker Otto 1F northeast': (810539, 2059, 'Chargestone Cave', None),
    'Chargestone Cave - Trainer: Hiker Jeremy B2F west': (810540, 2060, 'Chargestone Cave', None),
    'Chargestone Cave - Trainer: Scientist Ronald 1F west': (810541, 2061, 'Chargestone Cave', None),
    'Chargestone Cave - Trainer: Scientist Lumi B1F northeast': (810542, 2062, 'Chargestone Cave', None),
    'Chargestone Cave - Trainer: Ranger Briana B1F southeast': (810543, 2063, 'Chargestone Cave', None),
    'Chargestone Cave - Trainer: Ranger Louis 1F south': (810544, 2064, 'Chargestone Cave', None),
    'Chargestone Cave - Trainer: Ace Trainer Vicki B2F south': (810545, 2065, 'Chargestone Cave', None),
    'Chargestone Cave - Trainer: Ace Trainer Corky 1F, southeast': (810546, 2066, 'Chargestone Cave', None),
    'Chargestone Cave - Trainer: Ace Trainer Shaye B2F, north': (810547, 2067, 'Chargestone Cave', None),
    'Chargestone Cave - Trainer: Ace Trainer Mary 1F, north': (810548, 2068, 'Chargestone Cave', None),
    'Chargestone Cave - Trainer: Doctor Kit B1F centre-east': (810671, 2191, 'Chargestone Cave', None),

    # Clay Tunnel
    'Clay Tunnel - Trainer: Hiker Teppei in Room 1 south': (810487, 2007, 'Clay Tunnel', None),
    'Clay Tunnel - Trainer: Hiker Manuel in Room 2 south of pond': (810488, 2008, 'Clay Tunnel', None),
    'Clay Tunnel - Trainer: Worker Morgann in Room 1 north': (810489, 2009, 'Clay Tunnel', None),
    'Clay Tunnel - Trainer: Worker Herman in Room 2 west of pond': (810490, 2010, 'Clay Tunnel', None),
    'Clay Tunnel - Trainer: Worker Paul in Room 2 north': (810491, 2011, 'Clay Tunnel', None),
    'Clay Tunnel - Trainer: Worker Leo in Room 3 central': (810506, 2026, 'Clay Tunnel', None),
    'Clay Tunnel - Trainer: Worker Brand in Room 3 central-north': (810507, 2027, 'Clay Tunnel', None),
    'Clay Tunnel - Trainer: Ranger Maxwell in Room 3 south': (810508, 2028, 'Clay Tunnel', None),
    'Clay Tunnel - Trainer: Ranger Katie in Room 3 north (Surf)': (810509, 2029, 'Clay Tunnel', None),

    # Desert Resort
    'Desert Resort - Trainer: Backpacker Walt in central-north': (810662, 2182, 'Desert Resort', None),
    'Desert Resort - Trainer: Backpacker Sam in central-west': (810663, 2183, 'Desert Resort', None),
    'Desert Resort - Trainer: Backpacker Tami in west': (810664, 2184, 'Desert Resort', None),
    'Desert Resort - Trainer: Backpacker Clara in centre': (810665, 2185, 'Desert Resort', None),
    'Desert Resort - Trainer: Ranger Jaden near entrance': (810666, 2186, 'Desert Resort', None),
    'Desert Resort - Trainer: Ranger Anja in east': (810667, 2187, 'Desert Resort', None),
    'Desert Resort - Trainer: Psychic Tommy southeast of Relic Castle': (810668, 2188, 'Desert Resort', None),
    'Desert Resort - Trainer: Psychic Future in northwest': (810669, 2189, 'Desert Resort', None),
    'Desert Resort - Trainer: Nurse Mariah in southeast': (810670, 2190, 'Desert Resort', None),

    # Dreamyard
    'Dreamyard - Trainer: Youngster Keita west of dark grass in southern section': (810593, 2113, 'Dreamyard', None),
    'Dreamyard - Trainer: School Kid William near furnace in southern section': (810739, 2259, 'Dreamyard', None),
    'Dreamyard - Trainer: School Kid Rita in western dead end in southern section': (810740, 2260, 'Dreamyard', None),
    'Dreamyard - Trainer: Psychic Olesi in south-east': (810741, 2261, 'Dreamyard', None),
    'Dreamyard - Trainer: Psychic Nandor in centre': (810742, 2262, 'Dreamyard', None),
    'Dreamyard - Trainer: Scientist Athena in east': (810743, 2263, 'Dreamyard', None),
    'Dreamyard - Trainer: Scientist Franklin in south-west': (810744, 2264, 'Dreamyard', None),

    # Driftveil Gym
    'Driftveil Gym - Trainer: Gym Leader Clay': (810158, 1678, 'Driftveil Gym', None, (2288,)),
    'Driftveil Gym - Trainer: Worker Maynard': (810319, 1839, 'Driftveil Gym', None),
    'Driftveil Gym - Trainer: Worker Pasqual': (810320, 1840, 'Driftveil Gym', None),
    'Driftveil Gym - Trainer: Worker Tibor': (810321, 1841, 'Driftveil Gym', None),
    'Driftveil Gym - Trainer: Worker Niel': (810322, 1842, 'Driftveil Gym', None),
    'Driftveil Gym - Trainer: Worker Tavarius': (810323, 1843, 'Driftveil Gym', None),
    'Driftveil Gym - Trainer: Worker Noel': (810324, 1844, 'Driftveil Gym', None),
    'Driftveil Gym - Trainer: Worker Friedrich': (810325, 1845, 'Driftveil Gym', None),

    # Driftveil City
    'Driftveil City - Trainer: Trainer Rood in safe house': (810346, 1866, 'Driftveil City', None),
    'Driftveil City - Trainer: Motorcyclist Charles': (810366, 1886, 'Driftveil City', None, (1887,)),
    'Driftveil City - Trainer: PkMn Trainer Hugh (post HoF)': (810696, 2216, 'Driftveil City', None, (2217, 2218)),

    # Floccesy Ranch
    'Floccesy Ranch - Trainer: PkMn Trainer Hugh at entrance': (810166, 1686, 'Floccesy Ranch', None, (1687, 1688)),
    'Floccesy Ranch - Trainer: Youngster Kenny in northern area': (810180, 1700, 'Floccesy Ranch', None),
    'Floccesy Ranch - Trainer: Lass Molly in southwest': (810181, 1701, 'Floccesy Ranch', None),
    'Floccesy Ranch - Trainer: Janitor Orville in northwest': (810182, 1702, 'Floccesy Ranch', None),

    # Floccesy Town
    'Floccesy Town - Trainer: School Kid Seymour in Alder\'s house': (810169, 1689, 'Floccesy Town', None, (2267, 2269)),
    'Floccesy Town - Trainer: School Kid Cassie in Alder\'s house': (810170, 1690, 'Floccesy Town', None, (2268, 2270)),
    'Floccesy Town - Trainer: PkMn Trainer Alder': (810582, 2102, 'Floccesy Town', None),

    # Giant Chasm
    'Giant Chasm - Trainer: Team Plasma Ghetsis in far cave': (810345, 1865, 'Giant Chasm', None),
    'Giant Chasm - Trainer: Team Plasma Grunt in crater': (810724, 2244, 'Giant Chasm', None),

    # Humilau Gym
    'Humilau Gym - Trainer: Gym Leader Marlon': (810160, 1680, 'Humilau Gym', None, (2291,)),
    'Humilau Gym - Trainer: Ace Trainer Doyle': (810350, 1870, 'Humilau Gym', None),
    'Humilau Gym - Trainer: Ace Trainer Melina': (810351, 1871, 'Humilau Gym', None),
    'Humilau Gym - Trainer: Ace Trainer Enzio': (810352, 1872, 'Humilau Gym', None),
    'Humilau Gym - Trainer: Ace Trainer Jeanne': (810353, 1873, 'Humilau Gym', None),
    'Humilau Gym - Trainer: Ace Trainer Santino': (810354, 1874, 'Humilau Gym', None),
    'Humilau Gym - Trainer: Ace Trainer Sable': (810355, 1875, 'Humilau Gym', None),

    # Icirrus City
    'Icirrus City - Trainer: Team Plasma Shadow 1': (810687, 2207, 'Icirrus City', None),
    'Icirrus City - Trainer: Team Plasma Shadow 2': (810688, 2208, 'Icirrus City', None),
    'Icirrus City - Trainer: Team Plasma Shadow 3': (810689, 2209, 'Icirrus City', None),

    # Lacunosa Town
    'Lacunosa Town - Trainer: Team Plasma Zinzolin': (810704, 2224, 'Lacunosa Town', None),
    'Lacunosa Town - Trainer: Team Plasma Grunt': (810705, 2225, 'Lacunosa Town', None),

    # Lostlorn Forest
    'Lostlorn Forest - Trainer: Veteran Murphy on cliff (Surf, Waterfall)': (810142, 1662, 'Lostlorn Forest', None),
    'Lostlorn Forest - Trainer: Ranger Serenity in west': (810297, 1817, 'Lostlorn Forest', None),
    'Lostlorn Forest - Trainer: Ranger Forrest in north': (810298, 1818, 'Lostlorn Forest', None),
    'Lostlorn Forest - Trainer: Breeder Galen in south': (810299, 1819, 'Lostlorn Forest', None),

    # Mistralton Cave
    'Mistralton Cave - Trainer: Hiker Jebediah 1F north': (810680, 2200, 'Mistralton Cave', None),
    'Mistralton Cave - Trainer: Hiker Shelby 1F south': (810681, 2201, 'Mistralton Cave', None),
    'Mistralton Cave - Trainer: Ace Trainer Geoff 2F west': (810682, 2202, 'Mistralton Cave', None),
    'Mistralton Cave - Trainer: Ace Trainer Belle 2F east': (810683, 2203, 'Mistralton Cave', None),

    # Mistralton Gym
    'Mistralton Gym - Trainer: Gym Leader Skyla': (810155, 1675, 'Mistralton Gym', None, (2289,)),
    'Mistralton Gym - Trainer: Pilot Flynn': (810149, 1669, 'Mistralton Gym', None),
    'Mistralton Gym - Trainer: Pilot Winslow': (810150, 1670, 'Mistralton Gym', None),
    'Mistralton Gym - Trainer: Pilot Ewing': (810151, 1671, 'Mistralton Gym', None),
    'Mistralton Gym - Trainer: Pilot Chase': (810152, 1672, 'Mistralton Gym', None),
    'Mistralton Gym - Trainer: Pilot Elron': (810332, 1852, 'Mistralton Gym', None),

    # Moor of Icirrus
    'Moor of Icirrus - Trainer: Fisherman Eustace in east': (810576, 2096, 'Moor of Icirrus', None),
    'Moor of Icirrus - Trainer: Fisherman Arnold in north': (810577, 2097, 'Moor of Icirrus', None),
    'Moor of Icirrus - Trainer: Ranger Parker in south-east': (810578, 2098, 'Moor of Icirrus', None),
    'Moor of Icirrus - Trainer: Ranger Elaine in west (Strength)': (810579, 2099, 'Moor of Icirrus', None),

    # N's Castle
    "N's Castle - Trainer: Trainer N": (810005, 1525, "N's Castle", None, (1526,)),
    "N's Castle - Trainer: Trainer N (Seasonal)": (810782, 2302, "N's Castle", None, (2303, 2304, 2305)),

    # Nimbasa City
    'Nimbasa City - Trainer: Lady Colette in old Gym': (810148, 1668, 'Nimbasa City', None),
    'Nimbasa City - Trainer: Rich Boy Rolan in old Gym': (810621, 2141, 'Nimbasa City', None),
    'Nimbasa City - Trainer: Team Plasma Grunt in amusement park': (810359, 1879, 'Nimbasa City', None),
    'Nimbasa City - Trainer: Team Plasma Grunt by Ferris Wheel': (810751, 2271, 'Nimbasa City', None),

    # Nimbasa Gym
    'Nimbasa Gym - Trainer: Gym Leader Elesa': (810153, 1673, 'Nimbasa Gym', None, (2287,)),
    'Nimbasa Gym - Trainer: Beauty Nikola': (810207, 1727, 'Nimbasa Gym', None),
    'Nimbasa Gym - Trainer: Beauty Fleming': (810208, 1728, 'Nimbasa Gym', None),
    'Nimbasa Gym - Trainer: Beauty Ampère': (810209, 1729, 'Nimbasa Gym', None),

    # Opelucid Gym
    'Opelucid Gym - Trainer: Gym Leader Drayden': (810159, 1679, 'Opelucid Gym', None, (2290,)),
    'Opelucid Gym - Trainer: Veteran Lucius': (810381, 1901, 'Opelucid Gym', None),
    'Opelucid Gym - Trainer: Veteran Jerry': (810382, 1902, 'Opelucid Gym', None),
    'Opelucid Gym - Trainer: Veteran Rhona': (810383, 1903, 'Opelucid Gym', None),
    'Opelucid Gym - Trainer: Veteran Ron': (810384, 1904, 'Opelucid Gym', None),
    'Opelucid Gym - Trainer: Veteran Denae': (810385, 1905, 'Opelucid Gym', None),

    # Opelucid City
    'Opelucid City - Trainer: Team Plasma Shadow': (810583, 2103, 'Opelucid City', None),
    'Opelucid City - Trainer: Team Plasma Zinzolin': (810584, 2104, 'Opelucid City', None),
    'Opelucid City - Trainer: Team Plasma Grunt 1': (810585, 2105, 'Opelucid City', None),
    'Opelucid City - Trainer: Team Plasma Grunt 2': (810586, 2106, 'Opelucid City', None),
    'Opelucid City - Trainer: Team Plasma Grunt 3': (810587, 2107, 'Opelucid City', None),

    # P2 Laboratory
    'P2 Laboratory - Trainer: Scientist Dudley': (810135, 1655, 'P2 Laboratory', None),

    # Pinwheel Forest
    'Pinwheel Forest - Trainer: School Kid Keston': (810633, 2153, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: School Kid Millie': (810634, 2154, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Ace Trainer Kelsey': (810635, 2155, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Ace Trainer Kathrine': (810636, 2156, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Black Belt Kentaro': (810637, 2157, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Battle Girl Lee': (810638, 2158, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Ranger Ralph': (810639, 2159, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Ranger Dwayne': (810640, 2160, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Ranger Melita': (810641, 2161, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Ranger Hillary': (810642, 2162, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Veteran Sinan': (810643, 2163, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Veteran Rosaline': (810644, 2164, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Youngster Keita': (810645, 2165, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Youngster Nicholas': (810646, 2166, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Nursery Aide Ethel': (810647, 2167, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Preschooler Jojo': (810648, 2168, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Preschooler José': (810649, 2169, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Preschooler Samantha': (810650, 2170, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Twins Ally & Amy': (810651, 2171, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Nursery Aide Rosalyn': (810790, 2310, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Preschooler Ike': (810791, 2311, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Youngster Henley': (810792, 2312, 'Pinwheel Forest', None),
    'Pinwheel Forest - Trainer: Lass Helia': (810793, 2313, 'Pinwheel Forest', None),

    # PWT (Plasma Frigate incident)
    'PWT - Trainer: Team Plasma Grunt 1 (Plasma Frigate)': (810372, 1892, 'PWT', None),
    'PWT - Trainer: Team Plasma Grunt 2 (Plasma Frigate)': (810373, 1893, 'PWT', None),
    'PWT - Trainer: Team Plasma Grunt 3 (Plasma Frigate)': (810374, 1894, 'PWT', None),
    'PWT - Trainer: Team Plasma Grunt 4 (Plasma Frigate)': (810375, 1895, 'PWT', None),
    'PWT - Trainer: Team Plasma Grunt 5 (Plasma Frigate)': (810376, 1896, 'PWT', None),
    'PWT - Trainer: Team Plasma Grunt 6 (Plasma Frigate)': (810377, 1897, 'PWT', None),

    # Plasma Frigate (Route 21)
    'Plasma Frigate - Trainer: Team Plasma Grunt 4 (from Route 21)': (810426, 1946, 'Plasma Frigate (Route 21)', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 5 (from Route 21)': (810427, 1947, 'Plasma Frigate (Route 21)', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 20 (from Route 21)': (810800, 2320, 'Plasma Frigate (Route 21)', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 21 (from Route 21)': (810801, 2321, 'Plasma Frigate (Route 21)', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 22 (from Route 21)': (810802, 2322, 'Plasma Frigate (Route 21)', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 23 (from Route 21)': (810807, 2327, 'Plasma Frigate (Route 21)', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 25 (from Route 21)': (810809, 2329, 'Plasma Frigate (Route 21)', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 27 (from Route 21)': (810812, 2332, 'Plasma Frigate (Route 21)', None),

    # Plasma Frigate (Giant Chasm & P2 Lab)
    'Plasma Frigate - Trainer: Team Plasma Grunt 1 (from Giant Chasm)': (810343, 1863, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Colress (from Giant Chasm)': (810344, 1864, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Zinzolin (from Giant Chasm)': (810347, 1867, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Shadow 1 (from Giant Chasm)': (810348, 1868, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 6 (from Giant Chasm)': (810428, 1948, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 7 (from Giant Chasm)': (810429, 1949, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 8 (from Giant Chasm)': (810431, 1951, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 9 (from Giant Chasm)': (810436, 1956, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 10 (from Giant Chasm)': (810437, 1957, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 11 (from Giant Chasm)': (810445, 1965, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 12 (from Giant Chasm)': (810446, 1966, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 13 (from Giant Chasm)': (810447, 1967, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 14 (from Giant Chasm)': (810448, 1968, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 15 (from Giant Chasm)': (810449, 1969, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 16 (from Giant Chasm)': (810452, 1972, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 17 (from Giant Chasm)': (810453, 1973, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 18 (from Giant Chasm)': (810454, 1974, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Zinzolin (from Giant Chasm)': (810497, 2017, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Shadow 2 (from Giant Chasm)': (810498, 2018, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Shadow 3 (from Giant Chasm)': (810499, 2019, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 19 (from Giant Chasm)': (810500, 2020, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 32 (from Giant Chasm)': (810797, 2317, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 33 (from Giant Chasm)': (810798, 2318, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 34 (from Giant Chasm)': (810799, 2319, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 24 (from Giant Chasm)': (810808, 2328, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Team Plasma Grunt 26 (from Giant Chasm)': (810810, 2330, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Doctor Julius (from Giant Chasm)': (810811, 2331, 'Plasma Frigate', None),
    'Plasma Frigate - Trainer: Colress (Post-Game at P2 Lab)': (810813, 2333, 'Plasma Frigate', None),

    # Pokémon League
    'Pokemon League - Trainer: Elite Four Shauntal': (810143, 1663, 'Pokemon League', None, (2292,)),
    'Pokemon League - Trainer: Elite Four Marshal': (810144, 1664, 'Pokemon League', None, (2294,)),
    'Pokemon League - Trainer: Elite Four Grimsley': (810145, 1665, 'Pokemon League', None, (2293,)),
    'Pokemon League - Trainer: Elite Four Caitlin': (810146, 1666, 'Pokemon League', None, (2295,)),
    'Pokemon League - Trainer: Champion Iris': (810536, 2056, 'Pokemon League', None, (2296,)),
    'Pokemon League - Trainer: Rematch Elite Four Shauntal': (810777, 2297, 'Pokemon League', None, ()),
    'Pokemon League - Trainer: Rematch Elite Four Grimsley': (810778, 2298, 'Pokemon League', None, ()),
    'Pokemon League - Trainer: Rematch Elite Four Marshal': (810779, 2299, 'Pokemon League', None, ()),
    'Pokemon League - Trainer: Rematch Elite Four Caitlin': (810780, 2300, 'Pokemon League', None, ()),
    'Pokemon League - Trainer: Rematch Champion Iris': (810781, 2301, 'Pokemon League', None, ()),

    # Relic Castle
    'Relic Castle - Trainer: Psychic Dua in B1F southeast': (810510, 2030, 'Relic Castle', None),
    'Relic Castle - Trainer: Psychic Perry in 1F southwest': (810511, 2031, 'Relic Castle', None),
    'Relic Castle - Trainer: Psychic Low in B1F north': (810512, 2032, 'Relic Castle', None),

    # Relic Passage
    'Relic Passage - Trainer: Hiker Tobias in middle section northwest': (810561, 2081, 'Relic Passage', None),
    'Relic Passage - Trainer: Hiker Keith near Driftveil exit': (810562, 2082, 'Relic Passage', None),
    'Relic Passage - Trainer: Backpacker Kendall in Castelia section': (810563, 2083, 'Relic Passage (Castelia)', None),
    'Relic Passage - Trainer: Backpacker Randall near Driftveil exit': (810564, 2084, 'Relic Passage', None),
    'Relic Passage - Trainer: Backpacker Annie in middle section south': (810565, 2085, 'Relic Passage', None),
    'Relic Passage - Trainer: Backpacker Eileen near Driftveil exit': (810566, 2086, 'Relic Passage', None),
    'Relic Passage - Trainer: Scientist Terrance in Castelia section': (810567, 2087, 'Relic Passage (Castelia)', None),
    'Relic Passage - Trainer: Scientist Lumina in Castelia section': (810568, 2088, 'Relic Passage (Castelia)', None),
    'Relic Passage - Trainer: Psychic Tully in middle section north': (810569, 2089, 'Relic Passage', None),
    'Relic Passage - Trainer: Psychic Ena in middle section northeast': (810570, 2090, 'Relic Passage', None),

    # Reversal Mountain
    'Reversal Mountain - Trainer: Cyclist Adelaide Exterior': (810467, 1987, 'Reversal Mountain', None),
    'Reversal Mountain - Trainer: Cyclist Jeremiah Exterior': (810468, 1988, 'Reversal Mountain', None),
    'Reversal Mountain - Trainer: Backpacker Kiyo 1F': (810513, 2033, 'Reversal Mountain', None, (2308,)),
    'Reversal Mountain - Trainer: Backpacker Kumiko 1F': (810514, 2034, 'Reversal Mountain', None, (2309,)),
    'Reversal Mountain - Trainer: Ranger Lewis 2F B2 / 1F W2': (810515, 2035, 'Reversal Mountain', None, (2036,)),
    'Reversal Mountain - Trainer: Ranger Eliza 1F B2 / 2F W2': (810517, 2037, 'Reversal Mountain', None, (2038,)),
    'Reversal Mountain - Trainer: Ace Trainer Ray 1F': (810519, 2039, 'Reversal Mountain', None, (2306,)),
    'Reversal Mountain - Trainer: Ace Trainer Cora 1F': (810520, 2040, 'Reversal Mountain', None, (2307,)),
    'Reversal Mountain - Trainer: Hiker Jared 1F': (810521, 2041, 'Reversal Mountain', None),
    'Reversal Mountain - Trainer: Hiker Markus 1F': (810522, 2042, 'Reversal Mountain', None),
    'Reversal Mountain - Trainer: Black Belt Corey 1F': (810523, 2043, 'Reversal Mountain', None),
    'Reversal Mountain - Trainer: Battle Girl Chan 1F': (810524, 2044, 'Reversal Mountain', None),
    'Reversal Mountain - Trainer: Doctor Derek 1F': (810672, 2192, 'Reversal Mountain', None),

    # Route 1
    'Route 1 - Trainer: Backpacker Shane': (810405, 1925, 'Route 1', None),
    'Route 1 - Trainer: Backpacker Jill': (810406, 1926, 'Route 1', None),
    'Route 1 - Trainer: Ranger Rick': (810409, 1929, 'Route 1', None),
    'Route 1 - Trainer: Ranger Audra': (810410, 1930, 'Route 1', None),
    'Route 1 - Trainer: Ace Trainer Sean': (810411, 1931, 'Route 1', None),
    'Route 1 - Trainer: Ace Trainer Cheyenne': (810412, 1932, 'Route 1', None),

    # Route 11
    'Route 11 - Trainer: Breeder Magnolia': (810303, 1823, 'Route 11', None),
    'Route 11 - Trainer: Ranger Thalia (Surf, Waterfall)': (810304, 1824, 'Route 11', None),
    'Route 11 - Trainer: Ranger Crofton': (810305, 1825, 'Route 11', None),

    # Route 12
    'Route 12 - Trainer: Backers Cleo & Rio': (810291, 1811, 'Route 12', None),
    'Route 12 - Trainer: Black Belt Jeriel': (810300, 1820, 'Route 12', None),
    'Route 12 - Trainer: Battle Girl Azra': (810301, 1821, 'Route 12', None),

    # Route 13
    'Route 13 - Trainer: Ace Trainer Angi': (810133, 1653, 'Route 13', None),
    'Route 13 - Trainer: Ace Trainer Miguel': (810134, 1654, 'Route 13', None),
    'Route 13 - Trainer: Fisherman Jones on sand bar': (810286, 1806, 'Route 13', None),
    'Route 13 - Trainer: Fisherman Damon on sand bar': (810287, 1807, 'Route 13', None),
    'Route 13 - Trainer: Fisherman Leroy in south-east': (810288, 1808, 'Route 13', None),
    'Route 13 - Trainer: Fisherman Vince north-east of dark grass island (Surf)': (810289, 1809, 'Route 13', None),
    'Route 13 - Trainer: Parasol Lady Laura south of sand bar': (810290, 1810, 'Route 13', None),
    'Route 13 - Trainer: Ranger Daryl east of house': (810294, 1814, 'Route 13', None),
    'Route 13 - Trainer: Ranger Dianne east of Cobalion in north': (810295, 1815, 'Route 13', None),
    'Route 13 - Trainer: Black Belt Wesley': (810730, 2250, 'Route 13', None),
    'Route 13 - Trainer: Battle Girl Alize': (810731, 2251, 'Route 13', None),

    # Route 14
    'Route 14 - Trainer: Gentleman Sheldon': (810277, 1797, 'Route 14', None),
    'Route 14 - Trainer: Socialite Marian': (810278, 1798, 'Route 14', None),
    'Route 14 - Trainer: Ace Trainer Kipp': (810279, 1799, 'Route 14', None),
    'Route 14 - Trainer: Ace Trainer Junko': (810280, 1800, 'Route 14', None),
    'Route 14 - Trainer: Black Belt Jay (Surf, Waterfall)': (810281, 1801, 'Route 14', None),
    'Route 14 - Trainer: Battle Girl Glinda': (810282, 1802, 'Route 14', None),
    'Route 14 - Trainer: Fisherman Sid': (810283, 1803, 'Route 14', None),
    'Route 14 - Trainer: Backpacker Reece (Surf)': (810285, 1805, 'Route 14', None),

    # Route 15
    'Route 15 - Trainer: Pokéfan Elliot': (810652, 2172, 'Route 15', None),
    'Route 15 - Trainer: Pokéfan Lydia': (810653, 2173, 'Route 15', None),
    'Route 15 - Trainer: Scientist Marie': (810654, 2174, 'Route 15', None),
    'Route 15 - Trainer: Backpacker Talon': (810655, 2175, 'Route 15', None),
    'Route 15 - Trainer: Backpacker Corin': (810656, 2176, 'Route 15', None),

    # Route 16
    'Route 16 - Trainer: Backers Stu & Art on south path': (810257, 1777, 'Route 16', None),
    'Route 16 - Trainer: Backpacker Ivan in northwest': (810258, 1778, 'Route 16', None),
    'Route 16 - Trainer: Backpacker Blossom in northeast (Strength)': (810259, 1779, 'Route 16', None),
    'Route 16 - Trainer: Cyclist Hector on south path': (810260, 1780, 'Route 16', None),
    'Route 16 - Trainer: Cyclist Krissa in east': (810261, 1781, 'Route 16', None),
    'Route 16 - Trainer: Depot Agent Hank in west': (810262, 1782, 'Route 16', None),

    # Route 17
    'Route 17 - Trainer: Fisherman Lydon': (810413, 1933, 'Route 17', None),
    'Route 17 - Trainer: Fisherman Bucky': (810414, 1934, 'Route 17', None),
    'Route 17 - Trainer: Swimmer (M) Wright': (810415, 1935, 'Route 17', None),
    'Route 17 - Trainer: Swimmer (M) Jeffery': (810416, 1936, 'Route 17', None),
    'Route 17 - Trainer: Swimmer (F) Ruth': (810417, 1937, 'Route 17', None),
    'Route 17 - Trainer: Swimmer (F) Dara': (810418, 1938, 'Route 17', None),

    # Route 18
    'Route 18 - Trainer: Hiker Stephen': (810419, 1939, 'Route 18', None),
    'Route 18 - Trainer: Veteran Vincent': (810420, 1940, 'Route 18', None),
    'Route 18 - Trainer: Veteran Chester': (810421, 1941, 'Route 18', None),
    'Route 18 - Trainer: Veteran Maya': (810422, 1942, 'Route 18', None),
    'Route 18 - Trainer: Veteran Gina': (810423, 1943, 'Route 18', None),
    'Route 18 - Trainer: Black Belt Zachary': (810424, 1944, 'Route 18', None),
    'Route 18 - Trainer: Battle Girl Wendy': (810425, 1945, 'Route 18', None),

    # Route 2
    'Route 2 - Trainer: Youngster Jimmy': (810401, 1921, 'Route 2', None),
    'Route 2 - Trainer: Lass Mali': (810402, 1922, 'Route 2', None),
    'Route 2 - Trainer: Veteran Oriana': (810403, 1923, 'Route 2', None),
    'Route 2 - Trainer: Veteran Rayne': (810404, 1924, 'Route 2', None),
    'Route 2 - Trainer: Youngster Mikey': (810407, 1927, 'Route 2', None),
    'Route 2 - Trainer: Lass Henrietta': (810408, 1928, 'Route 2', None),

    # Route 20
    'Route 20 - Trainer: Youngster Terrell in northwest near Floccesy': (810164, 1684, 'Route 20', None),
    'Route 20 - Trainer: Lass Isabel in western grass patch': (810165, 1685, 'Route 20', None),
    'Route 20 - Trainer: Preschooler Albert east of bridge': (810173, 1693, 'Route 20', None),
    'Route 20 - Trainer: Preschooler Lin east of Nursery Aide': (810174, 1694, 'Route 20', None),
    'Route 20 - Trainer: Twins Lia & Lily near dark grass': (810175, 1695, 'Route 20', None),
    'Route 20 - Trainer: Nursery Aide Kimya in central clearing': (810176, 1696, 'Route 20', None),
    'Route 20 - Trainer: Hiker Jerome on eastern path': (810206, 1726, 'Route 20', None),
    'Route 20 - Trainer: Pokemon Ranger Leaf on southeast island (Basic Badge, Autumn, Surf)': (810386, 1906, 'Route 20', None),
    'Route 20 - Trainer: Pokemon Ranger Naoko above waterfall (Basic Badge, Autumn, Surf, Waterfall)': (810387, 1907, 'Route 20', None),
    'Route 20 - Trainer: Pokemon Ranger Bret on central island (Basic Badge, Autumn, Surf)': (810388, 1908, 'Route 20', None),
    'Route 20 - Trainer: Pokemon Ranger Malory on eastern island (Basic Badge, Autumn, Surf)': (810389, 1909, 'Route 20', None),
    'Route 20 - Trainer: Youngster Petey on western path': (810392, 1912, 'Route 20', None),
    'Route 20 - Trainer: Team Plasma Grunt near dark grass': (810763, 2283, 'Route 20', None),

    # Route 21
    'Route 21 - Trainer: Swimmer (M) Kyle': (810308, 1828, 'Route 21', None),
    'Route 21 - Trainer: Swimmer (F) Kaoru': (810309, 1829, 'Route 21', None),
    'Route 21 - Trainer: Swimmer (M) Harold': (810310, 1830, 'Route 21', None),
    'Route 21 - Trainer: Swimmer (F) Desiree': (810311, 1831, 'Route 21', None),
    'Route 21 - Trainer: Fisherman Kenzo': (810312, 1832, 'Route 21', None),
    'Route 21 - Trainer: Black Belt Kenneth': (810326, 1846, 'Route 21', None),
    'Route 21 - Trainer: Doctor Braid': (810327, 1847, 'Route 21', None),

    # Route 22
    'Route 22 - Trainer: Ace Trainer Lucca': (810043, 1563, 'Route 22', None),
    'Route 22 - Trainer: Ace Trainer Shel': (810044, 1564, 'Route 22', None),
    'Route 22 - Trainer: Backpacker Myra': (810306, 1826, 'Route 22', None),
    'Route 22 - Trainer: Backpacker Lowell': (810307, 1827, 'Route 22', None),
    'Route 22 - Trainer: Breeder Addison': (810333, 1853, 'Route 22', None),
    'Route 22 - Trainer: Hiker Justin': (810334, 1854, 'Route 22', None),

    # Route 23
    'Route 23 - Trainer: Hiker Don': (810475, 1995, 'Route 23', None),
    'Route 23 - Trainer: Hiker Doug (Cut)': (810476, 1996, 'Route 23', None),
    'Route 23 - Trainer: Black Belt Luke': (810477, 1997, 'Route 23', None),
    'Route 23 - Trainer: Battle Girl Brenda': (810478, 1998, 'Route 23', None),
    'Route 23 - Trainer: Ace Trainer Juliet': (810479, 1999, 'Route 23', None),
    'Route 23 - Trainer: Ace Trainer Grant': (810480, 2000, 'Route 23', None),
    'Route 23 - Trainer: Black Belt Benjamin (Cut)': (810481, 2001, 'Route 23', None),
    'Route 23 - Trainer: Battle Girl Tiffany (Cut, Strength)': (810482, 2002, 'Route 23', None),
    'Route 23 - Trainer: Ranger Lena': (810483, 2003, 'Route 23', None),
    'Route 23 - Trainer: Ranger Steve': (810484, 2004, 'Route 23', None),
    'Route 23 - Trainer: Ace Trainer Tom (Cut)': (810485, 2005, 'Route 23', None),
    'Route 23 - Trainer: Ace Trainer Miki (Cut)': (810486, 2006, 'Route 23', None),

    # Route 3
    'Route 3 - Trainer: Lass Shannon': (810337, 1857, 'Route 3', None),
    'Route 3 - Trainer: School Kid Edgar': (810393, 1913, 'Route 3', None),
    'Route 3 - Trainer: School Kid Marsha': (810394, 1914, 'Route 3', None),
    'Route 3 - Trainer: Nursery Aide Autumn': (810395, 1915, 'Route 3', None),
    'Route 3 - Trainer: Preschooler Buster': (810396, 1916, 'Route 3', None),
    'Route 3 - Trainer: Preschooler Eva': (810397, 1917, 'Route 3', None),
    'Route 3 - Trainer: Preschooler Tyrone': (810398, 1918, 'Route 3', None),
    'Route 3 - Trainer: Fisherman Bruce': (810399, 1919, 'Route 3', None),
    'Route 3 - Trainer: Fisherman Mack (Surf)': (810400, 1920, 'Route 3', None),
    'Route 3 - Trainer: Backers May & Mal': (810753, 2273, 'Route 3', None),

    # Route 4
    'Route 4 - Trainer: Lady Lina in central ruins': (810147, 1667, 'Route 4', None),
    'Route 4 - Trainer: Fisherman Hubert at south water': (810210, 1730, 'Route 4', None),
    'Route 4 - Trainer: Fisherman Andrew at south water': (810211, 1731, 'Route 4', None),
    'Route 4 - Trainer: Policeman Braven in south near Castelia Gate': (810212, 1732, 'Route 4', None),
    'Route 4 - Trainer: Backpacker Clifford in southeast': (810213, 1733, 'Route 4', None),
    'Route 4 - Trainer: Policeman Dell in north near Nimbasa Gate': (810214, 1734, 'Route 4', None),
    'Route 4 - Trainer: Policeman Neagle on central road': (810215, 1735, 'Route 4', None),
    'Route 4 - Trainer: Roughneck Joey in western fenced area': (810216, 1736, 'Route 4', None),
    'Route 4 - Trainer: Roughneck Silvester in northwest fenced area': (810217, 1737, 'Route 4', None),
    'Route 4 - Trainer: Biker Stanley in western fenced area': (810218, 1738, 'Route 4', None),
    'Route 4 - Trainer: Hooligans Rob & Sal on western street': (810220, 1740, 'Route 4', None),
    'Route 4 - Trainer: Rich Boy Keenan in west ruins': (810221, 1741, 'Route 4', None),
    'Route 4 - Trainer: Backpacker Roland in north near Nimbasa Gate': (810222, 1742, 'Route 4', None),
    'Route 4 - Trainer: Backpacker Rachel in east ruins': (810223, 1743, 'Route 4', None),
    'Route 4 - Trainer: Pokéfan Norbert in east': (810224, 1744, 'Route 4', None),
    'Route 4 - Trainer: Pokéfan Sachiko in northeast ruins': (810225, 1745, 'Route 4', None),
    'Route 4 - Trainer: Twins Tara & Val in central ruins': (810226, 1746, 'Route 4', None),
    'Route 4 - Trainer: Youngster Sinclair in western fenced area': (810284, 1804, 'Route 4', None),
    'Route 4 - Trainer: Breeder Irene in southern area': (810296, 1816, 'Route 4', None),
    'Route 4 - Trainer: Trainer Colress blocking north road': (810358, 1878, 'Route 4', None),

    # Route 5
    'Route 5 - Trainer: Backers Ava & Aya on road': (810252, 1772, 'Route 5', None),
    'Route 5 - Trainer: Baker Jenn on road': (810253, 1773, 'Route 5', None),
    'Route 5 - Trainer: Artist Horton above road': (810254, 1774, 'Route 5', None),
    'Route 5 - Trainer: Dancer Brian on road': (810255, 1775, 'Route 5', None),
    'Route 5 - Trainer: Musician Preston on road': (810256, 1776, 'Route 5', None),
    'Route 5 - Trainer: Ranger Lois above road': (810293, 1813, 'Route 5', None),
    'Route 5 - Trainer: Motorcyclist Charles on road (Bolt Badge)': (810339, 1859, 'Route 5', None, (1860,)),

    # Route 6
    'Route 6 - Trainer: Scientist Jacques (South of Season Research Lab)': (810263, 1783, 'Route 6', None),
    'Route 6 - Trainer: Scientist Marissa (Southwest of Season Research Lab)': (810264, 1784, 'Route 6', None),
    'Route 6 - Trainer: School Kid Alvin (West, near bridge)': (810265, 1785, 'Route 6', None),
    'Route 6 - Trainer: School Kid Mara (East, near central grass)': (810266, 1786, 'Route 6', None),
    'Route 6 - Trainer: Parasol Lady Nicole (Southeast)': (810267, 1787, 'Route 6', None),
    'Route 6 - Trainer: Parasol Lady Tihana (West, near Chargestone Cave)': (810268, 1788, 'Route 6', None),
    'Route 6 - Trainer: Ranger Richard (Behind Season Research Lab)': (810292, 1812, 'Route 6', None),
    'Route 6 - Trainer: Breeder April (South, near water)': (810752, 2272, 'Route 6', None),

    # Route 7
    'Route 7 - Trainer: Lass Flo (South, near southern grass)': (810269, 1789, 'Route 7', None),
    'Route 7 - Trainer: Youngster Cody (Southwest, near southern grass)': (810270, 1790, 'Route 7', None),
    'Route 7 - Trainer: Nursery Aide Hollie (West, south of northwestern grass)': (810271, 1791, 'Route 7', None),
    'Route 7 - Trainer: Preschooler Greg (Northwest, near northwestern grass)': (810272, 1792, 'Route 7', None),
    'Route 7 - Trainer: Preschooler Chrissy (North, south of Celestial Tower)': (810273, 1793, 'Route 7', None),
    'Route 7 - Trainer: Twins Sola & Ana (Northeast, near northern house)': (810274, 1794, 'Route 7', None),
    'Route 7 - Trainer: Harlequin Pat (East, near easternmost raised walkway)': (810275, 1795, 'Route 7', None),
    'Route 7 - Trainer: Harlequin Ian (Northeast, north of easternmost raised walkway)': (810276, 1796, 'Route 7', None),
    'Route 7 - Trainer: Breeder Marcus (Southwest corner)': (810302, 1822, 'Route 7', None),

    # Route 8
    'Route 8 - Trainer: Youngster Astor': (810571, 2091, 'Route 8', None),
    'Route 8 - Trainer: Lass Mai': (810572, 2092, 'Route 8', None),
    'Route 8 - Trainer: Parasol Lady Ingrid': (810573, 2093, 'Route 8', None),
    'Route 8 - Trainer: Parasol Lady Tyra': (810574, 2094, 'Route 8', None),
    'Route 8 - Trainer: Fisherman Ryder': (810575, 2095, 'Route 8', None),

    # Route 9
    'Route 9 - Trainer: Biker Zeke': (810219, 1739, 'Route 9', None),
    'Route 9 - Trainer: Hooligans Jim & Cas': (810328, 1848, 'Route 9', None),
    'Route 9 - Trainer: Roughneck Chance': (810329, 1849, 'Route 9', None),
    'Route 9 - Trainer: Roughneck Reese': (810330, 1850, 'Route 9', None),
    'Route 9 - Trainer: Biker Phillip': (810331, 1851, 'Route 9', None),

    # Seaside Cave
    'Seaside Cave - Trainer: Black Belt Drago': (810469, 1989, 'Seaside Cave', None),
    'Seaside Cave - Trainer: Battle Girl Tia': (810470, 1990, 'Seaside Cave', None),
    'Seaside Cave - Trainer: Black Belt Rich': (810471, 1991, 'Seaside Cave', None),
    'Seaside Cave - Trainer: Battle Girl Maki (Strength)': (810472, 1992, 'Seaside Cave', None),
    'Seaside Cave - Trainer: Ranger Johan': (810473, 1993, 'Seaside Cave', None),
    'Seaside Cave - Trainer: Ranger Mikiko': (810474, 1994, 'Seaside Cave', None),
    'Seaside Cave - Trainer: Black Belt Rocky': (810580, 2100, 'Seaside Cave', None),

    # Shopping Mall
    'Shopping Mall - Trainer: Waiter Lou': (810011, 1531, 'Shopping Mall', None),
    'Shopping Mall - Trainer: Waitress Olwen': (810012, 1532, 'Shopping Mall', None),

    # Strange House
    'Strange House - Trainer: Backpacker Boone (1F)': (810390, 1910, 'Strange House', None),
    'Strange House - Trainer: Psychic Lynette (2F)': (810391, 1911, 'Strange House', None),

    # Striaton City
    'Striaton City - Trainer: Ace Trainer Dusty': (810493, 2013, 'Striaton City', None),
    'Striaton City - Trainer: Striaton Trio Battle 1': (810494, 2014, 'Striaton City', None),
    'Striaton City - Trainer: Striaton Trio Battle 2': (810495, 2015, 'Striaton City', None),

    # Twist Mountain
    'Twist Mountain - Trainer: Worker Cliff': (810492, 2012, 'Twist Mountain', None),
    'Twist Mountain - Trainer: Worker Cairn': (810525, 2045, 'Twist Mountain', None),
    'Twist Mountain - Trainer: Worker Gus': (810526, 2046, 'Twist Mountain', None),
    'Twist Mountain - Trainer: Worker Victor': (810527, 2047, 'Twist Mountain', None),
    'Twist Mountain - Trainer: Worker Patton': (810528, 2048, 'Twist Mountain', None),
    'Twist Mountain - Trainer: Worker Ryan': (810529, 2049, 'Twist Mountain', None),
    'Twist Mountain - Trainer: Hiker Hunter': (810530, 2050, 'Twist Mountain', None),
    'Twist Mountain - Trainer: Hiker Wade': (810531, 2051, 'Twist Mountain', None),
    'Twist Mountain - Trainer: Veteran Zach': (810532, 2052, 'Twist Mountain', None),
    'Twist Mountain - Trainer: Veteran Julia': (810533, 2053, 'Twist Mountain', None),
    'Twist Mountain - Trainer: Veteran Carter': (810534, 2054, 'Twist Mountain', None),
    'Twist Mountain - Trainer: Veteran Chloris': (810535, 2055, 'Twist Mountain', None),
    'Twist Mountain - Trainer: Nurse Carol': (810725, 2245, 'Twist Mountain', None),

    # Undella Bay
    'Undella Bay - Trainer: Ace Trainer Summer': (810313, 1833, 'Undella Bay', None),
    'Undella Bay - Trainer: Swimmer (M) Matt': (810314, 1834, 'Undella Bay', None),
    'Undella Bay - Trainer: Swimmer (M) Bart': (810315, 1835, 'Undella Bay', None),
    'Undella Bay - Trainer: Swimmer (M) Tim': (810316, 1836, 'Undella Bay', None),
    'Undella Bay - Trainer: Swimmer (F) Arissa': (810317, 1837, 'Undella Bay', None),
    'Undella Bay - Trainer: Swimmer (F) Mitzi': (810318, 1838, 'Undella Bay', None),

    # Undella Town
    'Undella Town - Trainer: PkMn Trainer Hugh (Post-Game)': (810378, 1898, 'Undella Town', None, (1899, 1900)),
    'Undella Town - Trainer: Trainer Cynthia': (810456, 1976, 'Undella Town', None),
    'Undella Town - Trainer: PkMn Trainer Hugh': (810693, 2213, 'Undella Town', None, (2214, 2215)),

    # Victory road
    'Victory Road - Trainer: Ace Trainer Billy': (810594, 2114, 'Victory Road', None),
    'Victory Road - Trainer: Psychic Alia': (810595, 2115, 'Victory Road', None),
    'Victory Road - Trainer: Ace Trainer Jamie': (810596, 2116, 'Victory Road', None),
    'Victory Road - Trainer: Psychic Al': (810597, 2117, 'Victory Road', None),
    'Victory Road - Trainer: Ace Trainer Beckett (Outside 1 B2 / Grove W2)': (810598, 2118, 'Victory Road', None),
    'Victory Road - Trainer: Ace Trainer Shelly (Outside 1 B2 / Grove W2)': (810599, 2119, 'Victory Road', None),
    'Victory Road - Trainer: Veteran Cathy': (810600, 2120, 'Victory Road', None),
    'Victory Road - Trainer: Doctor Logan': (810601, 2121, 'Victory Road', None),
    'Victory Road - Trainer: Ace Trainer Webster (2F)': (810602, 2122, 'Victory Road', None),
    'Victory Road - Trainer: Ace Trainer Shanta (2F)': (810603, 2123, 'Victory Road', None),
    'Victory Road - Trainer: Veteran Sterling (Outside 2)': (810604, 2124, 'Victory Road', None),
    'Victory Road - Trainer: Veteran Portia (Outside 2)': (810605, 2125, 'Victory Road', None),
    'Victory Road - Trainer: Ace Trainer Caroll (Outside 2)': (810606, 2126, 'Victory Road', None),
    'Victory Road - Trainer: Black Belt Martell (Outside 2)': (810607, 2127, 'Victory Road', None),
    'Victory Road - Trainer: Ace Trainer Elmer (Outside 2)': (810608, 2128, 'Victory Road', None),
    'Victory Road - Trainer: Battle Girl Chalina (Outside 2)': (810609, 2129, 'Victory Road', None),
    'Victory Road - Trainer: Ace Trainer Pierce': (810610, 2130, 'Victory Road', None),
    'Victory Road - Trainer: Ace Trainer Chandra (Grove B2 / Outside 1 W2)': (810611, 2131, 'Victory Road', None),
    'Victory Road - Trainer: Veteran Hugo (3F)': (810612, 2132, 'Victory Road', None),
    'Victory Road - Trainer: Backpacker Mae': (810613, 2133, 'Victory Road', None),
    'Victory Road - Trainer: Veteran Claude (1F, Surf, Waterfall)': (810614, 2134, 'Victory Road', None),
    'Victory Road - Trainer: Veteran Cecile (1F, Surf, Waterfall)': (810615, 2135, 'Victory Road', None),
    'Victory Road - Trainer: Veteran Abraham (2F)': (810657, 2177, 'Victory Road', None),
    'Victory Road - Trainer: Ranger Eddie (2F)': (810658, 2178, 'Victory Road', None),
    'Victory Road - Trainer: Ranger Elle (2F)': (810659, 2179, 'Victory Road', None),
    'Victory Road - Trainer: PkMn Trainer Hugh (4F)': (810684, 2204, 'Victory Road', None, (2205, 2206)),

    # Village Bridge
    'Village Bridge - Trainer: Gentleman Stonewall': (810177, 1697, 'Village Bridge', None),
    'Village Bridge - Trainer: Baker Chris': (810335, 1855, 'Village Bridge', None),
    'Village Bridge - Trainer: Youngster Karl': (810336, 1856, 'Village Bridge', None),
    'Village Bridge - Trainer: Artist Gough': (810338, 1858, 'Village Bridge', None),
    'Village Bridge - Trainer: Fisherman Dean (Surf)': (810349, 1869, 'Village Bridge', None),
    'Village Bridge - Trainer: Hoopster Derrick': (810726, 2246, 'Village Bridge', None),
    'Village Bridge - Trainer: Smasher Lizzy': (810727, 2247, 'Village Bridge', None),
    'Village Bridge - Trainer: Smasher Amy': (810728, 2248, 'Village Bridge', None),
    'Village Bridge - Trainer: Hoopster Nicolas': (810729, 2249, 'Village Bridge', None),

    # Virbank City
    'Virbank City - Trainer: Team Plasma Grunt at harbour': (810690, 2210, 'Virbank City', None),

    # Virbank Complex
    'Virbank Complex - Trainer: Youngster Masahiro near inner complex entrance': (810745, 2265, 'Virbank Complex Inside', None),
    'Virbank Complex - Trainer: Worker Isaac in the southeast': (810203, 1723, 'Virbank Complex Inside', None),
    'Virbank Complex - Trainer: Worker Mitchell northeast on raised platform': (810204, 1724, 'Virbank Complex Inside', None),
    'Virbank Complex - Trainer: Worker Nathan in the west accessible from dropping off beams': (810205, 1725, 'Virbank Complex Inside', None),
    'Virbank Complex - Trainer: Lass Daya in the south': (810738, 2258, 'Virbank Complex Inside', None),
    'Virbank Complex - Trainer: Youngster Waylon raised in the northwest': (810746, 2266, 'Virbank Complex Inside', None),

    # Virbank Gym
    'Virbank Gym - Trainer: Roughneck Nicky': (810178, 1698, 'Virbank Gym', None, (270,)),
    'Virbank Gym - Trainer: Guitarist Billy Jo': (810179, 1699, 'Virbank Gym', None, (271,)),
    'Virbank Gym - Trainer: Gym Leader Roxie': (810157, 1677, 'Virbank Gym', None, (2285,)),

    # Wellspring Cave
    'Wellspring Cave - Trainer: Veteran Shaun (Surf, Flash)': (810042, 1562, 'Wellspring Cave', None),
    'Wellspring Cave - Trainer: Hiker Zaiem': (810674, 2194, 'Wellspring Cave', None),
    'Wellspring Cave - Trainer: Battle Girl Maggie': (810675, 2195, 'Wellspring Cave', None),
    'Wellspring Cave - Trainer: Battle Girl Xiao (Surf, Flash)': (810676, 2196, 'Wellspring Cave', None),
    'Wellspring Cave - Trainer: Black Belt Edward (Surf, Flash)': (810677, 2197, 'Wellspring Cave', None),
    'Wellspring Cave - Trainer: Black Belt Thomas (Surf, Flash)': (810678, 2198, 'Wellspring Cave', None),
}

