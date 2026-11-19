from __future__ import annotations

from typing import NamedTuple
from BaseClasses import ItemClassification


class ItemInfo(NamedTuple):
    ap_id: int
    internal_id: int
    pocket: str
    classification: ItemClassification


PROGRESSION_ITEM_TABLE: dict[str, ItemInfo] = {

    # Gym badges
    "Basic Badge":  ItemInfo(400001, 0, "badge", ItemClassification.progression),
    "Toxic Badge":  ItemInfo(400002, 1, "badge", ItemClassification.progression),
    "Insect Badge": ItemInfo(400003, 2, "badge", ItemClassification.progression),
    "Bolt Badge":   ItemInfo(400004, 3, "badge", ItemClassification.progression),
    "Quake Badge":  ItemInfo(400005, 4, "badge", ItemClassification.progression),
    "Jet Badge":    ItemInfo(400006, 5, "badge", ItemClassification.progression),
    "Legend Badge": ItemInfo(400007, 6, "badge", ItemClassification.progression),
    "Wave Badge":   ItemInfo(400008, 7, "badge", ItemClassification.progression),

    # HMs
    "HM01 Cut":       ItemInfo(100420, 0x01A4, "tm_hm", ItemClassification.progression),
    "HM02 Fly":       ItemInfo(100421, 0x01A5, "tm_hm", ItemClassification.progression),
    "HM03 Surf":      ItemInfo(100422, 0x01A6, "tm_hm", ItemClassification.progression),
    "HM04 Strength":  ItemInfo(100423, 0x01A7, "tm_hm", ItemClassification.progression),
    "HM05 Waterfall": ItemInfo(100424, 0x01A8, "tm_hm", ItemClassification.progression),
    "HM06 Dive":      ItemInfo(100425, 0x01A9, "tm_hm", ItemClassification.progression),

    # Progressive level cap & seasonal items
    "Level Cap Upgrade": ItemInfo(400100, 0, "special", ItemClassification.progression),
    "Spring":            ItemInfo(400101, 0, "special", ItemClassification.progression),
    "Summer":            ItemInfo(400102, 1, "special", ItemClassification.progression),
    "Autumn":            ItemInfo(400103, 2, "special", ItemClassification.progression),
    "Winter":            ItemInfo(400104, 3, "special", ItemClassification.progression),

    # Days of the week items
    "Sunday":            ItemInfo(400120, 0, "special", ItemClassification.progression),
    "Monday":            ItemInfo(400121, 1, "special", ItemClassification.progression),
    "Tuesday":           ItemInfo(400122, 2, "special", ItemClassification.progression),
    "Wednesday":         ItemInfo(400123, 3, "special", ItemClassification.progression),
    "Thursday":          ItemInfo(400124, 4, "special", ItemClassification.progression),
    "Friday":            ItemInfo(400125, 5, "special", ItemClassification.progression),
    "Saturday":          ItemInfo(400126, 6, "special", ItemClassification.progression),

    # Progression and travel items
    "Town Map":         ItemInfo(100442, 0x01BA, "key_items", ItemClassification.useful),
    "Super Rod":        ItemInfo(100447, 0x01BF, "key_items", ItemClassification.progression),
    "Bicycle":          ItemInfo(100450, 0x01C2, "key_items", ItemClassification.useful),
    "Lunar Wing":       ItemInfo(100453, 0x01C5, "key_items", ItemClassification.progression),
    "Member Card":      ItemInfo(100454, 0x01C6, "key_items", ItemClassification.filler),
    "S.S. Ticket":      ItemInfo(100456, 0x01C8, "key_items", ItemClassification.filler),
    "Magma Stone":      ItemInfo(100458, 0x01CA, "key_items", ItemClassification.progression),
    "Secret Key":       ItemInfo(100467, 0x01D3, "key_items", ItemClassification.filler),
    "Dowsing Machine":  ItemInfo(100471, 0x01D7, "key_items", ItemClassification.progression),
    "Pass":             ItemInfo(100480, 0x01E0, "key_items", ItemClassification.filler),
    "Liberty Pass":     ItemInfo(100574, 0x023E, "key_items", ItemClassification.filler),
    "Dragon Skull":     ItemInfo(100579, 0x0243, "key_items", ItemClassification.filler),
    "Light Stone":      ItemInfo(100616, 0x0268, "key_items", ItemClassification.progression),
    "Dark Stone":       ItemInfo(100617, 0x0269, "key_items", ItemClassification.progression),
    "Medal Box":        ItemInfo(100627, 0x0273, "key_items", ItemClassification.useful),
    "DNA Splicers":     ItemInfo(100628, 0x0274, "key_items", ItemClassification.progression),
    "Plasma Card":      ItemInfo(100633, 0x0279, "key_items", ItemClassification.progression),
    "Card Key":         ItemInfo(100475, 0x01DB, "key_items", ItemClassification.progression),
    "Grubby Hanky":     ItemInfo(100634, 0x027A, "key_items", ItemClassification.progression),
    "Colress MCHN":     ItemInfo(100635, 0x027B, "key_items", ItemClassification.progression),
    "Permit":           ItemInfo(100630, 0x0276, "key_items", ItemClassification.progression),
}
