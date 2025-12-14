from collections.abc import Callable
from BaseClasses import Entrance, CollectionState
from worlds.generic.Rules import set_rule
from typing import TYPE_CHECKING
from worlds.glyphs.Macros import *

if TYPE_CHECKING:
    from . import GlyphsWorld

def connect_entrances(world: "GlyphsWorld"):
    player = world.player
    state = CollectionState(world.multiworld)

    # Region Access
    # -------------------------------------from--------------------------to--------------------------------conditions--------------------------------
    connect_areas(world, "Menu",                      "Region 1 - Upper Left")
    connect_areas(world, "Region 1 - Upper Left",     "Region 1 - Upper Right",   lambda state: can_dash(state, player))
    connect_areas(world, "Region 1 - Upper Right",    "Region 1 - Upper Left",    lambda state: can_dash(state, player))
    connect_areas(world, "Region 1 - Upper Left",     "Region 1 - Central",       lambda state: True)
    connect_areas(world, "Region 1 - Upper Right",    "Region 1 - Central",       lambda state: True)
    connect_areas(world, "Region 1 - Central",        "Region 1 - Upper Right",   lambda state: can_dash(state, player)                   and defeated_runic_construct(state, player))
    connect_areas(world, "Region 1 - Central",        "Region 1 - Left",          lambda state: can_dash(state, player)                   and defeated_runic_construct(state, player))
    connect_areas(world, "Region 1 - Left",           "Region 1 - Central",       lambda state: can_dash(state, player))
    connect_areas(world, "Region 1 - Upper Right",    "Region 2 - Left",          lambda state: can_dash(state, player))
    connect_areas(world, "Region 2 - Left",           "Region 2 - Central",       lambda state: can_dash(state, player))
    connect_areas(world, "Region 2 - Central",        "Region 2 - Left",          lambda state: can_dash(state, player))
    connect_areas(world, "Region 2 - Central",        "Region 2 - Sector 1",      lambda state: can_dash(state, player))
    connect_areas(world, "Region 2 - Sector 1",       "Region 2 - Central",       lambda state: True)
    connect_areas(world, "Region 2 - Central",        "Region 2 - Sector 2",      lambda state: can_dash(state, player)                   and can_press_green_buttons(state, player))
    connect_areas(world, "Region 2 - Sector 1",       "Region 2 - Sector 2",      lambda state: can_dash(state, player)                   and can_press_green_buttons(state, player))
    connect_areas(world, "Region 2 - Central",        "Region 2 - Sector 4",      lambda state: True)
    connect_areas(world, "Region 2 - Sector 4",       "Region 2 - Sector 4 End",  lambda state: can_dash(state, player))
    connect_areas(world, "Region 1 - Central",        "Region 2 - Sector 4 End",  lambda state: can_solve_flower_puzzle(state, player))
    connect_areas(world, "Region 2 - Central",        "Region 2 - Serpent Upper", lambda state: can_dash(state, player)                   and can_press_green_buttons(state, player))
    connect_areas(world, "Region 2 - Sector 2",       "Region 2 - Serpent Upper", lambda state: can_dash(state, player)                   and can_press_green_buttons(state, player))
    connect_areas(world, "Region 2 - Serpent Upper",  "Region 2 - Serpent Lower", lambda state: can_dash(state, player)                   and can_press_green_buttons(state, player))
    connect_areas(world, "Region 2 - Serpent Lower",  "Region 2 - Lower",         lambda state: defeated_gilded_serpent(state, player)    and has_grapple(state, player))
    connect_areas(world, "Region 2 - Sector 4",       "Region 2 - Shadow Chase",  lambda state: can_dash(state, player)                   and can_press_green_buttons(state, player)    and shadow_chase_open(state, player))
    connect_areas(world, "Region 2 - Lower",          "Region 3",                 lambda state: True)
    connect_areas(world, "Region 2 - Central",        "Region 4 - Entrance",      lambda state: wizard_true_defeat(state, player))
    connect_areas(world, "Region 2 - Sector 4",       "Region 4 - Entrance",      lambda state: wizard_true_defeat(state, player))
    connect_areas(world, "Region 4 - Entrance",       "Region 2 - Sector 4",      lambda state: wizard_true_defeat(state, player))
    connect_areas(world, "Region 4 - Entrance",       "Region 4 - Upper",         lambda state: can_dash_attack(state, player)            and defeated_spearman(state, player))
    connect_areas(world, "Region 4 - Upper",          "Region 4 - Central",       lambda state: can_dash_attack(state, player)            and can_parry(state, player))
    connect_areas(world, "Region 4 - Central",        "Region 4 - Lower",         lambda state: can_dash(state, player)                   and can_parry(state, player)                  and can_press_green_buttons(state, player))
    connect_areas(world, "Region 3",                  "Region 4 - Lower",         lambda state: can_solve_flower_puzzle(state, player))
    connect_areas(world, "Region 3",                  "Collapse",                 lambda state: collapse_available(state, player))
    connect_areas(world, "Region 2 - Sector 2",       "Smile Shop",               lambda state: can_dash(state, player)                   and can_press_green_buttons(state, player))
    connect_areas(world, "Smile Shop",                "Region 1 - Central",       lambda state: True)
    connect_areas(world, "Region 2 - Lower",          "Dark Region",              lambda state: can_dash(state, player))
    connect_areas(world, "Dark Region",               "Region 3",                 lambda state: can_dash(state, player))
    connect_areas(world, "Dark Region",               "Smile Shop",               lambda state: can_dash_attack(state, player))
    connect_areas(world, "Region 2 - Left",           "The Between",              lambda state: can_dash(state, player))
    connect_areas(world, "The Between",               "Region 2 - Left",          lambda state: True)
    connect_areas(world, "The Between",               "Smile Shop",               lambda state: can_dash(state, player))
    connect_areas(world, "Menu",                      "Act 1",                    lambda state: act_1_available(state, player))
    connect_areas(world, "Menu",                      "Act 2",                    lambda state: act_2_available(state, player))
    connect_areas(world, "Menu",                      "Act 3",                    lambda state: act_3_available(state, player))
    connect_areas(world, "Act 1",                     "Act 2",                    lambda state: void_gate_open(state, player)             and can_dash_attack(state, player))
    connect_areas(world, "Act 2",                     "Act 3",                    lambda state: can_fight(state, player, world)           and can_dash_attack(state, player))
    connect_areas(world, "Act 1",                     "Epilogue",                 lambda state: can_dash(state, player)                   and state.has("Shroud", player))


