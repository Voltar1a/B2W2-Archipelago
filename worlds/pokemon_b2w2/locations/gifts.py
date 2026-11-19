from __future__ import annotations

# NPC gift checks (domain: 300000 + idx)
NPC_GIFT_LOCATIONS: dict[str, tuple[int, int | None, str | None, tuple[int, int] | None]] = {

    # Abundant Shrine
    'Abundant Shrine - Gift: Elder near Landorus shrine': (300215, 1710, 'Abundant Shrine', None),

    # Abyssal Ruins
    'Abyssal Ruins - Gift: 4F Central altar chamber crown': (300164, 1469, 'Abyssal Ruins', None),

    # Accumula Town
    'Accumula Town - Gift: Youngster in northwest building 1F': (300220, 2766, 'Accumula Town', None),
    'Accumula Town - Gift: Lass in northwest building 2F': (300221, 2767, 'Accumula Town', None),
    'Accumula Town - Gift: Man in northern building': (300223, 335, 'Accumula Town', None),
    'Accumula Town - Gift: Girl in northwest building': (300225, 337, 'Accumula Town', None),
    'Accumula Town - Gift: Pianist in northeastern house': (300228, 2335, 'Accumula Town', None),
    'Accumula Town - Gift: Man in building next to gate': (300322, 103, 'Accumula Town', None),

    # Anville Town
    'Anville Town - Gift: Railwayman in Lost and Found': (300311, 239, 'Anville Town', None),
    'Anville Town - Gift: Girl on platform after finding Pansage': (300321, 365, 'Anville Town', None),

    # Aspertia City
    'Aspertia City - Gift: Bianca at lookout': (300001, 2802, 'Aspertia City', None),
    'Aspertia City - Gift: Woman at Route 19 gate': (300002, 1703, 'Aspertia City', None),
    'Aspertia City - Gift: School Kid in Trainers\' School': (300003, 269, 'Aspertia City', None),
    'Aspertia City - Gift: Girl in northeast house after defeating Cheren': (300004, 277, 'Aspertia City', None),
    # HoF postgame gifts in s856 are bypassed when living_room_starter is enabled

    # Aspertia Gym
    'Aspertia Gym - Gift: Clyde': (300007, 115, 'Aspertia Gym', None),

    # Bridge Gates (placed in their respective route/city regions)
    'Gate - Gift: Clerk at Route 8 gate': (300197, 346, 'Route 8', None),
    'Gate - Gift: Roughneck at Route 16 gate': (300216, 385, 'Route 16', None),

    # Castelia City
    'Castelia City - Gift: Clerk at Bridge Gate': (300167, 442, 'Castelia City', None),
    'Castelia City - Gift: Harlequin near Prime Pier': (300047, 2338, 'Castelia City', None),
    'Castelia City - Gift: Harlequin after finding clowns': (300074, 2339, 'Castelia City', None),
    'Castelia City - Gift: Mode Street - Casteliacone stand lady': (300050, 2752, 'Castelia City', None),
    'Castelia City - Gift: Unity Pier - Girl': (300051, 443, 'Castelia City', None),
    'Castelia City - Gift: Gym Street - Man in Studio Castelia 1F': (300063, 2732, 'Castelia City', None),
    'Castelia City - Gift: Castelia Street - Woman in Battle Company 1F': (300065, 361, 'Castelia City', None),
    'Castelia City - Gift: Castelia Street - Battle Company president on 1F': (300068, 852, 'Castelia City', None),
    'Castelia City - Gift: Castelia Street - Scientist in Battle Company 47F': (300069, 143, 'Castelia City', None),
    'Castelia City - Gift: Castelia Street - Clerk in middle of Battle Company 47F': (300070, 362, 'Castelia City', None),
    'Castelia City - Gift: Castelia Street - Clerk in Battle Company 47F': (300071, 210, 'Castelia City', None),
    'Castelia City - Gift: North Street - Man in left building': (300072, 382, 'Castelia City', None),
    'Castelia City - Gift: Narrow Street - Waiter in cafe': (300075, 133, 'Castelia City', None),
    'Castelia City - Gift: North Street - Pokédex Scientist on 1F of right building': (300076, 244, 'Castelia City', None),

    # Castelia Gate
    'Castelia Gate - Gift: Bianca at Route 4 gate': (300073, 1706, 'Castelia Gate', None),

    # Castelia Gym
    'Castelia Gym - Gift: Clyde': (300049, 109, 'Castelia Gym', None),

    # Castelia Sewers
    'Castelia Sewers - Gift: Scientist in northern room (Spring/Summer, Surf)': (300281, 2781, 'Castelia Sewers', None),
    'Castelia Sewers - Gift: Scientist in room near Doctor': (300284, 2782, 'Castelia Sewers', None),

    # Celestial Tower
    'Celestial Tower - Gift: Professor Juniper on 1F': (300192, 766, 'Celestial Tower', None),

    # Chargestone Cave
    'Chargestone Cave - Gift: Nugget Brothers on B1F 1': (300153, 296, 'Chargestone Cave', None),
    'Chargestone Cave - Gift: Nugget Brothers on B1F 2': (300359, 2585, 'Chargestone Cave', None),

    # Desert Resort
    'Desert Resort - Gift: Man in black in sand pit': (300149, 216, 'Desert Resort', None),

    # Dragonspiral Tower
    'Dragonspiral Tower - Gift: Cedric at tower entrance': (300162, 2341, 'Dragonspiral Tower', None),

    # Dreamyard
    'Dreamyard - Gift: Soul Dew after battling Latios/Latias': (300365, 497, 'Dreamyard', None),

    # Driftveil City
    'Driftveil City - Gift: Clyde': (300108, 111, 'Driftveil City', None),
    'Driftveil City - Gift: Girl on upper floor of Pokemon Center': (300109, 122, 'Driftveil City', None),
    'Driftveil City - Gift: Old man on 1F of Grand Hotel Driftveil': (300112, 319, 'Driftveil City', None),
    'Driftveil City - Gift: Lady on 1F of Driftveil Luxury Suites (TM move)': (300113, 2759, 'Driftveil City', None),
    'Driftveil City - Gift: Man in black at market': (300117, 324, 'Driftveil City', None),
    'Driftveil City - Gift: Gentleman on 25F of Driftveil Chateau Hotel': (300301, 318, 'Driftveil City', None),
    'Driftveil City - Gift: Axew on 19F of Grand Hotel Driftveil': (300302, 320, 'Driftveil City', None),
    'Driftveil City - Gift: Waiter on 23F of Driftveil Luxury Suites': (300303, 322, 'Driftveil City', None),
    'Driftveil City - Gift: Veteran on 25F of Driftveil Continental Hotel': (300304, 323, 'Driftveil City', None),

    # Driftveil Drawbridge
    'Driftveil Drawbridge - Gift: Youngster on bridge': (300169, 282, 'Driftveil Drawbridge', None),

    # Floccesy Ranch
    'Floccesy Ranch - Gift: After battling Hugh': (300017, 2343, 'Floccesy Ranch', None),
    'Floccesy Ranch - Gift: Hugh in northwest': (300018, 2344, 'Floccesy Ranch', None),

    # Floccesy Town
    'Floccesy Town - Gift: Old man in house east of Pokemon Center': (300009, 278, 'Floccesy Town', None),
    'Floccesy Town - Gift: Mr Medal after defeating School Kids': (300010, 267, 'Floccesy Town', None),
    'Floccesy Town - Gift: Bianca after defeating Cheren': (300011, 2345, 'Floccesy Town', None),

    # Giant Chasm
    'Giant Chasm - Gift: Rood after defeating Plasma Grunt': (300163, 2346, 'Giant Chasm', None),
    'Giant Chasm - Gift: DNA Splicers after defeating Ghetsis': (300310, 481, 'Giant Chasm', None),

    # Humilau City
    'Humilau City - Gift: Couple after Celestial Tower bell': (300271, 2347, 'Humilau City', None),
    'Humilau City - Gift: Nurse in northeastern house': (300272, 342, 'Humilau City', None),
    'Humilau City - Gift: Socialite in house near Route 22': (300274, 2768, 'Humilau City', None),

    # Humilau Gym
    'Humilau Gym - Gift: Clyde': (300278, 117, 'Humilau Gym', None),

    # Icirrus City
    'Icirrus City - Gift: Battle Girl in Pokemon Center': (300123, 120, 'Icirrus City', None),
    'Icirrus City - Gift: Fan Club Chairman 1': (300126, 201, 'Icirrus City', None),
    'Icirrus City - Gift: Fan Club Chairman 2': (300366, 202, 'Icirrus City', None),
    'Icirrus City - Gift: Fan Club Chairman 3': (300367, 203, 'Icirrus City', None),

    # Lacunosa Town
    'Lacunosa Town - Gift: Executive in northeast house (Night)': (300232, 2784, 'Lacunosa Town', None),

    # Lentimas Town
    'Lentimas Town - Gift: Old woman in Pokemon Center': (300268, 294, 'Lentimas Town', None),

    # Marine Tube
    'Marine Tube - Gift: Female Ace Trainer': (300270, 389, 'Marine Tube', None),

    # Mistralton City
    'Mistralton City - Gift: Professor Juniper on runway': (300118, 1707, 'Mistralton City', None),
    'Mistralton City - Gift: Veteran in Cargo Service building': (300358, 121, 'Mistralton City', None),
    'Mistralton City - Gift: Pilot in Cargo Service building': (300120, 472, 'Mistralton City', None),
    'Mistralton City - Gift: TM collector in Pokemon Center (10 TMs)': (300313, 450, 'Mistralton City', None),
    'Mistralton City - Gift: TM collector in Pokemon Center (20 TMs)': (300314, 451, 'Mistralton City', None),
    'Mistralton City - Gift: TM collector in Pokemon Center (35 TMs)': (300121, 452, 'Mistralton City', None),
    'Mistralton City - Gift: TM collector in Pokemon Center (50 TMs)': (300315, 453, 'Mistralton City', None),
    'Mistralton City - Gift: TM collector in Pokemon Center (70 TMs)': (300316, 454, 'Mistralton City', None),
    'Mistralton City - Gift: TM collector in Pokemon Center (95 TMs)': (300317, 455, 'Mistralton City', None),

    # Mistralton Gym
    'Mistralton Gym - Gift: Clyde': (300357, 112, 'Mistralton Gym', None),

    # Musical Theater
    'Musical Theater - Gift: Owner at theater entrance': (300099, 2350, 'Musical Theater', None),

    # N's Castle
    'N\'s Castle - Gift: 5F, N after the first battle': (300175, 1708, 'N\'s Castle', None),

    # Nacrene City
    'Nacrene City - Gift: Lenora in museum': (300036, 445, 'Nacrene City', None),
    'Nacrene City - Gift: Waitress in Cafe Warehouse (Wed/Sat)': (300043, 2735, 'Nacrene City', None),
    'Nacrene City - Gift: Customer in Cafe Warehouse (Sun/Thu)': (300046, 2353, 'Nacrene City', None),

    # Nimbasa City
    'Nimbasa City - Gift: Rosa/Nate at Battle Subway entrance': (300077, 764, 'Nimbasa City', None),
    'Nimbasa City - Gift: Clyde': (300078, 110, 'Nimbasa City', None),
    'Nimbasa City - Gift: Socialite in northwest building': (300081, 305, 'Nimbasa City', None),
    'Nimbasa City - Gift: Madame in northwest building': (300105, 262, 'Nimbasa City', None),
    'Nimbasa City - Gift: Ace Trainer in 2F of northwestern building': (300107, 213, 'Nimbasa City', None),
    'Nimbasa City - Gift: Woman in old Gym': (300364, 459, 'Nimbasa City', None),

    # Nuvema Town
    'Nuvema Town - Gift: Cheren\'s father': (300218, 413, 'Nuvema Town', None),
    'Nuvema Town - Gift: Cedric Juniper': (300363, 2437, 'Nuvema Town', None),

    # Opelucid City
    'Opelucid City - Gift: Clyde': (300129, 114, 'Opelucid City', None),
    'Opelucid City - Gift: Linebacker on 2F of Drayden\'s house': (300132, 240, 'Opelucid City', None),
    'Opelucid City - Gift: Woman on 2F of Drayden\'s house': (300133, 241, 'Opelucid City', None),
    'Opelucid City - Gift: Woman in house east of Gym': (300138, 236, 'Opelucid City', None),

    # P2 Laboratory
    'P2 Laboratory - Gift: Scientist Dudley 1': (300319, 2443, 'P2 Laboratory', None),
    'P2 Laboratory - Gift: Scientist Dudley 2': (300320, 2461, 'P2 Laboratory', None),

    # Pinwheel Forest
    'Pinwheel Forest - Gift: Ranger near Challenge Rock': (300142, 2760, 'Pinwheel Forest', None),
    'Pinwheel Forest - Gift: Cheren after meeting Gorm': (300144, 908, 'Pinwheel Forest', None),
    'Pinwheel Forest - Gift: Scientist after Habitat List': (300148, 470, 'Pinwheel Forest', None),

    # Plasma Frigate
    'Plasma Frigate - Gift: Colress in bridge chamber': (300306, 429, 'Plasma Frigate', None),

    # Pokémon League

    # PWT
    'PWT - Gift: Worker southeast of fountain': (300312, 448, 'PWT', None),

    # Reversal Mountain

    # Route 1
    'Route 1 - Gift: Woman in second patch of tall grass': (300362, 425, 'Route 1', None),

    # Route 11
    'Route 11 - Gift: Ranger inside trailer': (300207, 384, 'Route 11', None),

    # Route 13
    'Route 13 - Gift: Flute gentleman on beach 1': (300208, 2738, 'Route 13', None),
    'Route 13 - Gift: Girl on cliff near house': (300213, 304, 'Route 13', None),

    # Route 16
    'Route 16 - Gift: Man in Nimbasa Gate': (300106, 263, 'Route 16', None),

    # Route 18
    'Route 18 - Gift: Northern cliff east of Veteran Chester': (300368, 943, 'Route 18', None),

    # Route 19
    'Route 19 - Gift: Alder after Floccesy events': (300008, 2361, 'Route 19', None),

    # Route 2
    'Route 2 - Gift: Lady east of Youngster Mikey': (300179, 2362, 'Route 2', None),

    # Route 20
    'Route 20 - Gift: Cheren near dark grass': (300012, 2363, 'Route 20', None),

    # Route 22
    'Route 22 - Gift: Colress at Terrakion plateau': (300279, 2364, 'Route 22', None),

    # Route 3
    'Route 3 - Gift: School Kid after Habitat List': (300180, 471, 'Route 3', None),

    # Route 4
    'Route 4 - Gift: Colress after battle': (300181, 1705, 'Route 4', None),
    'Route 4 - Gift: Ace Trainer in house': (300182, 2772, 'Route 4', None),
    'Route 4 - Gift: Black Belt in first left house': (300288, 386, 'Route 4', None),
    'Route 4 - Gift: Maid in house (Guess Pokémon cry)': (300289, 363, 'Route 4', None),

    # Route 5
    'Route 5 - Gift: Item bought from Breeder': (300186, 2751, 'Route 5', None),

    # Route 6
    'Route 6 - Gift: Girl in house near Hiker': (300190, 383, 'Route 6', None),

    # Route 8
    'Route 8 - Gift: Parasol lady near puddles 2': (300195, 2749, 'Route 8', None),

    # Shopping Mall
    'Shopping Mall - Gift: Lady in bottom section': (300200, 2765, 'Shopping Mall', None),

    # Skyarrow Bridge
    'Skyarrow Bridge - Gift: Runner after bridge quest': (300166, 2586, 'Skyarrow Bridge', None),

    # Strange House
    'Strange House - Gift: Ghost girl in bedroom': (300287, 899, 'Strange House', None),

    # Striaton City
    'Striaton City - Gift: Fisherman left of Route 3 gate (Surf)': (300028, 140, 'Striaton City', None),
    'Striaton City - Gift: Roughneck in eastmost alley': (300361, 142, 'Striaton City', None),
    'Striaton City - Gift: Chef in restaurant': (300030, 2777, 'Striaton City', None),
    'Striaton City - Gift: Girl in Pokemon Center': (300033, 381, 'Striaton City', None),
    'Striaton City - Gift: Man on 1F of lower east apartment': (300034, 104, 'Striaton City', None),
    'Striaton City - Gift: Schoolboy quiz in Trainers\' School': (300035, 355, 'Striaton City', None),

    # Twist Mountain
    'Twist Mountain - Gift: Fossil worker in cave 5': (300159, 2747, 'Twist Mountain', None),

    # Undella Town
    'Undella Town - Gift: Man in Pokemon Center': (300235, 295, 'Undella Town', None),
    'Undella Town - Gift: Zinzolin in front of gate': (300360, 2803, 'Undella Town', None),

    # Victory road

    # Village Bridge
    'Village Bridge - Gift: Girl near restaurant': (300170, 468, 'Village Bridge', None),
    'Village Bridge - Gift: Baker after battle (Post-Game)': (300171, 457, 'Village Bridge', None),
    'Village Bridge - Gift: Fisherman by river': (300318, 299, 'Village Bridge', None),

    # Virbank City
    'Virbank City - Gift: Attendant in Route 20 gate': (300019, 2367, 'Virbank City', None),
    'Virbank City - Gift: Nursery Aide in the nursery': (300020, 279, 'Virbank City', None),
    'Virbank City - Gift: Roughneck in front of Gym': (300021, 492, 'Virbank City', None),

    # Virbank Complex
    'Virbank Complex - Gift: Roughneck trading Poke Ball for Great Ball': (300023, 2763, 'Virbank Complex', None),

    # Virbank Complex Inside
    'Virbank Complex - Gift: Scientist after talking to him three times': (300024, 310, 'Virbank Complex Inside', None),
    'Virbank Complex - Gift: Girl at southernmost end after filling Habitat List': (300025, 467, 'Virbank Complex Inside', None),

    # Virbank Gym
    'Virbank Gym - Gift: Clyde': (300022, 116, 'Virbank Gym', None),

    # Pokemon Ranger post-battle Berry gifts
    'Chargestone Cave - Gift: Ranger Briana (B1F, southeast)': (300323, 2467, 'Chargestone Cave', None),
    'Chargestone Cave - Gift: Ranger Louis (1F, south)': (300324, 2469, 'Chargestone Cave', None),
    'Clay Tunnel - Gift: Ranger Katie in Room 3 north (Surf)': (300325, 2471, 'Clay Tunnel', None),
    'Clay Tunnel - Gift: Ranger Maxwell in Room 3 south': (300326, 2472, 'Clay Tunnel', None),
    'Desert Resort - Gift: Ranger Anja in east': (300327, 2473, 'Desert Resort', None),
    'Desert Resort - Gift: Ranger Jaden near entrance': (300328, 2475, 'Desert Resort', None),
    'Lostlorn Forest - Gift: Ranger Forrest in north': (300329, 2479, 'Lostlorn Forest', None),
    'Lostlorn Forest - Gift: Ranger Serenity in west': (300330, 2483, 'Lostlorn Forest', None),
    'Moor of Icirrus - Gift: Ranger Elaine': (300331, 2484, 'Moor of Icirrus', None),
    'Moor of Icirrus - Gift: Ranger Parker': (300332, 2488, 'Moor of Icirrus', None),
    'Pinwheel Forest - Gift: Ranger Dwayne': (300333, 2491, 'Pinwheel Forest', None),
    'Pinwheel Forest - Gift: Ranger Hillary': (300334, 2492, 'Pinwheel Forest', None),
    'Pinwheel Forest - Gift: Ranger Melita': (300335, 2493, 'Pinwheel Forest', None),
    'Pinwheel Forest - Gift: Ranger Ralph': (300336, 2501, 'Pinwheel Forest', None),
    'Reversal Mountain - Gift: Ranger Eliza (1F B2 / 2F W2)': (300337, 2507, 'Reversal Mountain', None),
    'Reversal Mountain - Gift: Ranger Lewis (2F B2 / 1F W2)': (300338, 2511, 'Reversal Mountain', None),
    'Route 1 - Gift: Ranger Audra': (300339, 2515, 'Route 1', None),
    'Route 1 - Gift: Ranger Rick': (300340, 2516, 'Route 1', None),
    'Route 11 - Gift: Ranger Crofton': (300341, 2517, 'Route 11', None),
    'Route 11 - Gift: Ranger Thalia (Surf, Waterfall)': (300342, 2519, 'Route 11', None),
    'Route 13 - Gift: Ranger Daryl': (300343, 2520, 'Route 13', None),
    'Route 13 - Gift: Ranger Dianne': (300344, 2523, 'Route 13', None),
    'Route 20 - Gift: Pokemon Ranger Bret on central island (Basic Badge, Autumn, Surf)': (300345, 2529, 'Route 20', None),
    'Route 20 - Gift: Pokemon Ranger Leaf on southeast island (Basic Badge, Autumn, Surf)': (300346, 2535, 'Route 20', None),
    'Route 20 - Gift: Pokemon Ranger Malory on eastern island (Basic Badge, Autumn, Surf)': (300347, 2536, 'Route 20', None),
    'Route 20 - Gift: Pokemon Ranger Naoko above waterfall (Basic Badge, Autumn, Surf, Waterfall)': (300348, 2537, 'Route 20', None),
    'Route 23 - Gift: Ranger Lena': (300349, 2540, 'Route 23', None),
    'Route 23 - Gift: Ranger Steve': (300350, 2544, 'Route 23', None),
    'Route 5 - Gift: Ranger Lois above road': (300351, 2549, 'Route 5', None),
    'Route 6 - Gift: Ranger Richard (Behind Season Research Lab)': (300352, 2551, 'Route 6', None),
    'Seaside Cave - Gift: Ranger Johan': (300353, 2567, 'Seaside Cave', None),
    'Seaside Cave - Gift: Ranger Mikiko': (300354, 2568, 'Seaside Cave', None),
    'Victory Road - Gift: Ranger Eddie (2F)': (300355, 2572, 'Victory Road', None),
    'Victory Road - Gift: Ranger Elle (2F)': (300356, 2577, 'Victory Road', None),

}

