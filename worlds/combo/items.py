from typing import TYPE_CHECKING, List

from BaseClasses import Item

from .glyphs.Items import item_table as glyphs_item_table
from .apquest.items import ITEM_NAME_TO_ID as APQUEST_ITEM_NAME_TO_ID

if TYPE_CHECKING:
    from . import ComboWorld

def build_item_name_to_id() -> dict[str, int]:
    item_name_to_id = {}
    item_name_to_id.update({name: data.ap_code for name, data in glyphs_item_table.items() if data.ap_code is not None})
    item_name_to_id.update(APQUEST_ITEM_NAME_TO_ID)
    return item_name_to_id

def create_item(world: "ComboWorld", name: str) -> Item:
    if name in glyphs_item_table:
        return world.glyphs.create_item(name)
    return world.apquest.create_item(name)

def create_items(world: "ComboWorld") -> None:
    itempool: List[Item] = world.glyphs.create_itempool()
    itempool += world.apquest.create_all_items()

    remaining = len(world.multiworld.get_unfilled_locations(world.player)) - len(itempool)
    for _ in range(remaining):
        itempool.append(world.create_filler())

    world.multiworld.itempool += itempool