def set_rules(world: "GlyphsWorld"):
    player = world.player
    options = world.options
    state = CollectionState(world.multiworld) 


    # Locations
    # ----------------------location_name-----------------------------------------conditions---------------------------------------------------------

    # Event Locations
    set_rule_from_string(world, "Defeat Runic Construct",              lambda state: can_fight_parryable_enemy(state, player, world))
    set_rule_from_string(world, "Stalker Sigil 1",                     lambda state: stalker_sigils_present(state, player))
    set_rule_from_string(world, "Serpent Lock 1",                      lambda state: can_dash(state, player))
    set_rule_from_string(world, "Serpent Lock 2",                      lambda state: can_dash(state, player)                     and can_press_green_buttons(state, player))
    set_rule_from_string(world, "Serpent Lock 3",                      lambda state: True)
    set_rule_from_string(world, "Defeat Gilded Serpent",               lambda state: can_dash(state, player)                     and serpent_door_open(state, player)                and can_fight(state, player, world))
    set_rule_from_string(world, "Stalker Sigil 2",                     lambda state: stalker_sigils_present(state, player)       and can_dash(state, player)                         and can_press_green_buttons(state, player))
    set_rule_from_string(world, "Stalker Sigil 3",                     lambda state: stalker_sigils_present(state, player))
    set_rule_from_string(world, "Solve Flower Puzzle",                 lambda state: can_dash(state, player)                     and can_press_green_buttons(state, player)          and has_grapple(state, player)                                      and defeated_gilded_serpent(state, player))
    set_rule_from_string(world, "Collapse Unlock",                     lambda state: can_dash(state, player)                     and wizard_fight_available(state, player, world)    and can_fight_parryable_enemy(state, player, world))
    set_rule_from_string(world, "Wizard True Defeat",                  lambda state: can_dash_attack(state, player)              and wizard_fight_available(state, player, world)    and can_fight_parryable_enemy(state, player, world))
    set_rule_from_string(world, "Defeat Spearman",                     lambda state: can_dash_attack(state, player)              and can_press_green_buttons(state, player)          and has_grapple(state, player)                                      and defeated_gilded_serpent(state, player))
    set_rule_from_string(world, "Good Ending",                         lambda state: can_fight(state, player, world)             and can_dash_attack(state, player)                  and can_parry(state, player)                                        and has_grapple(state, player)                          and wraith_fight_available(state, player, world)    and state.has("Gold Shard", player, 3))
    set_rule_from_string(world, "Last Fracture",                       lambda state: has_clarity(state, player)                  and wraith_fight_available(state, player, world)    and state.has("Good Ending", player))
    set_rule_from_string(world, "False Ending",                        lambda state: can_dash(state, player)                     and has_grapple(state, player))
    set_rule_from_string(world, "Smilemask Ending",                    lambda state: state.has("Smile Token", player, 10))
    set_rule_from_string(world, "Defeat Null",                         lambda state: can_dash_attack(state, player)              and has_grapple(state, player)                      and has_sword(state, player))
    set_rule_from_string(world, "Clarity",                             lambda state: defeated_null(state, player)                and state.has("Rune Cube", player, 3))
    set_rule_from_string(world, "Perfect Clarity",                     lambda state: defeated_null(state, player)                and state.has("Rune Cube", player, 3)               and (state.has("Shroud", player)                                    or state.has("Progressive Essence of George", player, 1)))
    set_rule_from_string(world, "Omnipotence Ending",                  lambda state: can_dash(state, player)                     and void_gate_open(state, player))
    set_rule_from_string(world, "Clear Act 1",                         lambda state: void_gate_open(state, player)               and can_dash_attack(state, player)                  and has_grapple(state, player)                                      and state.has("Shroud", player))
    set_rule_from_string(world, "Clear Act 2",                         lambda state: has_sword(state, player)                    and can_dash_attack(state, player)                  and (state.has("Shroud", player)                                    or state.has("Progressive Essence of George", player, 1))     and has_grapple(state, player)                      and can_parry(state, player)            and state.has("Gold Shard", player, 1))
    set_rule_from_string(world, "True Ending",                         lambda state: can_fight(state, player, world)             and can_parry(state, player)                        and (state.has("Shroud", player)                                    or state.has("Progressive Essence of George", player, 1))     and state.has("Gold Shard", player, 3))
    set_rule_from_string(world, "Epilogue Ending",                     lambda state: can_dash(state, player)                     and has_grapple(state, player)                      and state.has("Shroud", player)                                     and state.has("Progressive Essence of George", player, 1))

    # Starting Item
    set_rule_from_string(world, "Starting Item",                       lambda state: True)

    # Region 1
    set_rule_from_string(world, "Sword Pedestal",                      lambda state: True)
    set_rule_from_string(world, "Runic Construct Reward",              lambda state: defeated_runic_construct(state, player))
    set_rule_from_string(world, "Map Pedestal",                        lambda state: can_dash(state, player))
    set_rule_from_string(world, "Silver Shard Puzzle 1",               lambda state: can_dash(state, player))
    set_rule_from_string(world, "Silver Shard Puzzle 2",               lambda state: can_dash(state, player)                     and has_grapple(state, player))
    set_rule_from_string(world, "Silver Shard Puzzle 3",               lambda state: can_dash(state, player))
    set_rule_from_string(world, "Smile Token Puzzle 3",                lambda state: can_dash(state, player)                     and has_grapple(state, player))
    set_rule_from_string(world, "Smile Token Puzzle 9",                lambda state: can_dash(state, player))
    set_rule_from_string(world, "Color Cypher Room Pickup",            lambda state: can_dash(state, player))
    set_rule_from_string(world, "Master Puzzle 2",                     lambda state: can_dash(state, player)                     and has_grapple(state, player))


    # Region 2
    set_rule_from_string(world, "Silver Shard Puzzle 4",               lambda state: can_dash(state, player))
    set_rule_from_string(world, "Silver Shard Puzzle 5",               lambda state: can_dash(state, player)                     and can_press_green_buttons(state, player))
    set_rule_from_string(world, "Silver Shard Puzzle 6",               lambda state: can_dash(state, player)                     and can_press_green_buttons(state, player))
    set_rule_from_string(world, "Silver Shard Puzzle 7",               lambda state: can_dash(state, player)                     and can_press_green_buttons(state, player))
    set_rule_from_string(world, "Silver Shard Puzzle 8",               lambda state: can_dash(state, player))
    set_rule_from_string(world, "Silver Shard Puzzle 9",               lambda state: can_dash(state, player)                     and (options.DashPuzzlesSolved.value                or state.can_reach_location("Color Cypher Room Pickup", player)))
    set_rule_from_string(world, "Silver Shard Puzzle 15",              lambda state: can_dash(state, player)                     and can_press_green_buttons(state, player)          and (defeated_gilded_serpent(state, player)                         or can_fight(state, player, world)))
    set_rule_from_string(world, "Smile Token Puzzle 1",                lambda state: can_dash(state, player))
    set_rule_from_string(world, "Smile Token Puzzle 6",                lambda state: can_dash(state, player)                     and defeated_gilded_serpent(state, player))
    set_rule_from_string(world, "Smile Token Puzzle 8",                lambda state: can_dash(state, player))
    set_rule_from_string(world, "Smile Token Puzzle 10",               lambda state: can_dash_attack(state, player)              and can_parry(state, player)                        and has_grapple(state, player))
    set_rule_from_string(world, "Gilded Serpent Reward",               lambda state: defeated_gilded_serpent(state, player))
    set_rule_from_string(world, "Cameo Room Pickup",                   lambda state: can_dash(state, player))
    set_rule_from_string(world, "Car Hall Pickup",                     lambda state: can_dash(state, player))
    set_rule_from_string(world, "Near Shooters Pickup",                lambda state: can_dash(state, player))
    set_rule_from_string(world, "Collapsed Tunnel Pickup",             lambda state: True)
    set_rule_from_string(world, "Nest Room Pickup",                    lambda state: can_dash(state, player))
    set_rule_from_string(world, "Serpent Boss Room Pickup",            lambda state: can_dash(state, player)                     and (options.LogicalWallJumps.value                 or (state.can_reach_region("Region 2 - Serpent Upper", player)      and can_press_green_buttons(state, player)              and defeated_gilded_serpent(state, player))))
    set_rule_from_string(world, "Shadow Chase Reward",                 lambda state: can_dash(state, player)                     and has_grapple(state, player)                      and can_press_green_buttons(state, player))
    set_rule_from_string(world, "Water Room Pickup",                   lambda state: can_solve_flower_puzzle(state, player))
    set_rule_from_string(world, "George Reward 1",                     lambda state: can_dash(state, player)                     and state.has("Seeds", player, 10))
    set_rule_from_string(world, "George Reward 2",                     lambda state: can_dash(state, player)                     and state.has("Seeds", player, 10))
    set_rule_from_string(world, "Shadow Chase Pickup",                 lambda state: can_dash(state, player)                     and has_grapple(state, player)                      and can_press_green_buttons(state, player))
    set_rule_from_string(world, "Master Puzzle 1",                     lambda state: can_dash(state, player)                     and state.has("Silver Shard", player, 15)           and (options.DashPuzzlesSolved.value                                or can_access_all_silver_shards(state, player)))


    # Region 3
    set_rule_from_string(world, "Green Stone Trial",                   lambda state: can_dash(state, player)                     and has_grapple(state, player)                      and can_press_green_buttons(state, player))
    set_rule_from_string(world, "Blue Stone Trial",                    lambda state: can_dash(state, player)                     and has_grapple(state, player)                      and can_press_green_buttons(state, player))
    set_rule_from_string(world, "Red Stone Trial",                     lambda state: can_dash(state, player)                     and has_grapple(state, player)                      and can_fight(state, player, world))
    set_rule_from_string(world, "Silver Shard Puzzle 10",              lambda state: can_dash(state, player)                     and has_grapple(state, player)                      and can_press_green_buttons(state, player))
    set_rule_from_string(world, "Silver Shard Puzzle 11",              lambda state: can_dash(state, player)                     and has_grapple(state, player)                      and can_press_green_buttons(state, player))
    set_rule_from_string(world, "Silver Shard Puzzle 12",              lambda state: can_dash(state, player))
    set_rule_from_string(world, "Silver Shard Puzzle 13",              lambda state: can_dash(state, player)                     and has_grapple(state, player))
    set_rule_from_string(world, "Silver Shard Puzzle 14",              lambda state: can_dash(state, player)                     and has_grapple(state, player)                      and can_press_green_buttons(state, player))
    set_rule_from_string(world, "Smile Token Puzzle 2",                lambda state: can_dash(state, player)                     and has_grapple(state, player))
    set_rule_from_string(world, "Smile Token Puzzle 7",                lambda state: can_dash(state, player)                     and has_grapple(state, player)                      and can_press_green_buttons(state, player))
    set_rule_from_string(world, "Wizard Reward",                       lambda state: can_dash_attack(state, player)              and wizard_fight_available(state, player, world)    and can_fight_parryable_enemy(state, player, world))
    set_rule_from_string(world, "Master Puzzle 3",                     lambda state: can_dash_attack(state, player)              and has_grapple(state, player)                      and has_sword(state, player))
    

    # Region 4
    set_rule_from_string(world, "Spearman Reward",                     lambda state: can_dash_attack(state, player)              and has_grapple(state, player)                      and can_fight(state, player, world))
    set_rule_from_string(world, "Multiparry Gold Shard Puzzle",        lambda state: can_dash(state, player)                     and has_grapple(state, player)                      and can_parry(state, player))
    set_rule_from_string(world, "Platforming Gold Shard Room",         lambda state: can_dash(state, player)                     and has_grapple(state, player)                      and can_parry(state, player)                                        and has_sword(state, player))
    set_rule_from_string(world, "Flower Puzzle Reward",                lambda state: can_solve_flower_puzzle(state, player))
    set_rule_from_string(world, "Smile Token Puzzle 4",                lambda state: can_dash(state, player)                     and has_grapple(state, player)                      and can_parry(state, player))
    set_rule_from_string(world, "Smile Token Puzzle 5",                lambda state: can_dash(state, player))
    set_rule_from_string(world, "On top of the Rosetta Stone Pickup",  lambda state: can_dash(state, player))
    set_rule_from_string(world, "Long Parry Platforming Room Pickup",  lambda state: can_dash(state, player)                     and has_grapple(state, player)                      and can_parry(state, player)                                        and can_press_green_buttons(state, player))


    # Collapse
    set_rule_from_string(world, "Escape Normal Sequence Pickup",       lambda state: can_dash(state, player)                     and has_grapple(state, player))


    # Smile Shop
    set_rule_from_string(world, "Smile Shop Item 1",                   lambda state: can_dash(state, player)                     and state.has("Smile Token", player, 10))
    set_rule_from_string(world, "Smile Shop Item 2",                   lambda state: can_dash(state, player)                     and state.has("Smile Token", player, 10))
    set_rule_from_string(world, "Smile Shop Item 3",                   lambda state: can_dash_attack(state, player)              and state.has("Smile Token", player, 10))           # item normally not available until you have dash attack
    set_rule_from_string(world, "Smile Shop Item 4",                   lambda state: can_dash(state, player)                     and state.has("Smile Token", player, 10)            and can_parry(state, player))  # item not normally available until you have parry
    set_rule_from_string(world, "Dash Puzzle Reward",                  lambda state: can_dash(state, player))
    if world.options.UnreasonableLocations.value:
        set_rule_from_string(world, "Respawn Reward",                  lambda state: True)


    # Dark Region
    set_rule_from_string(world, "Secret Room Pickup",                  lambda state: can_dash_attack(state, player)              and has_grapple(state, player)                      and has_sword(state, player))
    set_rule_from_string(world, "Large Room Pickup in the Corner",     lambda state: can_dash_attack(state, player)              and has_grapple(state, player)                      and has_sword(state, player))
    set_rule_from_string(world, "Null Reward",                         lambda state: can_dash_attack(state, player)              and has_grapple(state, player)                      and has_sword(state, player))


    # The Between
    set_rule_from_string(world, "Between Reward 1",                    lambda state: state.has("Progressive Sword", player, 2)   and state.has("Progressive Dash Orb", player, 3)    and has_grapple(state, player)                                      and can_parry(state, player)                            and state.has("Progressive Essence of George", player, 1) and state.has("Shroud", player)         and state.has("Silver Shard", player, 15) and state.has("Gold Shard", player, 1))
    set_rule_from_string(world, "Between Reward 2",                    lambda state: state.has("Progressive Sword", player, 2)   and state.has("Progressive Dash Orb", player, 3)    and has_grapple(state, player)                                      and can_parry(state, player)                            and state.has("Progressive Essence of George", player, 1) and state.has("Shroud", player)         and state.has("Silver Shard", player, 15) and state.has("Gold Shard", player, 1))


    # Act 1
    set_rule_from_string(world, "Enter Void Reward",                   lambda state: True)
    set_rule_from_string(world, "Void Gate Shard Location 1",          lambda state: can_dash(state, player))
    set_rule_from_string(world, "Void Gate Shard Location 2",          lambda state: can_dash(state, player)                     and state.has("Shroud", player))
    set_rule_from_string(world, "Void Gate Shard Location 3",          lambda state: can_dash(state, player)                     or state.has("Shroud", player))
    set_rule_from_string(world, "Void Gate Shard Location 4",          lambda state: can_dash(state, player))
    set_rule_from_string(world, "Void Gate Shard Location 5",          lambda state: can_dash(state, player)                     and has_grapple(state, player))
    set_rule_from_string(world, "Void Gate Shard Location 6",          lambda state: can_dash(state, player))
    set_rule_from_string(world, "Void Gate Shard Location 7",          lambda state: can_dash(state, player))
    set_rule_from_string(world, "John Room Pickup",                    lambda state: can_dash(state, player))


    # Act 2
    set_rule_from_string(world, "Free Item",                           lambda state: True)
    set_rule_from_string(world, "Boss Rush Heal 1",                    lambda state: can_fight_parryable_enemy(state, player, world))
    set_rule_from_string(world, "Boss Rush Heal 2",                    lambda state: has_sword(state, player)                    and can_dash_attack(state, player)                  and (state.has("Shroud", player)                                    or state.has("Progressive Essence of George", player, 1)))
    set_rule_from_string(world, "Boss Rush Heal 3",                    lambda state: has_sword(state, player)                    and can_dash_attack(state, player)                  and (state.has("Shroud", player)                                    or state.has("Progressive Essence of George", player, 1)))
    set_rule_from_string(world, "Boss Rush Heal 4",                    lambda state: has_sword(state, player)                    and can_dash_attack(state, player)                  and (state.has("Shroud", player)                                    or state.has("Progressive Essence of George", player, 1))     and has_grapple(state, player))
    set_rule_from_string(world, "Pink Bow Pickup",                     lambda state: can_dash(state, player)                     or has_grapple(state, player))

    # Act 3
    set_rule_from_string(world, "Preminition Reward",                  lambda state: True)

    # Victory condition rule!
    victory: lambda state: False
    if options.Goal.value == options.Goal.option_false_ending:
        victory = lambda state: state.has("False Ending", player)
    elif options.Goal.value == options.Goal.option_good_ending:
        victory = lambda state: state.has("Good Ending", player)
    elif options.Goal.value == options.Goal.option_true_ending:
        victory = lambda state: state.has("True Ending", player)
    elif options.Goal.value == options.Goal.option_all_star_endings:
        victory = lambda state: state.has("Perfect Clarity", player) and state.has("Smilemask Ending", player) and state.has("Omnipotence Ending", player)
    elif options.Goal.value == options.Goal.option_epilogue:
        victory = lambda state: state.has("Epilogue Ending", player)
    elif options.Goal.value == options.Goal.option_all_endings:
        victory = lambda state: state.has("False Ending", player) and state.has("Good Ending", player) and state.has("True Ending", player) and state.has("Perfect Clarity", player) and state.has("Smilemask Ending", player) and state.has("Omnipotence Ending", player) and state.has("Epilogue Ending", player)
    world.multiworld.completion_condition[player] = victory

def connect_areas(world: "GlyphsWorld", source: str, target: str, rule=None) -> Entrance:
    sourceRegion = world.get_region(source)
    targetRegion = world.get_region(target)
    return sourceRegion.connect(targetRegion, rule=rule)

def set_rule_from_string(world: "GlyphsWorld", location_name: str, rule=None) -> None:
    set_rule(world.get_location(location_name), rule=rule)