from enum import IntEnum
from typing import NamedTuple, Optional
from BaseClasses import Location, Item, ItemClassification

class GlyphsLocation(Location):
    game = "GLYPHS"

class GlyphsItem(Item):
    game = "GLYPHS"

class ItemData(NamedTuple):
    ap_code: Optional[int]
    classification: ItemClassification
    count: Optional[int] = 1

class LocData(NamedTuple):
    ap_code: Optional[int]
    region: Optional[str]
