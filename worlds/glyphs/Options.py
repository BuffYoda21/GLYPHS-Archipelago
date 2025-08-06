from typing import List, Dict, Any
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Choice, OptionGroup, OptionSet, Toggle, Range

# If youve ever gone to an options page and seen how sometimes options are grouped
# This is that
def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in glyphs_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list



# Game Options
class Goal(Choice):
    """
    Determines what ending must be reached for Archipelago to consider your game as complete.
    """
    display_name = "Completion Requirements"
    option_false_ending = 1
    option_good_ending = 2
    option_true_ending = 3
    option_all_star_endings = 4
    option_epilouge = 5
    option_all_endings = 6
    default = option_true_ending

class StartingSword(Toggle):
    """
    Start the game with the sword.
    """
    display_name = "Starting Sword"

class GenericParries(Toggle):
    """
    Allows normal damaging bullets to be parried.
    Parried bullets are 3x more powerful and move faster than normal.
    """
    display_name = "Generic Parries"

class Multiplayer(Toggle):
    """
    Enables multiplayer with other glyphs players in the multiworld that have this option enabled
    """
    display_name = "Multiplayer"



# Randomization Options
# class RandomizeWorldSpawn(Toggle):
#     """
#     Shuffles what save button you start on.
#     If false, you will start at the standard spawn point.
#     """
#     display_name = "Randomize World Spawn"

class LocationPool(Choice):
    """
    Determines what locations will be shuffled in the world.
    False Ending: Includes all locations relevent to the false ending
    Good Ending: Includes all locations relevent to the good ending
    Full Tomb: Like Good Ending but includes the between and master puzzles in the pool
    Outer Void: Includes Full Tomb and Outer Void locations
    """
    display_name = "Location Pool"
    option_false_ending = 1
    option_good_ending = 2
    option_full_tomb = 3
    option_outer_void = 4
    default = option_false_ending

class HatLocations(Toggle):
    """
    Adds hat puzzles to the location pool.
    If false, all hat puzzles will yield junk items.
    """
    display_name = "Include Hat Puzzles"

class Shopsanity(Toggle):
    """
    Shuffles smile shop items into the pool.
    Also removes the refund button (spend wisely).
    """
    display_name = "Shopsanity"

class RandomShopPrices(Toggle):
    """
    Randomizes the prices of shop items.
    Never exceeds 10 total (or 7 if only false ending locations are shuffled).
    """
    display_name = "Randomize Shop Prices"

class EnableTraps(Toggle):
    """
    Adds traps to the itempool
    """
    display_name = "Enable Traps"

class TrapTypes(OptionSet):
    """
    Determines what kinds of traps will be added to the item pool
    """
    display_name = "Trap Types"
    valid_keys = {
        "Smile Trap",
        "Enemy Trap",
        "John Trap",
        "Spear Trap",
        "Screen Flip Trap",
        "Instakill Trap",
    }

class UnreasonableLocations(Toggle):
    """
    Include unreasonable item locations in the item pool such as certain hats
    """
    display_name = "Shuffle Unreasonable Locations"



# Logical Options
class SwordlessCombat(Toggle):
    """
    Swordless combat is considered in logic.
    Ex: Fighting with only dash attacks
    """
    display_name = "Swordless Combat"

class BulletCombat(Toggle):
    """
    Considers defeating bosses with only parried projectiles in logic.
    Does nothing if Swordless Combat is not enabled.
    If Generic Parries is enabled, also includes relevant bosses.
    """
    display_name = "Parry Combat"

class DashPuzzlesSolved(Toggle):
    """
    Logic assumes you already have the answer to all the dash puzzles in the game.
    """
    display_name = "Assume Dash Puzzle Solution"

## Actually might be alot harder to implement than I thought
# class MultiplayerCheese(Toggle):
#     """
#     Considers skips made possible by multiplayer in logic.
#     Does nothing if multiplayer is not enabled or if there are no other players to connect to.
#     """
#     display_name = "Multiplayer Cheeses in Logic"

class LocicalWallJumps(Toggle):
    """
    Considers skips utilizing wall jumps in logic.
    """
    display_name = "Wall Jumps in Logic"