# Gym badges (domain: 400001..400008, flag = 2414 + badge_idx)
BADGE_LOCATIONS: dict[str, tuple[int, int | None, str | None, tuple[int, int] | None]] = {

    # Aspertia Gym
    'Aspertia Gym - Gym Leader Cheren Basic Badge': (400001, 1676, 'Aspertia Gym', None, (2284,)),

    # Castelia City
    'Castelia Gym - Gym Leader Burgh Insect Badge': (400003, 1674, 'Castelia City', None, (2286,)),

    # Driftveil City
    'Driftveil Gym - Gym Leader Clay Quake Badge': (400005, 1678, 'Driftveil City', None, (2288,)),

    # Humilau City
    'Humilau Gym - Gym Leader Marlon Wave Badge': (400008, 1680, 'Humilau City', None, (2291,)),

    # Mistralton City
    'Mistralton Gym - Gym Leader Skyla Jet Badge': (400006, 1675, 'Mistralton City', None, (2289,)),

    # Nimbasa City
    'Nimbasa Gym - Gym Leader Elesa Bolt Badge': (400004, 1673, 'Nimbasa City', None, (2287,)),

    # Opelucid City
    'Opelucid Gym - Gym Leader Drayden Legend Badge': (400007, 1679, 'Opelucid City', None, (2290,)),

    # Virbank Gym
    'Virbank Gym - Gym Leader Roxie Toxic Badge': (400002, 1677, 'Virbank Gym', None, (2285,)),
}

