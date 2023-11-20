from typing import Union
from cadCAD_tools.types import Param, ParamSweep
from cadCAD_tools.preparation import prepare_params

from card_game.types.misc_types import Percentage, SystemParams, MarketParams, PlayerCoeffs
from card_game.types.player import PlayerCoeffs

DAYS_PER_MONTH: int = 30
ACTIONS_COUNT: int = 15
PLAYERS_PER_GAME: int = 3

DEFAULT_SYSTEM_PARAMS = SystemParams(
    cards_from_box_min=2,
    cards_from_box_max=5,
    golden_set=100,
    g_card_per_ordinary=10,
    g_cards_cur_per_prev=2,
    boxes_per_g_card=3,
    box_price_usd=10.0,
    g_card_price_usd=25.0,
    jackpot = 5000.0   
)

DEFAULT_MARKET_PARAMS = MarketParams(
    init_g_card_price=25.0,
    init_card_price=20/7,
    Kp_g=1e-3,
    Ki_g=1e-4,
    Kp_o=1e-4,
    Ki_o=1e-5,
    system_fee=0.1,
    anti_windup=True,
    g_integral_limits=(-20.0, 50.0),
    integral_limits=(-2.0, 5.0),
    g_limits=(0.1, None),
    limits=(0.1, None)
)

DEFAULT_PLAYER_COEFFS = PlayerCoeffs(
    leave_game=(0.1, 0.01, 0.05),
    sell_g_card_to_game=(3.0, 0.0),
    buy_box=3.0,
    play_in_g_league=200.0,
    play_in_league=25.0,
    buy_g_card_from_game=1.0,
    change_cards_to_golden=(100.0, 10.0),
    convert_g_cards_to_cur=(100.0, 10.0),
    exchange_g_card_to_boxes=(5.0, 0.0),
    buy_g_card_from_market=0.05,
    buy_card_from_market=(0.05, 0.2),
    sell_g_card_to_market=5.0,
    sell_card_to_market=(10.0, 5.0),
    try_collusion=2000.0   
)


params: dict[str, Union[Param, ParamSweep]] = {
    'to_payable_conversion_factor': Param(2, Percentage),
    'player_coeffs': Param(DEFAULT_PLAYER_COEFFS, PlayerCoeffs),
    'steps_per_day': Param(30, int),
    'days_per_season': Param(30, int),
    'system_params': Param(DEFAULT_SYSTEM_PARAMS, SystemParams),
    'market_params': Param(DEFAULT_MARKET_PARAMS, MarketParams),
    'betatest_enabled': Param(True, bool),
    'betatest_limit': Param(1500, int),
    'collusion_enabled': Param(True, bool),
    'market_enabled': Param(True, bool),
}

params = prepare_params(params)