class LogicalWallJumpChains(Toggle):
    """
    Considers skips that require multiple consecutive wall jumps in logic.
    Does nothing if "Wall Jumps in Logic" is not enabled.
    """
    display_name = "Wall Jump Chains in Logic"



# Open Settings
class WizardRequirements(Range):
    """
    Determines the number of glyphstones required to trigger the wizard fight
    """
    display_name = "Wizard Glyphstones"
    range_start = 0
    range_end = 3
    default = 3

class WraithRequirements(Choice):
    """
    Determines requirements to enter the Wraith boss room.
    None: Boss room can be entered without any additional items
    Vanilla: Boss room requires 15 silver shards
    Intended: Boss room requires 15 silver shards and 3 glyphstones
    Silver Shards: Boss room requires a configurable number of silver shards
    Gold Shards: Boss room requires a configurable number of gold shards
    Smile Tokens: Boss room requires a configurable number of smile tokens
    Rune Cubes: Boss room requires a configurable number of rune cubes
    Glyphstones: Boss room requires a configurable number of glyphstones
    """
    display_name = "Wraith Requirements"
    option_none = 1
    option_vanilla = 2
    option_intended = 3
    option_silver_shards = 2
    option_gold_shards = 3
    option_smile_tokens = 4
    option_rune_cubes = 5
    option_glyphstones = 6

class WraithSilverCount(Range):
    """
    The number of silver shards required to enter the wraith boss room.
    """
    display_name = "Wraith Silver Shards"
    range_start = 1
    range_end = 15
    default = 15

class WraithGoldCount(Range):
    """
    The number of gold shards required to enter the wraith boss room.
    """
    display_name = "Wraith Gold Shards"
    range_start = 1
    range_end = 3
    default = 3

class WraithSmileCount(Range):
    """
    The number of smile tokens required to enter the wraith boss room.
    """
    display_name = "Wraith Smile Tokens"
    range_start = 1
    range_end = 10
    default = 10

class WraithRuneCount(Range):
    """
    The number of rune cubes required to enter the wraith boss room.
    """
    display_name = "Wraith Rune Cubes"
    range_start = 1
    range_end = 3
    default = 3

class WraithGlyphstoneCount(Range):
    """
    The number of glyphstones required to enter the wraith boss room.
    """
    display_name = "Wraith Glyphstones"
    range_start = 1
    range_end = 3
    default = 3



@dataclass
class GlyphsOptions(PerGameCommonOptions):
    # Game Options
    Goal:                   Goal
    StartingSword:          StartingSword
    GenericParries:         GenericParries
    Multiplayer:            Multiplayer

    # Randomization Options
    LocationPool:           LocationPool
    HatLocations:           HatLocations
    Shopsanity:             Shopsanity
    RandomShopPrices:       RandomShopPrices
    EnableTraps:            EnableTraps
    TrapTypes:              TrapTypes
    UnreasonableLocatons:   UnreasonableLocations

    # Logical Options
    SwordlessCombat:        SwordlessCombat
    BulletCombat:           BulletCombat
    DashPuzzlesSolved:      DashPuzzlesSolved
    LocicalWallJumps:       LocicalWallJumps
    LogicalWallJumpChains:  LogicalWallJumpChains

    # Open Settings
    WizardRequirements:     WizardRequirements
    WraithRequirements:     WraithRequirements
    WraithSilverCount:      WraithSilverCount
    WraithGoldCount:        WraithGoldCount
    WraithSmileCount:       WraithSmileCount
    WraithRuneCount:        WraithRuneCount
    WraithGlyphstoneCount:  WraithGlyphstoneCount

# This is where you organize your options
# Its entirely up to you how you want to organize it
glyphs_option_groups: Dict[str, List[Any]] = {
    "Game Options": [Goal, StartingSword, GenericParries, Multiplayer],
    "Randomization Options": [LocationPool, HatLocations, Shopsanity, RandomShopPrices, EnableTraps, TrapTypes, UnreasonableLocations],
    "Logical Options": [SwordlessCombat, BulletCombat, DashPuzzlesSolved, LocicalWallJumps, LogicalWallJumpChains],
    "Open Settings": [WizardRequirements, WraithRequirements, WraithSilverCount, WraithGoldCount, WraithSmileCount, WraithRuneCount, WraithGlyphstoneCount],
}