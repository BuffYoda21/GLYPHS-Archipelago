from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import OoT3DWorld

def create_and_connect_regions(world: OoT3DWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: OoT3DWorld) -> None:
    menu = Region("Menu", world.player, world.multiworld)
    spawn_room = Region("Spawn Room", world.player, world.multiworld)
    placeholder_area = Region("Placeholder Area", world.player, world.multiworld)
    placeholder_dungeon = Region("Placeholder Dungeon", world.player, world.multiworld)
    finale = Region("Finale", world.player, world.multiworld)

    regions = [menu, spawn_room, placeholder_area, placeholder_dungeon, finale]

    world.multiworld.regions += regions

def connect_regions(world: OoT3DWorld) -> None:
    menu = world.get_region("Menu")
    spawn_room = world.get_region("Spawn Room")
    placeholder_area = world.get_region("Placeholder Area")
    placeholder_dungeon = world.get_region("Placeholder Dungeon")
    finale = world.get_region("Finale")

    menu.connect(spawn_room, "Menu to Spawn")
    spawn_room.connect(placeholder_area, "Spawn to Placeholder Area")
    placeholder_area.connect(placeholder_dungeon, "Placeholder Area to Placeholder Dungeon")
    placeholder_dungeon.connect(finale, "Placeholder Dungeon to Finale")

    if world.options.placeholder:
        spawn_room.connect(finale, "Finale Skip")
