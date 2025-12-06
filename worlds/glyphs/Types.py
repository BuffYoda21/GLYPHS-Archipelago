from enum import IntEnum
from typing import NamedTuple, Optional
from BaseClasses import Location, Item, ItemClassification

class GlyphsLocation(Location):
    game = "GLYPHS"

class GlyphsItem(Item):
    game = "GLYPHS"

class ItemData:
    def __init__(self, ap_code: Optional[int], classification: ItemClassification, advancement: bool = False, count: Optional[int] = 1):
        self.ap_code = ap_code
        self.classification = classification
        self.advancement = advancement
        self.count = count

    def __repr__(self) -> str:  # Helpful for debugging/tests
        return f"ItemData(ap_code={self.ap_code!r}, classification={self.classification!r}, advancement={self.advancement!r}, count={self.count!r})"

class LocData(NamedTuple):
    ap_code: Optional[int]
    region: Optional[str]
