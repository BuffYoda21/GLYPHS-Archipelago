from collections.abc import Callable

from BaseClasses import CollectionState
from typing import TYPE_CHECKING

from .Buttons import get_button_color
from .Types import ButtonColor

if TYPE_CHECKING:
    from . import GlyphsWorld

def set_macro_rules(state: CollectionState, world: "GlyphsWorld") -> None:
    player = world.player

    if world.options.LogicalWallJumps.value:
        world.wall_jump_rule = lambda state: can_dash(state, player)
    else:
        world.wall_jump_rule = lambda state: False

    if world.options.SwordlessCombat.value:
        world.can_fight_rule = lambda state: state.has("Progressive Sword", player, 1) or state.has("Progressive Dash Orb", player, 2)
    else:
        world.can_fight_rule = lambda state: state.has("Progressive Sword", player, 1)

    required_glyphstones = world.options.WizardRequirements.value
    world.wizard_available_rule = lambda state: state.has("Glyphstone", player, required_glyphstones)

    key = world.options.WraithRequirements.current_key.lower()
    if key == "none":
        world.wraith_available_rule = lambda state: True
    elif key == "vanilla":
        world.wraith_available_rule = lambda state: state.has("Silver Shard", player, 15)
    elif key == "intended":
        world.wraith_available_rule = lambda state: state.has("Silver Shard", player, 15) and state.has("Glyphstone", player, 3)
    elif key == "silver_shards":
        count = world.options.WraithSilverCount.value
        world.wraith_available_rule = lambda state: state.has("Silver Shard", player, count)
    elif key == "gold_shards":
        count = world.options.WraithGoldCount.value
        world.wraith_available_rule = lambda state: state.has("Gold Shard", player, count)
    elif key == "smile_tokens":
        count = world.options.WraithSmileCount.value
        world.wraith_available_rule = lambda state: state.has("Smile Token", player, count)
    elif key == "rune_cubes":
        count = world.options.WraithRuneCount.value
        world.wraith_available_rule = lambda state: state.has("Rune Cube", player, count)
    elif key == "glyphstones":
        count = world.options.WraithGlyphstoneCount.value
        world.wraith_available_rule = lambda state: state.has("Glyphstone", player, count)

    world.macro_init = True

def has_sword(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 1)

