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

def can_fight(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 1) or (state.has("Progressive Dash Orb", player, 2) and options.SwordlessCombat.value)

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
    return state.has("False Ending")

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