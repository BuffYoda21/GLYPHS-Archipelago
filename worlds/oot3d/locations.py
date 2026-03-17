from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import OoT3DWorld

LOCATION_NAME_TO_ID = {
    "Placeholder Location 1": 1,
    "Placeholder Location 2": 2,
    "Placeholder Location 3": 3,
    "Placeholder Location 4": 4,
    "Placeholder Location 5": 5,
    "Placeholder Location 6": 6,
}

class OoT3DLocation(Location):
    game = "Ocarina of Time 3D"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def create_all_locations(world: OoT3DWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: OoT3DWorld) -> None:
    spawn_room = world.get_region("Spawn Room")
    placeholder_area = world.get_region("Placeholder Area")
    placeholder_dungeon = world.get_region("Placeholder Dungeon")

    spawn_room_location = get_location_names_with_ids(
        ["Placeholder Location 1", "Placeholder Location 2"]
    )
    spawn_room.add_locations(spawn_room_location, OoT3DLocation)

    placeholder_area_locations = get_location_names_with_ids(["Placeholder Location 3", "Placeholder Location 4"])
    placeholder_area.add_locations(placeholder_area_locations, OoT3DLocation)

    placeholder_dungeon_locations = get_location_names_with_ids(["Placeholder Location 5", "Placeholder Location 6"])
    placeholder_dungeon.add_locations(placeholder_dungeon_locations, OoT3DLocation)


def create_events(world: OoT3DWorld) -> None:
    placeholder_area = world.get_region("Placeholder Area")
    finale = world.get_region("Finale")

    placeholder_area.add_event("Dungeon Open", "Dungeon Open", location_type=OoT3DLocation, item_type=items.OoT3DItem)
    finale.add_event("Boss Defeated", "Victory", location_type=OoT3DLocation, item_type=items.OoT3DItem)