def can_dash(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Dash Orb", player, 1)

def can_dash_attack(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Dash Orb", player, 2)

def can_wall_jump(state: CollectionState, world: "GlyphsWorld") -> bool:
    return world.wall_jump_rule(state)

## Logically will never be needed
# def can_chain_wall_jumps(state: CollectionState, player: int, world: "GlyphsWorld") -> bool:
#     return can_wall_jump(state, player, world) and world.options.LogicalWallJumpChains.value

def can_press_buttons(state: CollectionState, player: int, world: "GlyphsWorld", button_list: list[str], allowedFaults: int=0) -> bool:
    items = state.prog_items[player]
    prog_dash = items["Progressive Dash Orb"]
    has_parry = items["Progressive Parry"] >= 1
    has_sword = items["Progressive Sword"] >= 1
    faults = 0

    for key in button_list:
        button = world.buttons[key]

        if button.isBroken and not items[button.shardName]:
            faults += 1
        elif button.color == ButtonColor.PINK:
            faults += not has_parry
        elif button.color == ButtonColor.BLUE:
            faults += prog_dash < 1
        elif button.color == ButtonColor.YELLOW:
            faults += prog_dash < 2
        elif button.color == ButtonColor.GREEN:
            faults += prog_dash < 2 and not has_sword

        if faults > allowedFaults:
            return False

    return True

def can_press_button(state: CollectionState, player: int, world: "GlyphsWorld", key: str) -> bool:
    return can_press_buttons(state, player, world, [key])

def between_buttons_missing(state: CollectionState, player: int, world: "GlyphsWorld") -> int:
    """
    DEPRICATED
    Use between_completion instead
    """
    count = 0
    if not can_press_button(state, player, world, "Between rm1"):
        count += 1
    if not can_press_button(state, player, world, "Between rm4"):
        count += 1
    if not can_press_button(state, player, world, "Between rm5"):
        count += 1
    if not can_press_button(state, player, world, "Between rm10"):
        count += 1
    if not can_press_button(state, player, world, "Between rm13"):
        count += 1
    if not can_press_button(state, player, world, "Between rm19"):
        count += 1
    if not can_press_button(state, player, world, "Between rm28"):
        count += 1
    if not can_press_button(state, player, world, "Between rm30"):
        count += 1
    if not can_press_button(state, player, world, "Between rm39"):
        count += 1
    if not can_press_button(state, player, world, "Between rm40"):
        count += 1
    if not can_press_button(state, player, world, "Between rm43 Button 1"):
        count += 1
    if not can_press_button(state, player, world, "Between rm43 Button 2"):
        count += 1
    if not can_press_button(state, player, world, "Between rm57"):
        count += 1
    if not can_press_button(state, player, world, "Between rm66"):
        count += 1
    if not can_press_button(state, player, world, "Between rm71"):
        count += 1
    if not can_press_button(state, player, world, "Between Pre-Boss 1"):
        count += 1
    return count

def between_completion(state: CollectionState, player: int, world: "GlyphsWorld", missing_allowed: int=0) -> bool:
    buttons_to_check = ["Between rm1", "Between rm4", "Between rm5", "Between rm10", "Between rm13", "Between rm19", "Between rm28", "Between rm30", "Between rm39",
                        "Between rm40", "Between rm43 Button 1", "Between rm43 Button 2", "Between rm57", "Between rm66", "Between rm71", "Between Pre-Boss 1"]
    return can_press_buttons(state, player, world, buttons_to_check, missing_allowed)

def can_press_green_buttons(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 1) or state.has("Progressive Dash Orb", player, 2)

def can_fight(state: CollectionState, world: "GlyphsWorld") -> bool:
    return world.can_fight_rule(state)

def can_warp(state: CollectionState, player: int) -> bool:
    return state.has("Map", player)

def has_grapple(state: CollectionState, player: int) -> bool:
    return state.has("Grapple", player)

def can_parry(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Parry", player, 1)

def serpent_door_open(state: CollectionState, player: int, world: "GlyphsWorld") -> bool:
    return state.has("Serpent Lock 1", player) and state.has("Serpent Lock 2", player) and state.has("Serpent Lock 3", player) and can_press_button(state, player, world, "R2B Gate Left")

def stalker_sigils_present(state: CollectionState, player: int) -> bool:
    return state.has("False Ending", player)

def shadow_chase_open(state: CollectionState, player: int, world: "GlyphsWorld") -> bool:
    return state.has("Stalker Sigil 1", player) and state.has("Stalker Sigil 2", player) and state.has("Stalker Sigil 3", player) and can_press_button(state, player, world, "R2J Gate Left")

def has_clarity(state: CollectionState, player: int) -> bool:
    return state.has("Clarity", player)

def wizard_fight_available(state: CollectionState, world: "GlyphsWorld") -> bool:
    return world.wizard_available_rule(state)

def wraith_fight_available(state: CollectionState, world: "GlyphsWorld") -> bool:
    return world.wraith_available_rule(state)

def defeated_runic_construct(state: CollectionState, player: int) -> bool:
    return state.has("Defeat Runic Construct", player)

def defeated_gilded_serpent(state: CollectionState, player: int) -> bool:
    return state.has("Defeat Gilded Serpent", player)

def collapse_available(state: CollectionState, player: int) -> bool:
    return state.has("Collapse Unlock", player)

def wizard_true_defeat(state: CollectionState, player: int) -> bool:
    return state.has("Wizard True Defeat", player)

def defeated_spearman(state: CollectionState, player: int) -> bool:
    return state.has("Defeat Spearman", player)

def defeated_null(state: CollectionState, player: int) -> bool:
    return state.has("Defeat Null", player)

def act_1_available(state: CollectionState, player: int) -> bool:
    return state.has("Last Fracture", player)

def act_2_available(state: CollectionState, player: int) -> bool:
    return state.has("Clear Act 1", player)

def act_3_available(state: CollectionState, player: int) -> bool:
    return state.has("Clear Act 2", player)

def void_gate_open(state: CollectionState, player: int) -> bool:
    return state.has("Void Gate Shard", player, 7)

# depricated
def can_start_flower_puzzle(state: CollectionState, player: int) -> bool:
    """
    If used in an entrance access rule, wrap with `multiworld.register_indirect_condition(world.get_region("Region 1E"), <foo>)`.
    """
    return state.can_reach_region("Region 1E", player) and can_dash(state, player)

# depricated
def can_solve_flower_puzzle(state: CollectionState, player: int) -> bool:
    """
    If used in an entrance access rule, wrap with `multiworld.register_indirect_condition(world.get_region("Region 1E"), <foo>)`.
    """
    return can_start_flower_puzzle(state, player) and defeated_gilded_serpent(state, player) and can_dash(state, player) and can_press_green_buttons(state, player) and has_grapple(state, player)

def flower_puzzle_completion(state: CollectionState, player: int, world: "GlyphsWorld") -> int:
    """
    If used in an entrance access rule, wrap with `multiworld.register_indirect_condition(world.get_region("Region 1E"), <foo>)`.
    """
    completion = 0
    wall_jump = can_wall_jump(state, world)
    if state.can_reach_region("Region 1E", player) and can_dash(state, player) and can_press_buttons(state, player, world, ["R1B 4th Lowest", "R1B 5th Lowest"]) and (wall_jump or can_press_button(state, player, world, "R1B 6th Lowest")):
        completion += 1
    else:
        return completion
    if can_press_buttons(state, player, world, ["R1B Map Room", "R2A Gate Left", "R2A Upper", "R2G Lower", "R2G Middle", "R2G Moving Platform", "R2N Chase 1"]) and (wall_jump or can_press_button(state, player, world, "R1F Right")) and (can_parry(state, player) or (get_button_color(world, "R2G Upper Middle") != ButtonColor.BLACK and can_press_buttons(state, player, world, ["R2G Upper Left", "R2G Upper Middle"]))):
        completion += 1
    else:
        return completion
    if defeated_gilded_serpent(state, player) and has_grapple(state, player) and can_press_button(state, player, world, "R2P Left"):
        completion += 1
    return completion

def can_access_all_silver_shards(state: CollectionState, player: int) -> bool:
    return (
        state.can_reach_location("(R1) Silver Shard Puzzle 1 - Map", player) and
        state.can_reach_location("(R1) Silver Shard Puzzle 2 - Grapple", player) and
        state.can_reach_location("(R1) Silver Shard Puzzle 3 - Spike Tunnel", player) and
        state.can_reach_location("(R2S1) Silver Shard Puzzle 4 - Save Button", player) and
        state.can_reach_location("(R2) Silver Shard Puzzle 5 - Respawn", player) and
        state.can_reach_location("(R2) Silver Shard Puzzle 6 - Invisible", player) and
        state.can_reach_location("(R2S2) Silver Shard Puzzle 7 - Timed", player) and
        state.can_reach_location("(R2) Silver Shard Puzzle 8 - Avoid Respawn", player) and
        state.can_reach_location("(R2) Silver Shard Puzzle 9 - Color Dash Puzzle", player) and
        state.can_reach_location("(R3) Silver Shard Puzzle 10 - Mirror", player) and
        state.can_reach_location("(R3) Silver Shard Puzzle 11 - No Dash", player) and
        state.can_reach_location("(R3) Silver Shard Puzzle 12 - QR", player) and
        state.can_reach_location("(R3) Silver Shard Puzzle 13 - Black Button", player) and
        state.can_reach_location("(R3) Silver Shard Puzzle 14 - Grapple", player) and
        state.can_reach_location("(R2) Silver Shard Puzzle 15 - Escape Serpent", player)
    )