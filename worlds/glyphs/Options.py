from typing import List, Dict, Any
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Choice, DeathLink, OptionGroup, OptionSet, Toggle, Range

def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in glyphs_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list



# Game Options
class Goal(Choice):
    """
    Determines what ending must be reached for Archipelago to consider your game as complete.
    Note: This option does not affect location/item pools so you still may have to complete more of the game than you would think.
    """
    display_name = "Completion Requirements"
    option_false_ending = 1
    option_good_ending = 2
    option_true_ending = 3
    option_all_star_endings = 4
    option_epilogue = 5
    option_all_endings = 6
    default = option_true_ending

class StartingSword(Toggle):
    """
    Start the game with the sword.
    """
    display_name = "Starting Sword"
    default = False

class StartingDash(Toggle):
    """
    Start the game with dash unlocked.
    """
    display_name = "Starting Dash"
    default = False

## Cool idea but practically not great
# class GenericParries(Toggle):
#     """
#     Allows normal damaging bullets to be parried.
#     Parried bullets are 3x more powerful and move faster than normal.
#     """
#     display_name = "Generic Parries"
#     default = False

## Still coming soon. Just disabled since it isn't implemented yet
# class Multiplayer(Toggle):
#     """
#     Enables multiplayer with other glyphs players in the multiworld that have this option enabled
#     """
#     display_name = "Multiplayer"
#     default = False



# Randomization Options
## To be implemented when save button randomization is implemented
# class RandomizeWorldSpawn(Toggle):
#     """
#     Shuffles what save button you start on.
#     If false, you will start at the standard spawn point.
#     """
#     display_name = "Randomize World Spawn"

## Ending selection should already filter down locations its self
# class LocationPool(Choice):
#     """
#     Determines what locations will be shuffled in the world.
#     False Ending: Includes all locations relevent to the false ending
#     Good Ending: Includes all locations relevent to the good ending
#     Full Tomb: Like Good Ending but includes the between and master puzzles in the pool
#     Outer Void: Includes Full Tomb and Outer Void locations
#     """
#     display_name = "Location Pool"
#     option_false_ending = 1
#     option_good_ending = 2
#     option_full_tomb = 3
#     option_outer_void = 4
#     default = option_false_ending

# class HatLocations(Toggle):
#     """
#     Adds hat puzzles to the location pool.
#     If false, all hat puzzles will yield junk items.
#     """
#     display_name = "Include Hat Puzzles"

# class Shopsanity(Toggle):
#     """
#     Shuffles smile shop items into the pool.
#     Also removes the refund button (spend wisely).
#     """
#     display_name = "Shopsanity"

class RandomShopPrices(Toggle):
    """
    Randomizes the prices of shop items.
    Never exceeds 10 total.
    """
    display_name = "Randomize Shop Prices"
    default = True

class RandomButtonColorPercent(Range):
    """
    Percent of buttons to randomize the color of.
    IMPORTANT:
    This option is known to cause issues with the universal tracker.
    By enabling it, you accept that it will not be fully reliable.
    """
    display_name = "Random Button Colors Percent"
    range_start = 0
    range_end = 100
    default = 0

class ExcludeBlack(Toggle):
    """
    Ensures no buttons are randomized to black.
    """
    display_name = "No Black Buttons"
    default = False

class EnableTraps(Toggle):
    """
    Adds traps to the itempool
    """
    display_name = "Enable Traps"
    default = True

class TrapTypes(OptionSet):
    """
    Determines what kinds of traps will be added to the item pool
    Valid Keys:
    Momentum Trap: Launches the player at a random angle
    John Trap: Spawns John for 1 minute
    Slow Trap: Slows the player down for a short period of time
    Screen Flip Trap: Flips the player's screen for a short period of time
    Dash Trap: Slows the player's dash for a short period of time
    """
    display_name = "Trap Types"
    valid_keys = {
        "Momentum Trap",
        "John Trap",
        "Slow Trap",
        "Screen Flip Trap",
        "Dash Trap",
    }
    default = {
        "Momentum Trap",
        "John Trap",
        "Slow Trap",
        "Screen Flip Trap",
        "Dash Trap",
    }

