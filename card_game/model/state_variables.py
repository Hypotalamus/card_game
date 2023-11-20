from cadCAD_tools.types import InitialValue
from cadCAD_tools.preparation import prepare_state
from uuid import UUID

from card_game.types.player import Player
from card_game.types.system import System
from card_game.types.market import Market
from card_game.types.misc_types import Action 

raw_state_variables: dict[str, InitialValue] = {
    'players': InitialValue({}, dict[UUID, Player]),
    'actions': InitialValue([], list[tuple[UUID, Action]]),
    'system': InitialValue(None, System),
    'market': InitialValue(None, Market),
    'day': InitialValue(1, int),
    'season': InitialValue(1, int),
    'new_day_has_begun': InitialValue(True, bool),
    'new_season_has_begun': InitialValue(True, bool),

    # Metrics
    'collusions_num': InitialValue(0, int),
    'jackpots_num': InitialValue(0, int),
    'players_num': InitialValue(0, int),
    'treasure': InitialValue(0, float),
    'g_card_marketprice': InitialValue(25.0, float),
    'card_marketprice': InitialValue(20/7, float),
    'sell_g_orders_num': InitialValue(0, int),
    'buy_g_orders_num': InitialValue(0, int),
    'sell_orders_num': InitialValue(0, int),
    'buy_orders_num': InitialValue(0, int),
    'g_cards_max_per_player': InitialValue(0, int)
}

state_variables = prepare_state(raw_state_variables)