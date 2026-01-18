from BaseClasses import CollectionState
from typing import TYPE_CHECKING
from .Options import GlyphsOptions

options: GlyphsOptions

if TYPE_CHECKING:
    from . import GlyphsWorld

def has_sword(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 1)

def can_dash(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Dash Orb", player, 1)

def can_dash_attack(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Dash Orb", player, 2)

def can_wall_jump(state: CollectionState, player: int, world: "GlyphsWorld") -> bool:
    return can_dash(state, player) and world.options.LogicalWallJumps.value

## Logically will never be needed
# def can_chain_wall_jumps(state: CollectionState, player: int, world: "GlyphsWorld") -> bool:
#     return can_wall_jump(state, player, world) and world.options.LogicalWallJumpChains.value

def can_press_green_buttons(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 1) or state.has("Progressive Dash Orb", player, 2)

def can_fight(state: CollectionState, player: int, world: "GlyphsWorld") -> bool:
    return state.has("Progressive Sword", player, 1) or (state.has("Progressive Dash Orb", player, 2) and world.options.SwordlessCombat.value)

def can_warp(state: CollectionState, player: int) -> bool:
    return state.has("Map", player)

def has_grapple(state: CollectionState, player: int) -> bool:
    return state.has("Grapple", player)

def can_parry(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Parry", player, 1)

def serpent_door_open(state: CollectionState, player: int) -> bool:
    return state.has("Serpent Lock 1", player) and state.has("Serpent Lock 2", player) and state.has("Serpent Lock 3", player)

def stalker_sigils_present(state: CollectionState, player: int) -> bool:
    return state.has("False Ending", player)

def shadow_chase_open(state: CollectionState, player: int) -> bool:
    return state.has("Stalker Sigil 1", player) and state.has("Stalker Sigil 2", player) and state.has("Stalker Sigil 3", player)

def has_clarity(state: CollectionState, player: int) -> bool:
    return state.has("Clarity", player)

def wizard_fight_available(state: CollectionState, player: int, world: "GlyphsWorld") -> bool:
    return state.has("Glyphstone", player, world.options.WizardRequirements.value)

def wraith_fight_available(state: CollectionState, player: int, world: "GlyphsWorld") -> bool:
    key = world.options.WraithRequirements.current_key.lower()
    if key == "none":
        return True
    if key == "vanilla":
        return state.has("Silver Shard", player, 15)
    if key == "intended":
        return state.has("Silver Shard", player, 15) and state.has("Glyphstone", player, 3)
    if key == "silver_shards":
        return has_wraith_silvers(state, player, world)
    if key == "gold_shards":
        return has_wraith_golds(state, player, world)
    if key == "smile_tokens":
        return has_wraith_smiles(state, player, world)
    if key == "rune_cubes":
        return has_wraith_runes(state, player, world)
    if key == "glyphstones":
        return has_wraith_glyphstones(state, player, world)
    return False

def has_wraith_silvers(state: CollectionState, player: int, world: "GlyphsWorld") -> bool:
    return state.has("Silver Shard", player, world.options.WraithSilverCount.value)

def has_wraith_golds(state: CollectionState, player: int, world: "GlyphsWorld") -> bool:
    return state.has("Gold Shard", player, world.options.WraithGoldCount.value)

def has_wraith_smiles(state: CollectionState, player: int, world: "GlyphsWorld") -> bool:
    return state.has("Smile Token", player, world.options.WraithSmileCount.value)

def has_wraith_runes(state: CollectionState, player: int, world: "GlyphsWorld") -> bool:
    return state.has("Rune Cube", player, world.options.WraithRuneCount.value)

def has_wraith_glyphstones(state: CollectionState, player: int, world: "GlyphsWorld") -> bool:
    return state.has("Glyphstone", player, world.options.WraithGlyphstoneCount.value)

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

def can_start_flower_puzzle(state: CollectionState, player: int) -> bool:
    return state.can_reach_region("Region 1E", player) and can_dash(state, player)

def can_solve_flower_puzzle(state: CollectionState, player: int) -> bool:
    return can_start_flower_puzzle(state, player) and defeated_gilded_serpent(state, player) and can_dash(state, player) and can_press_green_buttons(state, player) and has_grapple(state, player)

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

def unlocked_gimmick(gimmick: str, state: CollectionState, player: int, world: "GlyphsWorld") -> bool:
    if not gimmick in world.options.GimmickRando.value:
        return True
    return state.has(gimmick, player)