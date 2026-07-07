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

class ButtonColor(IntEnum):
        RED = 0
        BLUE = 1
        GREEN = 2
        YELLOW = 3
        PINK = 4
        BLACK = 5

class ButtonData:
    def __init__(self, id: int, color: ButtonColor, validColors: Optional[list[ButtonColor]] = None):
        self.id = id
        self.color = color
        if validColors is None:
            validColors = [color]
        else:
            self.validColors = validColors

    
    def __repr__(self) -> str:
        return f"ButtonData(id={self.id!r}, color={self.color!r})"

class LocData(NamedTuple):
    ap_code: Optional[int]
    region: Optional[str]
