from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import OoT3DWorld

ITEM_NAME_TO_ID = {
    "Placeholder Item": 1,
    "Ice Trap": 2,
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Placeholder Item": ItemClassification.progression,
    "Ice Trap": ItemClassification.trap,
}

class OoT3DItem(Item):
    game = "Ocarina of Time 3D"

def get_random_filler_item_name(world: OoT3DWorld) -> str:
    if world.random.randint(0, 99) < world.options.trap_chance:
        return "Ice Trap"
    return "Placeholder Item"


def create_item_with_correct_classification(world: OoT3DWorld, name: str) -> OoT3DItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    if name == "PlaceHolder Item" and world.options.placeholder:
        classification = ItemClassification.progression | ItemClassification.useful

    return OoT3DItem(name, classification, ITEM_NAME_TO_ID[name], world.player)

def create_all_items(world: OoT3DWorld) -> None:
    # Base Itempool
    itempool: list[Item] = [
        world.create_item("Placeholder Item"),
        world.create_item("Placeholder Item"),
    ]

    if world.options.placeholder:
        itempool.append(world.create_item("Placeholder Item"))

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool

    if world.options.placeholder:
        starting_confetti_cannon = world.create_item("Placeholder Item")
        world.push_precollected(starting_confetti_cannon)
