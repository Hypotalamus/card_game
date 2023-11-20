from card_game.types.misc_types import MarketParams

class Market:

    def __init__(self, params: MarketParams):
        self.g_card_price = params.init_g_card_price
        self.card_price = params.init_card_price
        self.params = params
        self.sell_g_cards_book = []
        self.buy_g_cards_book = []
        self.sell_cards_book = []
        self.buy_cards_book = []
        self.integral_g: float = 0
        self.sat_g: int = 0
        self.integral_o: float = 0
        self.sat_o: int = 0

    def get_card_price(self):
        return self.card_price
    
    def get_g_card_price(self):
        return self.g_card_price
    
    def cancel_bids(self, uuid, players):
        player = players[uuid]
        g_buy_inds = [ind for ind, el in enumerate(self.buy_g_cards_book) if el == player]
        while len(g_buy_inds) > 0:
            ind = g_buy_inds.pop()
            self.buy_g_cards_book.pop(ind)

        buy_inds = [ind for ind, el in enumerate(self.buy_cards_book) if el == player]
        while len(buy_inds) > 0:
            ind = buy_inds.pop()
            self.buy_cards_book.pop(ind)

        g_sell_inds = [ind for ind, el in enumerate(self.sell_g_cards_book) if el == player]
        while len(g_sell_inds) > 0:
            ind = g_sell_inds.pop()
            self.sell_g_cards_book.pop(ind)
            player.card_balance.gold_a_cur += 1

        sell_inds = [ind for ind, el in enumerate(self.sell_cards_book) if el == player]
        while len(sell_inds)  > 0:
            ind = sell_inds.pop()
            self.sell_cards_book.pop(ind)
            player.card_balance.ordinary += 1


    def send_golden_card_purchase_bid(self, uuid, players):
        player = players[uuid]
        self.buy_g_cards_book.append(player)

    def send_card_purchase_bid(self, uuid, players):
        player = players[uuid]
        self.buy_cards_book.append(player)

    def send_golden_card_sale_bid(self, uuid, players):
        player = players[uuid]
        assert player.card_balance.gold_a_cur > 0, "Player has not golden card for market!"
        player.card_balance.gold_a_cur -= 1
        self.sell_g_cards_book.append(player)

    def send_card_sale_bid(self, uuid, players):
        player = players[uuid]
        assert player.card_balance.ordinary > 0, "Player has not ordinary card for market!"
        player.card_balance.ordinary -= 1
        self.sell_cards_book.append(player)

    def process_bids(self, system):
        g_card_price = self.get_g_card_price()
        card_price = self.get_card_price()
        fee = self.params.system_fee
        g_card_seller_check = (1 - fee) * g_card_price
        g_card_system_check = fee * g_card_price
        card_seller_check = (1 - fee) * card_price
        card_system_check = fee * card_price

        while len(self.sell_g_cards_book) > 0 and len(self.buy_g_cards_book) > 0:
            seller = self.sell_g_cards_book.pop(0)
            buyer = self.buy_g_cards_book.pop(0)
            seller.earned_usd += g_card_seller_check
            buyer.spent_usd += g_card_price
            system.treasure += g_card_system_check
            buyer.card_balance.gold_a_cur += 1

        while len(self.sell_cards_book) > 0 and len(self.buy_cards_book) > 0:
            seller = self.sell_cards_book.pop(0)
            buyer = self.buy_cards_book.pop(0)
            seller.earned_usd += card_seller_check
            buyer.spent_usd += card_price
            system.treasure += card_system_check
            buyer.card_balance.ordinary += 1

    def _satlimit(self, isGolden: bool) -> None:
        if isGolden:
            min_val, max_val = self.params.g_integral_limits
            self.sat_g = 0
            if max_val is not None:
                self.sat_g = 1 if self.integral_g > max_val else self.sat_g
                self.integral_g = min(max_val, self.integral_g)
            if min_val is not None:
                self.sat_g = -1 if self.integral_g < min_val else self.sat_g
                self.integral_g = max(min_val, self.integral_g)
        else:
            min_val, max_val = self.params.integral_limits
            self.sat_o = 0
            if max_val is not None:
                self.sat_o = 1 if self.integral_o > max_val else self.sat_o
                self.integral_o = min(max_val, self.integral_o)
            if min_val is not None:
                self.sat_o = -1 if self.integral_o < min_val else self.sat_o
                self.integral_o = max(min_val, self.integral_o)

    def _limit(self, isGolden: bool) -> None:
        if isGolden:
            min_val, max_val = self.params.g_limits
            if max_val is not None:
                self.g_card_price = min(max_val, self.g_card_price)
            if min_val is not None:
                self.g_card_price = max(min_val, self.g_card_price)
        else:
            min_val, max_val = self.params.limits
            if max_val is not None:
                self.card_price = min(max_val, self.card_price)
            if min_val is not None:
                self.card_price = max(min_val, self.card_price)                         

    def update_prices(self):
        err = len(self.buy_g_cards_book) - len(self.sell_g_cards_book)
        Kp = self.params.Kp_g
        Ki = self.params.Ki_g
        if self.params.anti_windup:
            windup_neg = self.sat_g < 0 and err < 0
            windup_pos = self.sat_g > 0 and err > 0
            if not windup_neg and not windup_pos:
                self.integral_g += Ki * err
            self._satlimit(isGolden=True)
        else:
           self.integral_g += Ki * err

        target_price = self.params.init_g_card_price

        self.g_card_price = target_price + Kp * err + self.integral_g
        self._limit(isGolden=True)

        err = len(self.buy_cards_book) - len(self.sell_cards_book)
        Kp = self.params.Kp_o
        Ki = self.params.Ki_o
        if self.params.anti_windup:
            windup_neg = self.sat_o < 0 and err < 0
            windup_pos = self.sat_o > 0 and err > 0
            if not windup_neg and not windup_pos:
                self.integral_o += Ki * err
            self._satlimit(isGolden=False)            
        else:
           self.integral_o += Ki * err

        target_price = self.params.init_card_price

        self.card_price = target_price + Kp * err + self.integral_o
        self._limit(isGolden=False)