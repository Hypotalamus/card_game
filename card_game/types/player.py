import random
from uuid import UUID

from card_game.types.system import System
from card_game.types.market import Market
from card_game.types.misc_types import Action, PlayerCoeffs
from card_game.model.params import ACTIONS_COUNT


class PlayerCardBalance():

    def __init__(self, gold_a_cur, gold_a_prev, gold_n_cur, gold_n_prev, ordinary):
        self.gold_a_cur: int = gold_a_cur
        self.gold_a_prev: int = gold_a_prev
        self.gold_n_cur: int = gold_n_cur
        self.gold_n_prev: int = gold_n_prev
        self.ordinary: int = ordinary

INITIAL_CARD_BALANCE = (0, 0, 0, 0, 0)

make_zero_threshold = lambda x: x if x > 0 else 0

class Player:
    def __init__(self, uuid, coeffs):
        self.uuid = uuid
        self.coeffs: PlayerCoeffs = coeffs
        self.card_balance: PlayerCardBalance = PlayerCardBalance(*INITIAL_CARD_BALANCE)
        self.win_streak: int = 0
        self.loss_streak: int = 0
        self.spent_usd: float = 0.0
        self.earned_usd: float = 0.0
        self.g_cards_a_cur_won: int = 0
        self.steps_passed: int = 0
        self.g_cards_a_cur_won_avg: float = 0.15 # May be different for different players?

    def choose_action(
            self, system: System, market: Market, top_5: dict[UUID, int],
            collusion_enabled: bool, market_enabled: bool) -> Action:
        g_card_per_ordinary = system.params.g_card_per_ordinary
        g_cards_cur_per_prev = system.params.g_cards_cur_per_prev
        cards_from_box_min = system.params.cards_from_box_min
        cards_from_box_max = system.params.cards_from_box_max
        box_price_usd = system.params.box_price_usd        
        card_game_price = 2 * box_price_usd / (cards_from_box_min + cards_from_box_max)
        card_market_price = market.get_card_price()
        g_card_game_price = system.params.g_card_price_usd
        g_card_market_price = market.get_g_card_price()
        golden_set = system.params.golden_set

        gold_a_cur = self.card_balance.gold_a_cur
        gold_a_prev = self.card_balance.gold_a_prev
        gold_n_cur = self.card_balance.gold_n_cur
        gold_n_prev = self.card_balance.gold_n_prev
        ordinary = self.card_balance.ordinary        
        # Special case: player can get jackpot
        if gold_a_cur >= golden_set:
            action = Action.GET_JACKPOT
            return action
        
        # Calculate weights
        weights = ACTIONS_COUNT * [0]
        # w1 - LEAVE_GAME
        c0, c1, c2 = self.coeffs.leave_game
        interim = self.spent_usd - self.earned_usd
        interim = self.loss_streak**2 - self.win_streak**2 + c2 * interim
        interim = make_zero_threshold(interim)
        weights[0] = c0 + c1 * interim
        # w2 - SELL_GOLDEN_CARD_TO_GAME
        c0, c1 = self.coeffs.sell_g_card_to_game
        predicat = int(gold_a_prev + gold_n_cur + gold_n_prev > 0)
        interim = self.spent_usd - self.earned_usd
        interim = make_zero_threshold(interim)
        weights[1] = predicat * (c0 + c1 * interim)
        # w3 - BUY_BOX
        c0 = self.coeffs.buy_box
        weights[2] = c0
        # w4 - PLAY_IN_GOLDEN_LEAGUE
        c0 = self.coeffs.play_in_g_league
        predicat = int(gold_a_prev + gold_n_cur + gold_n_prev > 0)
        weights[3] = predicat * c0
        # w5 - PLAY_IN_COMMON_LEAGUE
        c0 = self.coeffs.play_in_league
        predicat = int(ordinary > 0) 
        weights[4] = predicat * c0
        # w6 - BUY_GOLDEN_CARD_FROM_GAME
        c0 = self.coeffs.buy_g_card_from_game
        weights[5] = c0
        # w7 - CHANGE_CARDS_TO_GOLDEN
        c0, c1 = self.coeffs.change_cards_to_golden
        predicat = int(ordinary >= g_card_per_ordinary)
        weights[6] = predicat * (c0 + c1 * (ordinary - g_card_per_ordinary))
        # w8 - CONVERT_PAST_GOLDEN_CARDS_TO_CURRENT
        c0, c1 = self.coeffs.convert_g_cards_to_cur
        predicat = int(gold_a_prev + gold_n_prev >= g_cards_cur_per_prev)
        weights[7] = predicat * (c0 + c1 * (gold_a_prev + gold_n_prev - g_cards_cur_per_prev))
        # w9 - EXCHANGE_GOLDEN_CARD_TO_BOXES
        c0, c1 = self.coeffs.exchange_g_card_to_boxes
        predicat = int(gold_a_prev + gold_n_cur + gold_n_prev > 0)
        interim = card_market_price - card_game_price
        interim = make_zero_threshold(interim)
        weights[8] = predicat * (c0 + c1 * interim)        
        if market_enabled:
            # w10 - BUY_GOLDEN_CARD_FROM_MARKET
            c0 = self.coeffs.buy_g_card_from_market
            delta_x = golden_set - gold_a_cur
            steps_until_season_end = system.steps_until_season_end
            delta_x_bar = self.estimate_g_cards_won_in_this_season(steps_until_season_end)
            interim = delta_x - delta_x_bar
            interim = make_zero_threshold(interim) 
            weights[9] = c0 * interim
            # w11 - BUY_CARD_FROM_MARKET
            c0, c1 = self.coeffs.buy_card_from_market
            interim = card_game_price - card_market_price
            weights[10] = make_zero_threshold(c0 + c1 * interim)
            # w12 - SELL_GOLDEN_CARD_TO_MARKET
            c0 = self.coeffs.sell_g_card_to_market
            predicat = int(gold_a_cur > 0)
            interim = g_card_market_price - g_card_game_price
            interim = make_zero_threshold(interim)
            weights[11] = predicat * c0 * interim
            # w13 - SELL_CARD_TO_MARKET
            c0, c1 = self.coeffs.sell_card_to_market
            predicat = int(ordinary > 0)
            interim = card_market_price - card_game_price
            weights[12] = predicat * make_zero_threshold(c0 + c1 * interim)
        # w14 - TRY_COLLUSION
        if collusion_enabled:
            c0 = self.coeffs.try_collusion
            predicat = self.collusion_available(top_5, golden_set)
            weights[13] = predicat * c0

        # Choose action
        actions_list = list(range(1, ACTIONS_COUNT + 1))
        choosen = random.choices(actions_list, weights)
        action = Action(choosen[0])
        return action
    
    def estimate_g_cards_won_in_this_season(self, steps_until_season_end) -> int:
        if self.steps_passed > 20:
            alpha = 0.95
            g_cards_a_cur_won_avg_new = self.g_cards_a_cur_won / self.steps_passed
            self.g_cards_a_cur_won_avg = self.g_cards_a_cur_won_avg * alpha + \
                g_cards_a_cur_won_avg_new * (1 - alpha)
            
        estimate = int(self.g_cards_a_cur_won_avg * steps_until_season_end)
        return estimate
    
    def collusion_available(self, top_5, golden_set) -> bool:
        uuids, g_cards_sum = top_5
        return self.uuid in uuids and g_cards_sum >= golden_set       