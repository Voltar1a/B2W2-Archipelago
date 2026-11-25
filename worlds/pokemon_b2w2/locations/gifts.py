from __future__ import annotations

# NPC gift checks (domain: 300000 + idx)
NPC_GIFT_LOCATIONS: dict[str, tuple[int, int | None, str | None, tuple[int, int] | None]] = {

    # Abundant Shrine
    'Abundant Shrine - Elder near Landorus shrine': (300215, 1710, 'Abundant Shrine', None),

    # Abyssal Ruins
    'Abyssal Ruins 4F - central altar chamber crown': (300164, 1469, 'Abyssal Ruins', None),

    # Accumula Town
    'Accumula Town - Youngster in southwest': (300220, 2766, 'Accumula Town', None),
    'Accumula Town - Lass in northeast': (300221, 2767, 'Accumula Town', None),
    'Accumula Town - Man in northern building 2F': (300223, 335, 'Accumula Town', None),
    'Accumula Town - Girl in northwest building 2F after quiz': (300225, 337, 'Accumula Town', None),
    'Accumula Town - Pianist in northeastern house': (300228, 2335, 'Accumula Town', None),
    'Accumula Town - Man in northwest building 2F': (300322, 103, 'Accumula Town', None),

    # Anville Town
    'Anville Town - Railwayman in southeast house': (300311, 239, 'Anville Town', None),
    'Anville Town - Girl on platform after talking, finding Pansage outside Musical Theatre, then talking again': (300321, 365, 'Anville Town', None),

    # Aspertia City
    'Aspertia City - Bianca': (300001, 2802, 'Aspertia City', None),
    'Aspertia City - Woman at Route 19 gate': (300002, 1703, 'Aspertia City', None),
    'Aspertia City - School Kid in Trainers\' School': (300003, 269, 'Aspertia City', None),
    'Aspertia City - Girl in northeast house after defeating Cheren': (300004, 277, 'Aspertia City', None),
    # HoF postgame gifts in s856 are bypassed when living_room_starter is enabled - issues so excluded

    # Aspertia Gym
    'Aspertia Gym - Clyde': (300007, 115, 'Aspertia Gym', None),

    # Castelia City
    'Castelia City - Clerk at Bridge Gate': (300167, 442, 'Castelia City', None),
    'Castelia City - Oceanfront Road - Harlequin near Prime Pier': (300047, 2338, 'Castelia City', None),
    'Castelia City - Oceanfront Road - Harlequin after finding clowns': (300074, 2339, 'Castelia City', None),
    'Castelia City - Mode Street - Casteliacone stand lady': (300050, 2752, 'Castelia City', None),
    'Castelia City - Unity Pier - Girl': (300051, 443, 'Castelia City', None),
    'Castelia City - Gym Street - Man in Studio Castelia 1F': (300063, 2732, 'Castelia City', None),
    'Castelia City - Castelia Street - Woman in Battle Company 1F': (300065, 361, 'Castelia City', None),
    'Castelia City - Castelia Street - Battle Company president on 1F': (300068, 852, 'Castelia City', None),
    'Castelia City - Castelia Street - Scientist in Battle Company 47F': (300069, 143, 'Castelia City', None),
    'Castelia City - Castelia Street - Clerk in middle of Battle Company 47F': (300070, 362, 'Castelia City', None),
    'Castelia City - Castelia Street - Clerk in Battle Company 47F': (300071, 210, 'Castelia City', None),
    'Castelia City - North Street - Man in left building 1F': (300072, 382, 'Castelia City', None),
    'Castelia City - Narrow Street - Waiter in café': (300075, 133, 'Castelia City', None),
    'Castelia City - North Street - Pokédex Scientist on 1F of right building': (300076, 244, 'Castelia City', None),

    # Castelia Gate
    'Castelia Gate - Bianca at Route 4 gate': (300073, 1706, 'Castelia Gate', None),

    # Castelia Gym
    'Castelia Gym - Clyde': (300049, 109, 'Castelia Gym', None),

    # Castelia Sewers
    'Castelia Sewers - Scientist in northern room (Spring/Summer + Surf)': (300281, 2781, 'Castelia Sewers - Water', None),
    'Castelia Sewers - Scientist in room near Doctor': (300284, 2782, 'Castelia Sewers', None),

    # Celestial Tower
    'Celestial Tower 1F - Professor Juniper': (300192, 1711, 'Celestial Tower', None),

    # Chargestone Cave
    'Chargestone Cave B1F - Nugget Brothers 1': (300153, 296, 'Chargestone Cave - Past Bridge', None),
    'Chargestone Cave B1F - Nugget Brothers 2': (300359, 2585, 'Chargestone Cave - Past Bridge', None),

    # Desert Resort
    'Desert Resort - Man in black in sand pit in the east': (300149, 216, 'Desert Resort', None),

    # Dragonspiral Tower
    'Dragonspiral Tower - Cedric at tower entrance': (300162, 2341, 'Dragonspiral Tower', None),

    # Dreamyard
    'Dreamyard - Northern area: Soul Dew after battling Latios/Latias on 2F southeastern ruins after chase': (300365, 497, 'Dreamyard - Cut Area', None),

    # Driftveil City
    'Driftveil City - Clyde': (300108, 111, 'Driftveil City', None),
    'Driftveil City - Girl on upper floor of Pokémon Center': (300109, 122, 'Driftveil City', None),
    'Driftveil City - Old man on 1F of Grand Hotel Driftveil': (300112, 319, 'Driftveil City', None),
    'Driftveil City - Lady on 1F of Driftveil Luxury Suites (TM move)': (300113, 2759, 'Driftveil City', None),
    'Driftveil City - Man in black at market': (300117, 324, 'Driftveil City', None),
    'Driftveil City - Gentleman on 25F of Driftveil Chateau Hotel': (300301, 318, 'Driftveil City', None),
    'Driftveil City - Axew on 19F of Grand Hotel Driftveil': (300302, 320, 'Driftveil City', None),
    'Driftveil City - Waiter on 23F of Driftveil Luxury Suites': (300303, 322, 'Driftveil City', None),
    'Driftveil City - Veteran on 25F of Driftveil Continental Hotel': (300304, 323, 'Driftveil City', None),

    # Driftveil Drawbridge
    'Driftveil Drawbridge - Youngster on west of bridge': (300169, 282, 'Driftveil Drawbridge', None),

    # Floccesy Ranch
    'Floccesy Ranch - After battling Hugh': (300017, 2343, 'Floccesy Ranch', None),
    'Floccesy Ranch - Hugh in northwest': (300018, 2344, 'Floccesy Ranch', None),

    # Floccesy Town
    'Floccesy Town - Old man in house east of Pokémon Center': (300009, 278, 'Floccesy Town', None),
    'Floccesy Town - Mr. Medal after defeating School Kids': (300010, 267, 'Floccesy Town', None),
    'Floccesy Town - Bianca after defeating Cheren': (300011, 2345, 'Floccesy Town', None),

    # Giant Chasm
    'Giant Chasm - Crater, Rood after defeating Plasma Grunt': (300163, 2346, 'Giant Chasm', None),
    'Giant Chasm - Crater, DNA Splicers after defeating Ghetsis': (300310, 481, 'Giant Chasm - Post-Frigate', None),

    # Humilau City
    'Humilau City - Couple outside Pokémon Center after ringing Celestial Tower bell': (300271, 2347, 'Humilau City', None),
    'Humilau City - Nurse in northeastern house': (300272, 342, 'Humilau City', None),
    'Humilau City - Socialite in northwestern house near Route 22 after walking Mienfoo': (300274, 2768, 'Humilau City', None),

    # Humilau Gym
    'Humilau Gym - Clyde': (300278, 117, 'Humilau Gym', None),

    # Icirrus City
    'Icirrus City - Battle Girl in Pokémon Center': (300123, 120, 'Icirrus City', None),
    'Icirrus City - Fan Club Chairman in western house 1': (300126, 201, 'Icirrus City', None),
    'Icirrus City - Fan Club Chairman in western house 2': (300366, 202, 'Icirrus City', None),
    'Icirrus City - Fan Club Chairman in western house 3': (300367, 203, 'Icirrus City', None),

    # Lacunosa Town
    'Lacunosa Town - Executive in northeast raised house': (300232, 2784, 'Lacunosa Town', None),

    # Lentimas Town
    'Lentimas Town - Old woman in Pokémon Center': (300268, 294, 'Lentimas Town', None),

    # Marine Tube
    'Marine Tube - Female Ace Trainer in middle': (300270, 389, 'Marine Tube', None),

    # Mistralton City
    'Mistralton City - Professor Juniper on runway': (300118, 1707, 'Mistralton City', None),
    'Mistralton City - Veteran in Cargo Service building': (300358, 121, 'Mistralton City', None),
    'Mistralton City - Pilot in Cargo Service building': (300120, 472, 'Mistralton City', None),
    'Mistralton City - TM collector in house east of Pokémon Center (10 TMs)': (300313, 450, 'Mistralton City', None),
    'Mistralton City - TM collector in house east of Pokémon Center (20 TMs)': (300314, 451, 'Mistralton City', None),
    'Mistralton City - TM collector in house east of Pokémon Center (35 TMs)': (300121, 452, 'Mistralton City', None),
    'Mistralton City - TM collector in house east of Pokémon Center (50 TMs)': (300315, 453, 'Mistralton City', None),
    'Mistralton City - TM collector in house east of Pokémon Center (70 TMs)': (300316, 454, 'Mistralton City', None),
    'Mistralton City - TM collector in house east of Pokémon Center (95 TMs)': (300317, 455, 'Mistralton City', None),

    # Mistralton Gym
    'Mistralton Gym - Clyde': (300357, 112, 'Mistralton Gym', None),

    # Musical Theater
    'Musical Theatre - Owner at theatre entrance': (300099, 2350, 'Musical Theater', None),

    # N's Castle
    'N\'s Castle 5F - N after the first battle': (300175, 1708, 'N\'s Castle', None),

    # Nacrene City
    'Nacrene City - Lenora in museum': (300036, 445, 'Nacrene City', None),
    'Nacrene City - Waitress by entrance inside of Café Warehouse (Wed/Sat)': (300043, 2735, 'Nacrene City', None),
    'Nacrene City - Waitress in lower section of Café Warehouse (Sun)': (300372, 2561, 'Nacrene City', None),
    'Nacrene City - Waitress in lower section of Café Warehouse (Sun/Thu)': (300046, 2353, 'Nacrene City', None),

    # Nimbasa City
    'Nimbasa City - Rosa/Nate at Battle Subway entrance': (300077, 764, 'Nimbasa City', None),
    'Nimbasa City - Clyde': (300078, 110, 'Nimbasa City', None),
    'Nimbasa City - Gentleman in the Pokémon Center': (300081, 305, 'Nimbasa City', None),
    'Nimbasa City - Madame in 2F of northwest building': (300105, 262, 'Nimbasa City', None),
    'Nimbasa City - Ace Trainer in 2F of northwestern building': (300107, 213, 'Nimbasa City', None),
    'Nimbasa City - Beauty at end of old Gym': (300364, 459, 'Nimbasa City', None),

    # Nuvema Town
    'Nuvema Town - Cheren\'s father in bottom right house': (300218, 413, 'Nuvema Town', None),
    'Nuvema Town - Cedric Juniper in northwest Juniper Pokémon Lab': (300363, 2437, 'Nuvema Town', None),

    # Opelucid City
    'Opelucid City - Clyde': (300129, 114, 'Opelucid City', None),
    'Opelucid City - Linebacker on 2F of Drayden\'s house': (300132, 240, 'Opelucid City', None),
    'Opelucid City - Woman on 2F of Drayden\'s house': (300133, 241, 'Opelucid City', None),
    'Opelucid City - Woman in house east of Gym': (300138, 236, 'Opelucid City', None),

    # P2 Laboratory
    'P2 Laboratory - Scientist Dudley 1': (300319, 2443, 'P2 Laboratory', None),
    'P2 Laboratory - Scientist Dudley 2': (300320, 2461, 'P2 Laboratory', None),

    # Pinwheel Forest
    'Pinwheel Forest - Outside: Challenge Rock (Fighting-type)': (300142, 2760, 'Pinwheel Forest', None),
    'Pinwheel Forest - Inside: Cheren in northeast inner forest after meeting Gorm': (300144, 908, 'Pinwheel Forest', None),
    'Pinwheel Forest - Inside: Scientist after Habitat List south': (300148, 470, 'Pinwheel Forest', None),

    # Plasma Frigate
    'Plasma Frigate - Colress in bridge chamber (P2 Lab)': (300306, 429, 'Plasma Frigate (P2 Laboratory)', None),
    'Plasma Frigate - Gift from Team Plasma Password Grunt north of beam puzzle pit (from Giant Chasm)': (300375, 356, 'Plasma Frigate', None),
    'Plasma Frigate - Gift from Team Plasma Password Grunt in left big room middle (from Route 21)': (300376, 356, 'Plasma Frigate (Route 21)', None),

    # PWT
    'PWT - Worker southeast of fountain': (300312, 448, 'PWT', None),

    # Route 1
    'Route 1 - Woman in the central patch of tall grass': (300362, 425, 'Route 1', None),

    # Route 2
    'Route 2 - Lady in the northeast': (300179, 2362, 'Route 2', None),

    # Route 3
    'Route 3 - School Kid after Habitat List in the north': (300180, 471, 'Route 3 - Water', None),

    # Route 4
    'Route 4 - Colress after battle': (300181, 1705, 'Route 4 - North', None),
    'Route 4 - Ace Trainer in first house on right': (300182, 2772, 'Route 4 - North', None),
    'Route 4 - Ace Trainer in first house east of ruins crossroads': (300369, 2772, 'Route 4 - North', None),
    'Route 4 - Black Belt in 2F of first left house': (300288, 386, 'Route 4 - North', None),
    'Route 4 - Black Belt in house in the far southeast of ruins': (300370, 386, 'Route 4 - North', None),
    'Route 4 - Maid in third house on right (Guess Pokémon cry)': (300289, 363, 'Route 4 - North', None),
    'Route 4 - Maid in southwest house (Guess Pokémon cry)': (300371, 363, 'Route 4 - North', None),

    # Route 5
    'Route 5 - Item bought from Breeder': (300186, 2751, 'Route 5', None),

    # Route 6
    'Route 6 - Girl in house southeast of Chargestone Cave': (300190, 383, 'Route 6', None),

    # Route 8
    'Route 8 - Parasol Lady by Tubeline Bridge in east': (300195, 2749, 'Route 8', None),
    'Tubeline Bridge - Scientist at Route 8 gate': (300197, 346, 'Route 8', None),

    # Route 11
    'Route 11 - Ranger inside trailer': (300207, 384, 'Route 11', None),

    # Route 13
    'Route 13 - Ace Trainer on beach near southern house': (300208, 2738, 'Route 13', None),
    'Route 13 - Girl in house in the west accessed from tree path': (300213, 304, 'Route 13', None),

    # Route 16
    'Route 16 - Man in Nimbasa Gate': (300106, 263, 'Route 16', None),
    'Marvelous Bridge - Roughneck at Route 16 gate': (300216, 385, 'Route 16', None),

    # Route 18
    'Route 18 - Northern cliff east of Veteran': (300368, 943, 'Route 18', None),

    # Route 19
    'Route 19 - Alder after Floccesy events': (300008, 2361, 'Route 19', None),

    # Route 20
    'Route 20 - Cheren near dark grass': (300012, 2363, 'Route 20 - North', None),

    # Route 22
    'Route 22 - Colress at Terrakion plateau in the northwest after beating Marlon': (300279, 2364, 'Route 22', None),

    # Shopping Mall
    'Shopping Mall - Lady in bottom section': (300200, 2765, 'Shopping Mall', None),

    # Skyarrow Bridge
    'Skyarrow Bridge - Runner after bridge quest': (300166, 2586, 'Skyarrow Bridge', None),

    # Strange House
    'Strange House 2F - Ghost girl in bedroom after second basement traverse': (300287, 899, 'Strange House', None),

    # Striaton City
    'Striaton City - Fisherman left of Route 3 gate across the water': (300028, 140, 'Striaton City', None),
    'Striaton City - Roughneck in easternmost alley': (300361, 142, 'Striaton City', None),
    'Striaton City - Pansage show in restaurant': (300030, 2777, 'Striaton City', None),
    'Striaton City - Girl in Pokémon Center': (300033, 381, 'Striaton City', None),
    'Striaton City - Man on 1F of lower east apartment': (300034, 104, 'Striaton City', None),
    'Striaton City - School Kid quiz in Trainers\' School': (300035, 355, 'Striaton City', None),

    # Twist Mountain
    'Twist Mountain - Fossil worker': (300159, 2747, 'Twist Mountain', None),

    # Undella Town
    'Undella Town - Man in west of Pokémon Center': (300235, 295, 'Undella Town', None),
    'Undella Town - Zinzolin in front of gate': (300360, 2803, 'Undella Town', None),

    # Victory road

    # Village Bridge
    'Village Bridge - Girl on bridge after checking out the noise in the room below her': (300170, 468, 'Village Bridge', None),
    'Village Bridge - Baker after battle (Post-Game)': (300171, 457, 'Village Bridge', None),
    'Village Bridge - Fisherman in third house from the right after meeting him on Route 8 east': (300318, 299, 'Village Bridge', None),

    # Virbank City
    'Virbank City - Attendant in Route 20 gate': (300019, 2367, 'Virbank City', None),
    'Virbank City - Nursery Aide in the nursery': (300020, 279, 'Virbank City', None),
    'Virbank City - Roughneck in front of Gym': (300021, 492, 'Virbank City', None),

    # Virbank Complex
    'Virbank Complex - Roughneck trading Poké Ball for Great Ball in entrance by waterside': (300023, 2763, 'Virbank Complex', None),

    # Virbank Complex Inside
    'Virbank Complex - Scientist after talking to him three times': (300024, 310, 'Virbank Complex Inside', None),
    'Virbank Complex - Girl at southernmost end after filling Habitat List': (300025, 467, 'Virbank Complex Inside', None),

    # Virbank Gym
    'Virbank Gym - Clyde': (300022, 116, 'Virbank Gym', None),

    # Pokemon Ranger post-battle berry gifts (unused persistent flags 1500..1519 & 2385..2398)
    'Chargestone Cave B1F - Gift from beating Ranger Briana southeast': (300323, 1500, 'Chargestone Cave - Past Bridge', None),
    'Chargestone Cave 1F - Gift from beating Ranger Louis in southwest of the cave, arriving from B1F': (300324, 1501, 'Chargestone Cave - Past Bridge', None),
    'Clay Tunnel - Gift from beating Ranger Katie in Twist Mountain side north': (300325, 1502, 'Clay Tunnel', None),
    'Clay Tunnel - Gift from beating Ranger Maxwell in Twist Mountain side south': (300326, 1503, 'Clay Tunnel', None),
    'Desert Resort - Gift from beating Ranger Anja in east': (300327, 1504, 'Desert Resort', None),
    'Desert Resort - Gift from beating Ranger Jaden near entrance': (300328, 1505, 'Desert Resort', None),
    'Lostlorn Forest - Gift from beating Ranger Forrest in north': (300329, 1506, 'Lostlorn Forest', None),
    'Lostlorn Forest - Gift from beating Ranger Serenity inside leaf pile': (300330, 1507, 'Lostlorn Forest', None),
    'Moor of Icirrus - Gift from beating Ranger Elaine in west behind Strength boulder': (300331, 1508, 'Moor of Icirrus - Strength', None),
    'Moor of Icirrus - Gift from beating Ranger Parker in southeast': (300332, 1509, 'Moor of Icirrus', None),
    'Pinwheel Forest - Inside: Gift from beating Ranger Dwayne south inner forest in leaf pile': (300333, 1510, 'Pinwheel Forest', None),
    'Pinwheel Forest - Inside: Gift from beating Ranger Hillary south inner forest': (300334, 1511, 'Pinwheel Forest', None),
    'Pinwheel Forest - Inside: Gift from beating Ranger Melita northeast inner forest': (300335, 1512, 'Pinwheel Forest', None),
    'Pinwheel Forest - Inside: Gift from beating Ranger Ralph northwest inner forest': (300336, 1513, 'Pinwheel Forest', None),
    'Reversal Mountain - Gift from beating Ranger Eliza 1F in south of the main cavern': (300337, 1514, 'Reversal Mountain', None),
    'Reversal Mountain B1F - Gift from beating Ranger Eliza in the northwest': (300377, 1514, 'Reversal Mountain', None),
    'Reversal Mountain - Gift from beating Ranger Lewis B1F to the left': (300338, 1515, 'Reversal Mountain', None),
    'Reversal Mountain 1F - Gift from beating Ranger Lewis in the southwest': (300378, 1515, 'Reversal Mountain', None),
    'Route 1 - Gift from beating Ranger Audra next to the gate in the western section': (300339, 1516, 'Route 1 - Water', None),
    'Route 1 - Gift from beating Ranger Rick east of the gate in the western section': (300340, 1517, 'Route 1 - Water', None),
    'Route 11 - Gift from beating Ranger Crofton south of trailer': (300341, 1518, 'Route 11', None),
    'Route 11 - Gift from beating Ranger Thalia northeast down waterfall': (300342, 1519, 'Route 11 - Waterfall', None),
    'Route 13 - Gift from beating Ranger Daryl east of northern house': (300343, 2385, 'Route 13', None),
    'Route 13 - Gift from beating Ranger Dianne east of Cobalion in north': (300344, 2386, 'Route 13', None),
    'Route 20 - Gift from beating Pokémon Ranger Bret in west of leaves (Autumn)': (300345, 2387, 'Route 20 - Autumn Islands', None),
    'Route 20 - Gift from beating Pokémon Ranger Leaf north of land in leaves (Autumn)': (300346, 2388, 'Route 20 - Autumn Islands', None),
    'Route 20 - Gift from beating Pokémon Ranger Malory west of land in leaves (Autumn)': (300347, 2389, 'Route 20 - Autumn Islands', None),
    'Route 20 - Gift from beating Pokémon Ranger Naoko above waterfall in south (Autumn)': (300348, 2390, 'Route 20 - Waterfall', None),
    'Route 23 - Gift from beating Ranger Lena north along main path at bottom of stairs': (300349, 2391, 'Route 23', None),
    'Route 23 - Gift from beating Ranger Steve east on cliff in leaf pile': (300350, 2392, 'Route 23', None),
    'Route 5 - Gift from beating Ranger Lois above road': (300351, 2393, 'Route 5', None),
    'Route 6 - Gift from beating Ranger Richard north of Season Research Lab across the water': (300352, 2394, 'Route 6', None),
    'Seaside Cave 1F - Gift from beating Ranger Johan southwest': (300353, 2395, 'Seaside Cave', None),
    'Seaside Cave 1F - Gift from beating Ranger Mikiko west': (300354, 2396, 'Seaside Cave', None),
    'Victory Road - Section 4: Cave, Gift from beating Ranger Eddie accessed from southeast of League gate': (300355, 2397, 'Victory Road - Strength', None),
    'Victory Road - Section 3: Cave, Gift from beating Ranger Eddie accessed from southeast of League gate': (300373, 2397, 'Victory Road - Strength', None),
    'Victory Road - Section 4: Cave, Gift from beating Ranger Elle northwest lower': (300356, 2398, 'Victory Road - Strength', None),
    'Victory Road - Section 3: Cave, Gift from beating Ranger Elle northwest lower': (300374, 2398, 'Victory Road - Strength', None),
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
    'Aspertia City - Bianca after defeating Cheren': (500027, 2368, 'Aspertia City', None),

    # Aspertia Gym
    'Aspertia Gym - Cheren after defeating Gym': (500083, 2377, 'Aspertia Gym', None),

    # Castelia City
    'Castelia City - Castelia Street - Guitarist in building on left 11F': (500044, 209, 'Castelia City', None),
    'Castelia City - North Street - Girl on the left in lower right building 47F': (500045, 416, 'Castelia City', None),
    'Castelia City - Narrow Street - Man behind dumpster': (500070, 2369, 'Castelia City', None),
    'Castelia City - Burgh after defeating Gym': (500076, 2379, 'Castelia City', None),

    # Castelia Sewers
    'Castelia Sewers - Hugh after defeating Team Plasma near Relic Passage': (500004, 2370, 'Castelia Sewers', None),

    # Driftveil City
    'Driftveil City - Clay after defeating Gym': (500078, 2381, 'Driftveil City', None),

    # Floccesy Ranch
    'Floccesy Ranch - Team Plasma Grunt at the end of forest': (500021, 2371, 'Floccesy Ranch', None),

    # Humilau City
    'Humilau Gym - Marlon after defeating Gym': (500055, 2384, 'Humilau Gym', None),

    # Lentimas Town
    'Lentimas Town - Woman in house near girl with Krokorok': (500057, 118, 'Lentimas Town', None),

    # Lostlorn Forest
    'Lostlorn Forest - Backpacker in northern clearing': (500095, 967, 'Lostlorn Forest', None),

    # Marine Tube
    'Marine Tube - Parasol Lady at Humilau City entrance': (500042, 343, 'Marine Tube', None),

    # Mistralton City
    'Mistralton City - Skyla after defeating Gym': (500062, 2382, 'Mistralton City', None),

    # Musical Theater
    'Musical Theatre - Lady to the right of the reception counter': (500049, 211, 'Musical Theater', None),

    # Nimbasa City
    'Nimbasa City - Elesa after defeating Gym': (500072, 2380, 'Nimbasa City', None),

    # Opelucid City
    'Opelucid City - Drayden after defeating Gym': (500082, 2383, 'Opelucid City', None),

    # Reversal Mountain
    'Reversal Mountain - Scientist after Habitat List in northeast of main cavern': (500054, 469, 'Reversal Mountain', None),

    # Route 5
    'Route 5 - Bianca near Nimbasa Gate': (500002, 2373, 'Route 5', None),

    # Route 6
    'Route 6 - Cheren after PWT Plasma Frigate in Season Research Lab': (500003, 2439, 'Route 6', None),

    # Route 23
    'Route 23 - Old man in house at end of stream across the water': (500035, 473, 'Route 23', None),

    # Tubeline Bridge
    'Tubeline Bridge - Battle Girl on middle of bridge': (500043, 345, 'Tubeline Bridge', None),

    # Undella Town
    'Undella Town - Hugh in front of Marine Tube gate': (500006, 414, 'Undella Town', None),

    # Victory road
    'Victory Road - N at badge check gates': (500005, 2374, 'Victory Road', None),
    'Victory Road - Gift from PkMn Trainer Hugh at the very end': (500024, 2375, 'Victory Road - Strength', None),

    # Virbank City
    'Virbank City - Roxie after defeating Team Plasma Grunt at harbour after Gym': (500001, 1704, 'Virbank City', None),

    # Virbank Complex
    'Virbank Complex - Man at entrance after defeating all three Workers': (500094, 465, 'Virbank Complex Inside', None),

    # Virbank Gym
    'Virbank Gym - Roxie after defeating Gym': (500009, 2378, 'Virbank Gym', None),
}
