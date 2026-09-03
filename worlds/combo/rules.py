from typing import TYPE_CHECKING, Callable

from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import ComboWorld

def set_completion_rule(world: "ComboWorld") -> None:
    options = world.options
    player = world.player
    state = CollectionState(world.multiworld)

    # Glyphs Victory Condition
    g_victory: Callable[[CollectionState], bool] = lambda state: False
    if options.Goal.value == options.Goal.option_false_ending:
        g_victory = lambda state: state.has("False Ending", player)
    elif options.Goal.value == options.Goal.option_good_ending:
        g_victory = lambda state: state.has("Good Ending", player)
    elif options.Goal.value == options.Goal.option_true_ending:
        g_victory = lambda state: state.has("True Ending", player)
    elif options.Goal.value == options.Goal.option_all_star_endings:
        g_victory = lambda state: state.has("Perfect Clarity", player) and state.has("Smilemask Ending", player) and state.has("Omnipotence Ending", player)
    elif options.Goal.value == options.Goal.option_epilogue:
        g_victory = lambda state: state.has("Epilogue Ending", player)
    elif options.Goal.value == options.Goal.option_all_endings:
        g_victory = lambda state: state.has("False Ending", player) and state.has("Good Ending", player) and state.has("True Ending", player) and state.has("Perfect Clarity", player) and state.has("Smilemask Ending", player) and state.has("Omnipotence Ending", player) and state.has("Epilogue Ending", player)

    # APQuest Victory Condition
    a_victory = lambda state: state.has("Victory", world.player)

    world.multiworld.completion_condition[player] = lambda state: g_victory(state) and a_victory(state)