class HatShuffle(Toggle):
    """
    Include hats in the item pool
    If enabled, hats will replace some junk items and traps
    If disabled, all hats will be included in starting inventory
    """
    display_name = "Shuffle Hats"
    default = True



# Logical Options
class SwordlessCombat(Toggle):
    """
    Swordless combat is considered in logic.
    Ex: Fighting with only dash attacks
    """
    display_name = "Swordless Combat"
    default = False

## Doesnt actually seem very practical/fun
# class BulletCombat(Toggle):
#     """
#     Considers defeating bosses with only parried projectiles in logic.
#     Does nothing if Swordless Combat is not enabled.
#     If Generic Parries is enabled, also includes relevant bosses.
#     """
#     display_name = "Parry Combat"
#     default = False

class DashPuzzlesSolved(Toggle):
    """
    Logic assumes you already have the answer to all the puzzles in the game written down somewhere.
    """
    display_name = "Assume Puzzles Solved"
    default = False

## Actually might be alot harder to implement than I thought
# class MultiplayerCheese(Toggle):
#     """
#     Considers skips made possible by multiplayer in logic.
#     Does nothing if multiplayer is not enabled or if there are no other players to connect to.
#     """
#     display_name = "Multiplayer Cheeses in Logic"

class LogicalWallJumps(Toggle):
    """
    Considers skips utilizing wall jumps in logic.
    """
    display_name = "Wall Jumps in Logic"
    default = False

## Logically will never be needed
# class LogicalWallJumpChains(Toggle):
#    """
#    Considers skips that require multiple consecutive wall jumps (2-3) in logic.
#    Does nothing if "Wall Jumps in Logic" is not enabled.
#    """
#    display_name = "Wall Jump Chains in Logic"

class FlowerPuzzleSkips(Toggle):
    """
    Considers skips utilizing the flower puzzle in logic.
    """
    display_name = "Flower Puzzle in Logic"
    default = False



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
    option_none = 0
    option_vanilla = 1
    option_intended = 2
    option_silver_shards = 3
    option_gold_shards = 4
    option_smile_tokens = 5
    option_rune_cubes = 6
    option_glyphstones = 7
    default = option_none

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
    Goal:                       Goal
    StartingSword:              StartingSword
    StartingDash:               StartingDash
  # GenericParries:             GenericParries
  # Multiplayer:                Multiplayer
    DeathLink:                  DeathLink

    # Randomization Options
  # LocationPool:               LocationPool
  # HatLocations:               HatLocations
  # Shopsanity:                 Shopsanity
    RandomShopPrices:           RandomShopPrices
    RandomButtonColorPercent:   RandomButtonColorPercent
    ExcludeBlack:               ExcludeBlack
    EnableTraps:                EnableTraps
    TrapTypes:                  TrapTypes
    HatShuffle:                 HatShuffle

    # Logical Options
    SwordlessCombat:            SwordlessCombat
  # BulletCombat:               BulletCombat
    DashPuzzlesSolved:          DashPuzzlesSolved
    LogicalWallJumps:           LogicalWallJumps
  # LogicalWallJumpChains:      LogicalWallJumpChains
    FlowerPuzzleSkips:          FlowerPuzzleSkips

    # Open Settings
    WizardRequirements:         WizardRequirements
    WraithRequirements:         WraithRequirements
    WraithSilverCount:          WraithSilverCount
    WraithGoldCount:            WraithGoldCount
    WraithSmileCount:           WraithSmileCount
    WraithRuneCount:            WraithRuneCount
    WraithGlyphstoneCount:      WraithGlyphstoneCount

glyphs_option_groups: Dict[str, List[Any]] = {
    "Game Options": [Goal, StartingSword, StartingDash, DeathLink],
    "Randomization Options": [RandomShopPrices, RandomButtonColorPercent, ExcludeBlack, EnableTraps, TrapTypes, HatShuffle],
    "Logical Options": [SwordlessCombat, DashPuzzlesSolved, LogicalWallJumps, FlowerPuzzleSkips],
    "Open Settings": [WizardRequirements, WraithRequirements, WraithSilverCount, WraithGoldCount, WraithSmileCount, WraithRuneCount, WraithGlyphstoneCount],
}