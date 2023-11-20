from enum import Enum
from dataclasses import dataclass

Percentage = float

class Action(Enum):
    LEAVE_GAME = 1
    SELL_GOLDEN_CARD_TO_GAME = 2
    BUY_BOX = 3
    PLAY_IN_GOLDEN_LEAGUE = 4
    PLAY_IN_COMMON_LEAGUE = 5
    BUY_GOLDEN_CARD_FROM_GAME = 6
    CHANGE_CARDS_TO_GOLDEN = 7
    CONVERT_PAST_GOLDEN_CARDS_TO_CURRENT = 8
    EXCHANGE_GOLDEN_CARD_TO_BOXES = 9
    BUY_GOLDEN_CARD_FROM_MARKET = 10
    BUY_CARD_FROM_MARKET = 11
    SELL_GOLDEN_CARD_TO_MARKET = 12
    SELL_CARD_TO_MARKET = 13
    TRY_COLLUSION = 14
    GET_JACKPOT = 15

class GoldenCard(Enum):
    active_cur = 1
    active_prev = 2
    inactive_cur = 3
    inactive_prev = 4

@dataclass(frozen=True)
class SystemParams:
    cards_from_box_min: int
    cards_from_box_max: int
    golden_set: int
    g_card_per_ordinary: int
    g_cards_cur_per_prev: int
    boxes_per_g_card: int
    box_price_usd: float
    g_card_price_usd: float
    jackpot: float

@dataclass(frozen=True)
class MarketParams:
    init_g_card_price: float
    init_card_price: float
    Kp_g: float # Coefficient of proportional branch of PI controller for golden cards price
    Ki_g: float # Coefficient of integral branch of PI controller for golden cards price
    Kp_o: float # Coefficient of proportional branch of PI controller for ordinary cards price
    Ki_o: float # Coefficient of integral branch of PI controller for ordinary cards price
    system_fee: float
    anti_windup: bool
    g_integral_limits: tuple[float, float] # (min, max) if anti windup enabled 
    integral_limits: tuple[float, float] # (min, max) if anti windup enabled
    g_limits: tuple[float, float] # (min, max) limit on price 
    limits: tuple[float, float] # (min, max) limit on price 

@dataclass(frozen=True)
class PlayerCoeffs():
    leave_game: tuple[float, float, float]
    sell_g_card_to_game: tuple[float, float]
    buy_box: float
    play_in_g_league: float
    play_in_league: float
    buy_g_card_from_game: float
    change_cards_to_golden: tuple[float, float]
    convert_g_cards_to_cur: tuple[float, float]
    exchange_g_card_to_boxes: tuple[float, float]
    buy_g_card_from_market: float
    buy_card_from_market: tuple[float, float] 
    sell_g_card_to_market: float
    sell_card_to_market: tuple[float, float]
    try_collusion: float