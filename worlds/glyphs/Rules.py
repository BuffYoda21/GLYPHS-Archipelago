from collections.abc import Callable
from BaseClasses import Entrance, MultiWorld, CollectionState
from worlds.generic.Rules import set_rule
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
    state = CollectionState(world)

    # Region Access
    # -------------------------------------from--------------------------to--------------------------------conditions--------------------------------
    connect_regions(world, player, "Menu",                      "Region 1 - Upper Left")
    connect_regions(world, player, "Region 1 - Upper Left",     "Region 1 - Upper Right",   lambda: can_dash(state, player))
    connect_regions(world, player, "Region 1 - Upper Right",    "Region 1 - Upper Left",    lambda: can_dash(state, player))
    connect_regions(world, player, "Region 1 - Upper Left",     "Region 1 - Central")
    connect_regions(world, player, "Region 1 - Upper Right",    "Region 1 - Central")
    connect_regions(world, player, "Region 1 - Central",        "Region 1 - Upper Right",   lambda: can_dash(state, player)                   and defeated_runic_construct(state, player))
    connect_regions(world, player, "Region 1 - Central",        "Region 1 - Left",          lambda: can_dash(state, player)                   and defeated_runic_construct(state, player))
    connect_regions(world, player, "Region 1 - Left",           "Region 1 - Central",       lambda: can_dash(state, player))
    connect_regions(world, player, "Region 1 - Upper Right",    "Region 2 - Left",          lambda: can_dash(state, player))
    connect_regions(world, player, "Region 1 - Left",           "Region 2 - Upper Right",   lambda: can_dash(state, player))
    connect_regions(world, player, "Region 2 - Left",           "Region 2 - Central",       lambda: can_dash(state, player))
    connect_regions(world, player, "Region 2 - Central",        "Region 2 - Left",          lambda: can_dash(state, player))
    connect_regions(world, player, "Region 2 - Central",        "Region 2 - Sector 1",      lambda: can_dash(state, player))
    connect_regions(world, player, "Region 2 - Sector 1",       "Region 2 - Central")
    connect_regions(world, player, "Region 2 - Central",        "Region 2 - Sector 2",      lambda: can_dash(state, player)                   and can_press_green_buttons(state, player))
    connect_regions(world, player, "Region 2 - Sector 1",       "Region 2 - Sector 2",      lambda: can_dash(state, player)                   and can_press_green_buttons(state, player))
    connect_regions(world, player, "Region 2 - Central",        "Region 2 - Sector 4")
    connect_regions(world, player, "Region 2 - Sector 4",       "Region 2 - Sector 4 End",  lambda: can_dash(state, player))
    connect_regions(world, player, "Region 1 - Central",        "Region 2 - Sector 4 End",  lambda: can_solve_flower_puzzle(state, player))
    connect_regions(world, player, "Region 2 - Central",        "Region 2 - Serpent Upper", lambda: can_dash(state, player)                   and can_press_green_buttons(state, player))
    connect_regions(world, player, "Region 2 - Sector 2",       "Region 2 - Serpent Upper", lambda: can_dash(state, player)                   and can_press_green_buttons(state, player))
    connect_regions(world, player, "Region 2 - Serpent Upper",  "Region 2 - Serpent Lower", lambda: can_dash(state, player)                   and can_press_green_buttons(state, player))
    connect_regions(world, player, "Region 2 - Serpent Lower",  "Region 2 - Lower",         lambda: defeated_gilded_serpent(state, player)    and has_grapple(state, player))
    connect_regions(world, player, "Region 2 - Lower",          "Region 3")
    connect_regions(world, player, "Region 2 - Central",        "Region 4 - Entrance",      lambda: wizard_true_defeat(state, player))
    connect_regions(world, player, "Region 2 - Sector 4",       "Region 4 - Entrance",      lambda: wizard_true_defeat(state, player))
    connect_regions(world, player, "Region 4 - Entrance",       "Region 2 - Sector 4",      lambda: wizard_true_defeat(state, player))
    connect_regions(world, player, "Region 4 - Entrance",       "Region 4 - Upper",         lambda: can_dash_attack(state, player)            and defeated_spearman(state, player))
    connect_regions(world, player, "Region 4 - Upper",          "Region 4 - Central",       lambda: can_dash_attack(state, player)            and can_parry(state, player))
    connect_regions(world, player, "Region 4 - Central",        "Region 4 - Lower",         lambda: can_dash(state, player)                   and can_parry(state, player)                  and can_press_green_buttons(state, player))
    connect_regions(world, player, "Region 3",                  "Region 4 - Lower",         lambda: can_solve_flower_puzzle(state, player))
    connect_regions(world, player, "Region 3",                  "Collapse",                 lambda: collapse_available(state, player) )
    connect_regions(world, player, "Region 2 - Sector 2",       "Smile Shop",               lambda: can_dash(state, player)                   and can_press_green_buttons(state, player))
    connect_regions(world, player, "Smile Shop",                "Region 1 - Central")
    connect_regions(world, player, "Region 2 - Lower",          "Dark Region",              lambda: can_dash(state, player))
    connect_regions(world, player, "Dark Region",               "Region 3")
    connect_regions(world, player, "Dark Region",               "Smile Shop",               lambda: can_dash_attack(state, player))
    connect_regions(world, player, "Region 2 - Left",           "The Between",              lambda: can_dash(state, player))
    connect_regions(world, player, "The Between",               "Region 2 - Left")
    connect_regions(world, player, "The Between",               "Smile Shop",               lambda: can_dash(state, player)                   and options.LocicalWallJumps.value)
    connect_regions(world, player, "Menu",                      "Act 1",                    lambda: act_1_available(state, player))
    connect_regions(world, player, "Menu",                      "Act 2",                    lambda: act_2_available(state, player))
    connect_regions(world, player, "Menu",                      "Act 3",                    lambda: act_3_available(state, player))
    connect_regions(world, player, "Act 1",                     "Act 2",                    lambda: void_gate_open(state, player)             and can_dash_attack(state, player))
    connect_regions(world, player, "Act 2",                     "Act 3",                    lambda: can_fight(state, player)                  and can_dash_attack(state, player))
    connect_regions(world, player, "Act 1",                     "Epilogue",                 lambda: can_dash(state, player)                   and state.has("Shroud", player))     


    # Event Locations
    set_rule_from_string("Defeat Runic Construct",  lambda: can_fight_parryable_enemy(state, player))
    set_rule_from_string("Stalker Sigil 1",         lambda: stalker_sigils_present(state, player))
    set_rule_from_string("Serpent Lock 1",          lambda: can_dash(state, player))
    set_rule_from_string("Serpent Lock 2",          lambda: can_dash(state, player) and can_press_green_buttons(state, player))
    set_rule_from_string("Serpent Lock 3")
    set_rule_from_string("Defeat Gilded Serpent",   lambda: can_dash(state, player) and serpent_door_open(state, player) and can_fight(state, player))
    set_rule_from_string("Stalker Sigil 2",         lambda: stalker_sigils_present(state, player) and can_dash(state, player) and can_press_green_buttons(state, player))
    set_rule_from_string("Stalker Sigil 3",         lambda: stalker_sigils_present(state, player))
    set_rule_from_string("Solve Flower Puzzle",     lambda: can_dash(state, player) and can_press_green_buttons(state, player) and has_grapple(state, player) and defeated_gilded_serpent(state, player))
    set_rule_from_string("Collapse Unlock",         lambda: can_dash(state, player) and wizard_fight_available(state, player) and can_fight_parryable_enemy(state, player))
    set_rule_from_string("Defeat Spearman",         lambda: can_dash_attack(state, player) and can_press_green_buttons(state, player) and has_grapple(state, player) and defeated_gilded_serpent(state, player))
    set_rule_from_string("Good Ending",             lambda: can_fight(state, player) and can_dash_attack(state, player) and can_parry(state, player) and has_grapple(state, player) and wraith_fight_available(state, player) and state.has("Gold Shard", player, 3))
    set_rule_from_string("Last Fracture",           lambda: has_clarity(state, player) and wraith_fight_available(state, player) and state.has("Defeat Wraith", player))
    set_rule_from_string("False Ending",            lambda: can_dash(state, player) and has_grapple(state, player))
    set_rule_from_string("Smilemask Ending",        lambda: state.has("Smile Token", player, 10))
    set_rule_from_string("Defeat Null",             lambda: can_dash_attack(state, player) and has_grapple(state, player) and has_sword(state, player))
    set_rule_from_string("Clarity",                 lambda: defeated_null(state, player) and state.has("Rune Cube", player, 3))
    set_rule_from_string("Omnipotence Ending",      lambda: can_dash_attack(state, player) and has_grapple(state, player) and void_gate_open(state, player) and state.has("Shroud", player))
    set_rule_from_string("Clear Act 1",             lambda: act_1_available(state, player) and void_gate_open(state, player) and can_dash_attack(state, player) and has_grapple(state, player) and state.has("Shroud", player))
    set_rule_from_string("Clear Act 2",             lambda: act_2_available(state, player) and can_dash_attack(state, player) and can_fight(state, player) and can_parry(state, player) and (state.has("Shroud", player) or state.has("Progressive Chicken Hat", player, 1)))
    set_rule_from_string("True Ending",             lambda: can_fight(state, player) and can_parry(state, player) and (state.has("Shroud", player) or state.has("Progressive Chicken Hat", player, 1)) and state.has("Gold Shard", player, 3))
    set_rule_from_string("Clear Epilogue",          lambda: can_dash(state, player) and has_grapple(state, player) and state.has("Shroud", player) and state.has("Progressive Chicken Hat", player, 1))


    # Region 1
    set_rule_from_string("Sword Pedestal")
    set_rule_from_string("Runic Construct Reward",      lambda: defeated_runic_construct(state, player))
    set_rule_from_string("Map Pedestal",                lambda: can_dash(state, player))
    set_rule_from_string("Silver Shard Puzzle 1",       lambda: can_dash(state, player))
    set_rule_from_string("Silver Shard Puzzle 2",       lambda: can_dash(state, player) and has_grapple(state, player))
    set_rule_from_string("Silver Shard Puzzle 3",       lambda: can_dash(state, player))
    set_rule_from_string("Smile Token Puzzle 3",        lambda: can_dash(state, player) and has_grapple(state, player))
    set_rule_from_string("Smile Token Puzzle 9",        lambda: can_dash(state, player))
    set_rule_from_string("Color Cypher Room Pickup",    lambda: can_dash(state, player))
    set_rule_from_string("Master Puzzle 2",             lambda: can_dash(state, player) and has_grapple(state, player))


    # Region 2
    set_rule_from_string("Silver Shard Puzzle 4",       lambda: can_dash(state, player))
    set_rule_from_string("Silver Shard Puzzle 5",       lambda: can_dash(state, player) and can_press_green_buttons(state, player))
    set_rule_from_string("Silver Shard Puzzle 6",       lambda: can_dash(state, player) and can_press_green_buttons(state, player))
    set_rule_from_string("Silver Shard Puzzle 7",       lambda: can_dash(state, player) and can_press_green_buttons(state, player))
    set_rule_from_string("Silver Shard Puzzle 8",       lambda: can_dash(state, player))
    set_rule_from_string("Silver Shard Puzzle 9",       lambda: can_dash(state, player) and (options.DashPuzzlesSolved.value or state.can_reach_location("Color Cypher Room Pickup", player)))
    set_rule_from_string("Silver Shard Puzzle 15",      lambda: can_dash(state, player) and can_press_green_buttons(state, player) and (defeated_gilded_serpent(state, player) or can_fight(state, player)))
    set_rule_from_string("Smile Token Puzzle 1",        lambda: can_dash(state, player))
    set_rule_from_string("Smile Token Puzzle 6",        lambda: can_dash(state, player) and defeated_gilded_serpent(state, player))
    set_rule_from_string("Smile Token Puzzle 8",        lambda: can_dash(state, player))
    set_rule_from_string("Smile Token Puzzle 10",       lambda: can_dash_attack(state, player) and can_parry(state, player) and has_grapple(state, player))
    set_rule_from_string("Gilded Serpent Reward",       lambda: defeated_gilded_serpent(state, player))
    set_rule_from_string("Cameo Room Pickup",           lambda: can_dash(state, player))
    set_rule_from_string("Car Hall Pickup",             lambda: can_dash(state, player))
    set_rule_from_string("Near Shooters Pickup",        lambda: can_dash(state, player))
    set_rule_from_string("Collapsed Tunnel Pickup")
    set_rule_from_string("Nest Room Pickup",            lambda: can_dash(state, player))
    set_rule_from_string("Serpent Boss Room Pickup",    lambda: can_dash(state, player) and (options.LogicalWallJumps.value or (state.can_reach_region("Region 2 - Serpent Upper") and can_press_green_buttons(state, player) and defeated_gilded_serpent(state, player))))
    set_rule_from_string("Shadow Chase Reward",         lambda: can_dash(state, player) and has_grapple(state, player) and can_press_green_buttons(state, player))
    set_rule_from_string("Water Room Pickup",           lambda: can_solve_flower_puzzle(state, player))
    set_rule_from_string("George Reward",               lambda: can_dash(state, player) and state.has("Seeds", player, 10))
    set_rule_from_string("Shadow Chase Pickup",         lambda: can_dash(state, player) and has_grapple(state, player) and can_press_green_buttons(state, player))
    set_rule_from_string("Master Puzzle 1",             lambda: can_dash(state, player) and state.has("Silver Shard", player, 15) and (options.DashPuzzlesSolved.value or can_access_all_silver_shards(state, player)))


    # Region 3
    set_rule_from_string("Green Stone Trial",           lambda: can_dash(state, player) and has_grapple(state, player) and can_press_green_buttons(state, player))
    set_rule_from_string("Blue Stone Trial",            lambda: can_dash(state, player) and has_grapple(state, player) and can_press_green_buttons(state, player))
    set_rule_from_string("Red Stone Trial",             lambda: can_dash(state, player) and has_grapple(state, player) and can_fight(state, player))
    set_rule_from_string("Silver Shard Puzzle 10",      lambda: can_dash(state, player) and has_grapple(state, player) and can_press_green_buttons(state, player))
    set_rule_from_string("Silver Shard Puzzle 11",      lambda: can_dash(state, player) and has_grapple(state, player) and can_press_green_buttons(state, player))
    set_rule_from_string("Silver Shard Puzzle 12",      lambda: can_dash(state, player))
    set_rule_from_string("Silver Shard Puzzle 13",      lambda: can_dash(state, player) and has_grapple(state, player))
    set_rule_from_string("Silver Shard Puzzle 14",      lambda: can_dash(state, player) and has_grapple(state, player) and can_press_green_buttons(state, player))
    set_rule_from_string("Smile Token Puzzle 2",        lambda: can_dash(state, player) and has_grapple(state, player))
    set_rule_from_string("Smile Token Puzzle 7",        lambda: can_dash(state, player) and has_grapple(state, player) and can_press_green_buttons(state, player))
    set_rule_from_string("Master Puzzle 3",             lambda: can_dash_attack(state, player) and has_grapple(state, player) and has_sword(state, player))
    

    # Region 4
    set_rule_from_string("Spearman Reward",                     lambda: can_dash_attack(state, player) and has_grapple(state, player) and can_fight(state, player))
    set_rule_from_string("Multiparry Gold Shard Puzzle",        lambda: can_dash(state, player) and has_grapple(state, player) and can_parry(state, player))
    set_rule_from_string("Platforming Gold Shard Room",         lambda: can_dash(state, player) and has_grapple(state, player) and can_parry(state, player) and has_sword(state, player))
    set_rule_from_string("Flower Puzzle Reward",                lambda: can_solve_flower_puzzle(state, player))
    set_rule_from_string("Smile Token Puzzle 4",                lambda: can_dash(state, player) and has_grapple(state, player) and can_parry(state, player))
    set_rule_from_string("Smile Token Puzzle 5",                lambda: can_dash(state, player))
    set_rule_from_string("On top of the Rosetta Stone Pickup",  lambda: can_dash(state, player))
    set_rule_from_string("Long Parry Platforming Room Pickup",  lambda: can_dash(state, player) and has_grapple(state, player) and can_parry(state, player) and can_press_green_buttons(state, player))



    # Victory condition rule!
    victory: lambda: False
    if options.Goal.value == options.Goal.option_false_ending:
        victory = lambda: state.has("False Ending")
    elif options.Goal.value == options.Goal.option_good_ending:
        victory = lambda: state.has("Good Ending")
    elif options.Goal.value == options.Goal.option_true_ending:
        victory = lambda: state.has("True Ending")
    elif options.Goal.value == options.Goal.option_all_star_endings:
        victory = lambda: state.has("Perfect Clarity") and state.has("Smilemask Ending") and state.has("Omnipotence Ending")
    elif options.Goal.value == options.Goal.option_epilouge:
        victory = lambda: state.has("Epilouge Ending")
    elif options.Goal.value == options.Goal.option_all_endings:
        victory = lambda: state.has("False Ending") and state.has("Good Ending") and state.has("True Ending") and state.has("Perfect Clarity") and state.has("Smilemask Ending") and state.has("Omnipotence Ending") and state.has("Epilouge Ending")
    world.multiworld.completion_condition[player] = victory

def connect_regions(world: MultiWorld, player: int, source: str, target: str, rule=None) -> Entrance:
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)
    return sourceRegion.connect(targetRegion, rule=rule)

def set_rule_from_string(location_name: str, rule=None) -> None:
    set_rule(GlyphsWorld.get_location(location_name), rule=rule)