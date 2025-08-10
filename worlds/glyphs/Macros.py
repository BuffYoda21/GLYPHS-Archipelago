from BaseClasses import CollectionState
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import GlyphsWorld
    options = GlyphsWorld.options

def has_sword(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 1)

def can_dash(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Dash Orb", player, 1)

def can_dash_attack(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Dash Orb", player, 2)

def can_press_green_buttons(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 1) or state.has("Progressive Dash Orb", player, 2)

def can_fight(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 1) or (state.has("Progressive Dash Orb", player, 2) and options.SwordlessCombat.value)

def can_warp(state: CollectionState, player: int) -> bool:
    return state.has("Map", player)

def has_grapple(state: CollectionState, player: int) -> bool:
    return state.has("Grapple", player)

def can_parry(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Parry", player, 1)

def can_fight_parryable_enemy(state: CollectionState, player: int) -> bool:
    return (
        state.has("Progressive Sword", player, 1)
        or (
            (
                state.has("Progressive Dash Orb", player, 2)
                or (state.has("Progressive Parry", player, 1) and options.GenericParries.value)
            )
            and options.SwordlessCombat.value
        )
    )

def serpent_door_open(state: CollectionState, player: int) -> bool:
    return state.has("Serpent Lock Activated", player, 3)

def stalker_sigils_present(state: CollectionState, player: int) -> bool:
    return state.has("False Ending", player)

def shadow_chase_open(state: CollectionState, player: int) -> bool:
    return state.has("Stalker Sigil Collected", player, 3)

def has_clarity(state: CollectionState, player: int) -> bool:
    return state.has("Clarity", player)

def wizard_fight_available(state: CollectionState, player: int) -> bool:
    return state.has("Glyphstones", player, options.WizardRequirements.value)

def wraith_fight_available(state: CollectionState, player: int) -> bool:
    if options.WraithRequirements.value == options.WraithRequirements.none:
        return True
    if options.WraithRequirements.value == options.WraithRequirements.vanilla:
        return state.has("Silver Shard", player, 15)
    if options.WraithRequirements.value == options.WraithRequirements.intended:
        return state.has("Silver Shard", player, 15) and state.has("Glyphstone", player, 3)
    if options.WraithRequirements.value == options.WraithRequirements.silver_shards:
        return has_wraith_silvers(state, player)
    if options.WraithRequirements.value == options.WraithRequirements.gold_shards:
        return has_wraith_golds(state, player)
    if options.WraithRequirements.value == options.WraithRequirements.smile_tokens:
        return has_wraith_smiles(state, player)
    if options.WraithRequirements.value == options.WraithRequirements.rune_cubes:
        return has_wraith_runes(state, player)
    if options.WraithRequirements.value == options.WraithRequirements.glyphstones:
        return has_wraith_glyphstones(state, player)
    return False

def has_wraith_silvers(state: CollectionState, player: int) -> bool:
    return state.has("Silver Shard", player, options.WraithSilverCount.value)

def has_wraith_golds(state: CollectionState, player: int) -> bool:
    return state.has("Gold Shard", player, options.WraithGoldCount.value)

def has_wraith_smiles(state: CollectionState, player: int) -> bool:
    return state.has("Smile Token", player, options.WraithSmileCount.value)

def has_wraith_runes(state: CollectionState, player: int) -> bool:
    return state.has("Rune Cube", player, options.WraithRuneCount.value)

def has_wraith_glyphstones(state: CollectionState, player: int) -> bool:
    return state.has("Glyphstone", player, options.WraithGlyphstoneCount.value)

def defeated_runic_construct(state: CollectionState, player: int) -> bool:
    return state.has("Runic Construct Defeated", player)

def defeated_gilded_serpent(state: CollectionState, player: int) -> bool:
    return state.has("Gilded Serpent Defeated", player)

def collapse_available(state: CollectionState, player: int) -> bool:
    return state.has("Collapse Unlocked", player)

def wizard_true_defeat(state: CollectionState, player: int) -> bool:
    return state.has("Wizard True Defeat", player)

def defeated_spearman(state: CollectionState, player: int) -> bool:
    return state.has("Spearman Defeated", player)

def defeated_null(state: CollectionState, player: int) -> bool:
    return state.has("Defeat Null", player)

def act_1_available(state: CollectionState, player: int) -> bool:
    return state.has("Act 1 Unlocked", player)

def act_2_available(state: CollectionState, player: int) -> bool:
    return state.has("Act 2 Unlocked", player)

def act_3_available(state: CollectionState, player: int) -> bool:
    return state.has("Act 3 Unlocked", player)

def void_gate_open(state: CollectionState, player: int) -> bool:
    return state.has("Void Gate Shard", player, 7)

def can_solve_flower_puzzle(state: CollectionState, player: int) -> bool:
    return defeated_gilded_serpent(state, player) and can_dash(state, player) and can_press_green_buttons(state, player) and has_grapple(state, player)

def can_access_all_silver_shards(state: CollectionState, player: int) -> bool:
    return (
        state.can_reach_location("Silver Shard Puzzle 1", player) and
        state.can_reach_location("Silver Shard Puzzle 2", player) and
        state.can_reach_location("Silver Shard Puzzle 3", player) and
        state.can_reach_location("Silver Shard Puzzle 4", player) and
        state.can_reach_location("Silver Shard Puzzle 5", player) and
        state.can_reach_location("Silver Shard Puzzle 6", player) and
        state.can_reach_location("Silver Shard Puzzle 7", player) and
        state.can_reach_location("Silver Shard Puzzle 8", player) and
        state.can_reach_location("Silver Shard Puzzle 9", player) and
        state.can_reach_location("Silver Shard Puzzle 10", player) and
        state.can_reach_location("Silver Shard Puzzle 11", player) and
        state.can_reach_location("Silver Shard Puzzle 12", player) and
        state.can_reach_location("Silver Shard Puzzle 13", player) and
        state.can_reach_location("Silver Shard Puzzle 14", player) and
        state.can_reach_location("Silver Shard Puzzle 15", player)
    )