# Story / gym TM & HM rewards (domain: 500000 + TM/HM num)
TM_REWARD_LOCATIONS: dict[str, tuple[int, int | None, str | None, tuple[int, int] | None]] = {

    # Aspertia City
    'Aspertia City - Gift: Bianca after defeating Cheren': (500027, 2368, 'Aspertia City', None),

    # Aspertia Gym
    'Aspertia Gym - Gift: Cheren after defeating Gym': (500083, 2377, 'Aspertia Gym', None),

    # Castelia City
    'Castelia City - Gift: North Street - Guitarist in building 11F': (500044, 209, 'Castelia City', None),
    'Castelia City - Gift: North Street - Party girl in building 47F': (500045, 416, 'Castelia City', None),
    'Castelia City - Gift: Narrow Street - Security Guard': (500070, 2369, 'Castelia City', None),
    'Castelia City - Gift: Burgh after defeating Gym': (500076, 2379, 'Castelia City', None),

    # Castelia Sewers
    'Castelia Sewers - Gift: Hugh after defeating Team Plasma near Relic Passage': (500004, 2370, 'Castelia Sewers', None),

    # Driftveil City
    'Driftveil City - Gift: Clay after defeating Gym': (500078, 2381, 'Driftveil City', None),

    # Floccesy Ranch
    'Floccesy Ranch - Gift: Team Plasma Grunt at the end of forest': (500021, 2371, 'Floccesy Ranch', None),

    # Humilau City
    'Humilau City - Gift: Marlon after defeating Gym': (500055, 2384, 'Humilau City', None),

    # Lentimas Town
    'Lentimas Town - Gift: Woman in house near girl with Krokorok': (500057, 118, 'Lentimas Town', None),

    # Lostlorn Forest
    'Lostlorn Forest - Gift: Backpacker in northern clearing': (500095, 967, 'Lostlorn Forest', None),

    # Marine Tube
    'Marine Tube - Gift: Parasol Lady at Humilau City entrance': (500042, 343, 'Marine Tube', None),

    # Mistralton City
    'Mistralton City - Gift: Skyla after defeating Gym': (500062, 2382, 'Mistralton City', None),

    # Musical Theater
    'Musical Theater - Gift: Lady next to reception counter': (500049, 211, 'Musical Theater', None),

    # Nimbasa City
    'Nimbasa City - Gift: Elesa after defeating Gym': (500072, 2380, 'Nimbasa City', None),

    # Opelucid City
    'Opelucid City - Gift: Drayden after defeating Gym': (500082, 2383, 'Opelucid City', None),

    # Reversal Mountain
    'Reversal Mountain - Gift: Scientist after Habitat List': (500054, 469, 'Reversal Mountain', None),

    # Route 23
    'Route 23 - Gift: Ace Trainer in house': (500035, 473, 'Route 23', None),

    # Route 5
    'Route 5 - Gift: Bianca': (500002, 2373, 'Route 5', None),

    # Route 6
    'Route 6 - Gift: Cheren after PWT Plasma Frigate': (500003, 2439, 'Route 6', None),

    # Tubeline Bridge
    'Tubeline Bridge - Gift: Battle Girl on bridge': (500043, 345, 'Tubeline Bridge', None),

    # Undella Town
    'Undella Town - Gift: Hugh in front of Marine Tube gate': (500006, 414, 'Undella Town', None),

    # Victory road
    'Victory Road - Gift: N at badge check gates': (500005, 2374, 'Victory Road', None),
    'Victory Road - Gift: Hugh': (500024, 2375, 'Victory Road', None),

    # Virbank City
    'Virbank City - Gift: Roxie after defeating Team Plasma Grunt': (500001, 1704, 'Virbank City', None),

    # Virbank Complex Inside
    'Virbank Complex Inside - Gift: Man at entrance after defeating all three Workers': (500094, 465, 'Virbank Complex Inside', None),

    # Virbank Gym
    'Virbank Gym - Gift: Roxie after defeating Gym': (500009, 2378, 'Virbank Gym', None),
}
