from typing import List, Dict, Any
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import DeathLink, OptionGroup

from .glyphs.Options import *
from .apquest.options import *

def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in combo_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list

@dataclass
class ComboOptions(PerGameCommonOptions):
    # GLYPHS
    Goal:                           Goal
    StartingSword:                  StartingSword
    StartingDash:                   StartingDash
    DeathLink:                      DeathLink
    RandomShopPrices:               RandomShopPrices
    RandomButtonColorPercent:       RandomButtonColorPercent
    ExcludeBlack:                   ExcludeBlack
    ButtonShardPercent:             ButtonShardPercent
    EnableTraps:                    EnableTraps
    TrapTypes:                      TrapTypes
    HatShuffle:                     HatShuffle
    SwordlessCombat:                SwordlessCombat
    DashPuzzlesSolved:              DashPuzzlesSolved
    LogicalWallJumps:               LogicalWallJumps
    FlowerPuzzleSkips:              FlowerPuzzleSkips
    WizardRequirements:             WizardRequirements
    WraithRequirements:             WraithRequirements
    WraithSilverCount:              WraithSilverCount
    WraithGoldCount:                WraithGoldCount
    WraithSmileCount:               WraithSmileCount
    WraithRuneCount:                WraithRuneCount
    WraithGlyphstoneCount:          WraithGlyphstoneCount

    # APQUEST
    hard_mode:                      HardMode
    hammer:                         Hammer
    extra_starting_chest:           ExtraStartingChest
    start_with_one_confetti_cannon: StartWithOneConfettiCannon
    trap_chance:                    TrapChance
    confetti_explosiveness:         ConfettiExplosiveness
    player_sprite:                  PlayerSprite
    
combo_option_groups: Dict[str, List[Any]] = {
    "GLYPHS Options": [Goal, StartingSword, StartingDash, DeathLink, RandomShopPrices, RandomButtonColorPercent, ExcludeBlack, ButtonShardPercent, EnableTraps, TrapTypes, HatShuffle, SwordlessCombat, DashPuzzlesSolved, LogicalWallJumps, FlowerPuzzleSkips, WizardRequirements, WraithRequirements, WraithSilverCount, WraithGoldCount, WraithSmileCount, WraithRuneCount, WraithGlyphstoneCount],
    "APQUEST Options": [HardMode, Hammer, ExtraStartingChest, StartWithOneConfettiCannon, TrapChance, ConfettiExplosiveness, PlayerSprite],
}