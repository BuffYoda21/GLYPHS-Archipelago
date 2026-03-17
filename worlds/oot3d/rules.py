from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from .world import OoT3DWorld


def set_all_rules(world: OoT3DWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

def set_all_entrance_rules(world: OoT3DWorld) -> None:
    spawn_to_placeholder_area = world.get_entrance("Spawn to Placeholder Area")
    placeholder_area_to_placeholder_dungeon = world.get_entrance("Placeholder Area to Placeholder Dungeon")
    placeholder_dungeon_to_finale = world.get_entrance("Placeholder Dungeon to Finale")

    set_rule(spawn_to_placeholder_area, lambda state: state.has("Placeholder Item", world.player))
    set_rule(placeholder_area_to_placeholder_dungeon, lambda state: state.has("Dungeon Open", world.player))
    set_rule(placeholder_dungeon_to_finale, lambda state: state.has("Placeholder Item", world.player, 2))

    if world.options.placeholder:
        spawn_to_finale = world.get_entrance("Finale Skip")
        set_rule(spawn_to_finale, lambda state: state.has("Placeholder Item", world.player))

def set_all_location_rules(world: OoT3DWorld) -> None:
    pass

def set_completion_condition(world: OoT3DWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
