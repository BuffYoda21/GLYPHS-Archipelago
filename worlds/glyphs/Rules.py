from collections.abc import Callable
from BaseClasses import Entrance, MultiWorld, CollectionState
from worlds.generic.Rules import add_rule, set_rule
from typing import TYPE_CHECKING

from worlds.glyphs.Macros import *

if TYPE_CHECKING:
    from . import GlyphsWorld

# This is the last big thing to do (at least for me)
# This is where you add item
# These are omega simplified rules
# There are a ton of different ways you can add rules from amoount of items you need to optional items
# Theres also difficulty options and a bunch others
# Id suggest going through a bunch of different ap worlds and seeing how they do the rules
# Even better if its a game you know a lot about and can tell what you need to get to certain locations
def set_rules(world: "GlyphsWorld"):
    player = world.player
    options = world.options

    # Region Access
    # -------------------------------from---------------to----------------------conditions--------------------------------
    connect_regions(world, player, "Menu",          "Region 1")
    connect_regions(world, player, "Region 1",      "Region 2",     lambda state: can_dash(state, player))
    connect_regions(world, player, "Region 2",      "Region 1")
    connect_regions(world, player, "Region 2",      "Region 3",     lambda state: can_dash(state, player)                   and can_press_green_buttons(state, player) and defeated_gilded_serpent(state, player) and has_grapple(state, player))
    # Region 3 -> Region 2 is not possible
    connect_regions(world, player, "Region 2",      "Region 4",     lambda state: can_dash(state, player)                   and wizard_true_defeat(state, player))
    connect_regions(world, player, "Region 4",      "Region 2",     lambda state: wizard_true_defeat(state, player))
    connect_regions(world, player, "Region 3",      "Region 4",     lambda state: can_dash(state, player)                   and can_press_green_buttons(state, player) and defeated_gilded_serpent(state, player) and has_grapple(state, player))
    # Region 4 -> Region 3 is not possible
    connect_regions(world, player, "Region 3",      "Collapse",     lambda state: collapse_available(state, player) )
    connect_regions(world, player, "Region 2",      "Smile Shop",   lambda state: can_dash(state, player)                   and can_press_green_buttons(state, player))
    connect_regions(world, player, "Smile Shop",    "Region 1")
    connect_regions(world, player, "Region 2",      "Dark Region",  lambda state: can_dash(state, player)                   and can_press_green_buttons(state, player) and defeated_gilded_serpent(state, player) and has_grapple(state, player))
    connect_regions(world, player, "Dark Region",   "Region 3")
    connect_regions(world, player, "Region 2",      "The Between",  lambda state: can_dash(state, player))
    connect_regions(world, player, "The Between",   "Region 2")
    connect_regions(world, player, "The Between",   "Smile Shop",   lambda state: can_dash(state, player)                   and options.LocicalWallJumps.value)
    connect_regions(world, player, "Menu",          "Act 1",        lambda state: act_1_available(state, player))
    connect_regions(world, player, "Menu",          "Act 2",        lambda state: act_2_available(state, player))
    connect_regions(world, player, "Menu",          "Act 3",        lambda state: act_3_available(state, player))
    connect_regions(world, player, "Act 1",         "Act 2",        lambda state: void_gate_open(state, player)             and can_dash_attack(state, player))
    connect_regions(world, player, "Act 2",         "Act 3",        lambda state: can_fight(state, player)                  and can_dash_attack(state, player))
    connect_regions(world, player, "Act 1",         "Epilogue",     lambda state = CollectionState: can_dash(state, player) and state.has("Shroud", player))     

    
    # Event Locations
    ez_set_rule("Defeat Runic Construct",   lambda state: state.can_reach_entrance("Menu -> Region 1", player) and can_fight_parryable_enemy(state, player))
    ez_set_rule("Stalker Sigil 1",          lambda state: state.can_reach_entrance("Menu -> Region 1", player) and can_fight_parryable_enemy(state, player))
    ez_set_rule("Serpent Lock 1",           lambda state: state.can_reach_entrance("Region 1 -> Region 2", player) and can_fight_parryable_enemy(state, player))
    
    # Victory condition rule!
    world.multiworld.completion_condition[player] = lambda state: state.has("Victory", player)

def connect_regions(world: MultiWorld, player: int, source: str, target: str, rule=None) -> Entrance:
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)
    return sourceRegion.connect(targetRegion, rule=rule)

def ez_set_rule(location_name: str, rule: Callable[[CollectionState], bool]) -> None:
    set_rule(GlyphsWorld.get_location(location_name), rule)