import random

from card_game.types.misc_types import SystemParams, GoldenCard

class System:

    def __init__(self, params: SystemParams, steps_per_season: int):
        self.params = params
        self.treasure: float = 0
        self.steps_until_season_end: int = steps_per_season

    def open_box(self, player) -> None:
        cards_from_box_min = self.params.cards_from_box_min
        cards_from_box_max = self.params.cards_from_box_max
        new_cards = random.randint(cards_from_box_min, cards_from_box_max)
        player.card_balance.ordinary += new_cards

    def play_round_in_golden_league(self, uuids, players):
        # Define players' order 
        random.shuffle(uuids)
        players_num = len(uuids)
        # Seize some golden cards
        cards_at_stake = []
        won_something = dict()   
        for uuid in uuids:
            won_something[uuid] = False
            player = players[uuid]
            choice = self._choose_golden_card(player)
            assert choice is not None, "Player plays in golden league, but hasn't golden cards!"

            if choice == GoldenCard.active_prev:
                player.card_balance.gold_a_prev -= 1
                cards_at_stake.append(GoldenCard.active_prev)
            elif choice == GoldenCard.inactive_cur:
                player.card_balance.gold_n_cur -= 1
                cards_at_stake.append(GoldenCard.active_cur)
            elif choice == GoldenCard.inactive_prev:
                player.card_balance.gold_n_prev -= 1
                cards_at_stake.append(GoldenCard.active_prev)

        player_ind = 0
        win_streak = 0
        cards_won = []
        random.shuffle(cards_at_stake)
        while len(cards_at_stake) > 0:
            res = random.randint(0, 1)
            if res:
                card = cards_at_stake.pop()
                cards_won.append(card)
                win_streak += 1
                uuid = uuids[player_ind]
                won_something[uuid] = True

                if len(cards_at_stake) == 0:
                    player = players[uuid]
                    if win_streak == players_num: # Strike!!!
                        player.card_balance.gold_a_cur += players_num
                        player.g_cards_a_cur_won += players_num
                    else:
                        for card in cards_won:
                            if card == GoldenCard.active_cur:
                                player.card_balance.gold_a_cur += 1
                                player.g_cards_a_cur_won += 1
                            elif card == GoldenCard.active_prev:
                                player.card_balance.gold_a_prev += 1
            else:
                if win_streak > 0:
                    uuid = uuids[player_ind]
                    player = players[uuid]
                    for card in cards_won:
                        if card == GoldenCard.active_cur:
                            player.card_balance.gold_a_cur += 1
                            player.g_cards_a_cur_won += 1
                        elif card == GoldenCard.active_prev:
                            player.card_balance.gold_a_prev += 1

                cards_won = []
                win_streak = 0
                player_ind += 1
                player_ind %= players_num
        
        for uuid, won in won_something.items():
            player = players[uuid]
            if won:
                player.win_streak += 1
                player.loss_streak = 0
            else:
                player.win_streak = 0
                player.loss_streak += 1

    def play_round_in_ordinary_league(self, uuids, players) -> None:
        # Define players' order 
        random.shuffle(uuids)
        players_num = len(uuids)
        won_something = dict()
        # Seize ordinary cards
        for uuid in uuids:
            won_something[uuid] = False
            player = players[uuid]
            assert player.card_balance.ordinary > 0, "Player plays without ordinary cards!"
            player.card_balance.ordinary -= 1

        cards_at_stake_num = players_num
        player_ind = 0
        win_streak = 0
        while cards_at_stake_num > 0:
            res = random.randint(0, 1)
            if res:
                cards_at_stake_num -= 1
                win_streak += 1
                uuid = uuids[player_ind]
                won_something[uuid] = True

                if cards_at_stake_num == 0:
                    player = players[uuid]
                    player.card_balance.ordinary += win_streak
            else:
                if win_streak > 0:
                    uuid = uuids[player_ind]
                    player = players[uuid]
                    player.card_balance.ordinary += win_streak

                win_streak = 0
                player_ind += 1
                player_ind %= players_num

        for uuid, won in won_something.items():
            player = players[uuid]
            if won:
                player.win_streak += 1
                player.loss_streak = 0
            else:
                player.win_streak = 0
                player.loss_streak += 1

    def buy_all_golden_cards(self, uuid, players):
        player = players[uuid]
        g_card_cost = self.params.g_card_price_usd
        g_cards_num = player.card_balance.gold_a_cur + player.card_balance.gold_a_prev + \
            player.card_balance.gold_n_cur + player.card_balance.gold_n_prev
        cashflow = g_cards_num * g_card_cost
        self.treasure -= cashflow
        player.earned_usd += cashflow
        player.card_balance.gold_a_cur = 0
        player.card_balance.gold_a_prev = 0
        player.card_balance.gold_n_cur = 0
        player.card_balance.gold_n_prev = 0

    def buy_golden_card(self, uuid, players):
        player = players[uuid]
        choice = self._choose_golden_card(player)
        assert choice is not None, "Player sells golden cards, but he has no one!"

        if choice == GoldenCard.active_prev:
            player.card_balance.gold_a_prev -= 1
        elif choice == GoldenCard.inactive_cur:
            player.card_balance.gold_n_cur -= 1
        elif choice == GoldenCard.inactive_prev:
            player.card_balance.gold_n_prev -= 1

        player.earned_usd += self.params.g_card_price_usd
        self.treasure -= self.params.g_card_price_usd

    def sell_box(self, uuid, players):
        player = players[uuid]
        player.spent_usd += self.params.box_price_usd
        self.treasure += self.params.box_price_usd
        self.open_box(player)

    def sell_golden_card(self, uuid, players):
        player = players[uuid]
        player.spent_usd += self.params.g_card_price_usd
        self.treasure += self.params.g_card_price_usd
        player.card_balance.gold_n_cur += 1

    def change_cards_to_golden(self, uuid, players):
        player = players[uuid]
        player.card_balance.ordinary -= self.params.g_card_per_ordinary
        player.card_balance.gold_n_cur += 1

    def convert_past_golden_cards_to_current(self, uuid, players):
        player = players[uuid]
        for _ in range(self.params.g_cards_cur_per_prev):
            choice = self._choose_golden_card(player, prev_only=True)
            assert choice is not None, "Player wants to convert golden cards, but he hasn't enough!"
            if choice == GoldenCard.active_prev:
                player.card_balance.gold_a_prev -= 1
            elif choice == GoldenCard.inactive_prev:
                player.card_balance.gold_n_prev -= 1

        player.card_balance.gold_n_cur += 1

    def exchange_golden_card_to_boxes(self, uuid, players):
        player = players[uuid]
        choice = self._choose_golden_card(player)
        assert choice is not None, "Player wants to exchange golden card to boxes, but he has no one!"
        if choice == GoldenCard.active_prev:
            player.card_balance.gold_a_prev -= 1
        elif choice == GoldenCard.inactive_cur:
            player.card_balance.gold_n_cur -= 1
        elif choice == GoldenCard.inactive_prev:
            player.card_balance.gold_n_prev -= 1

        for _ in range(self.params.boxes_per_g_card):
            self.open_box(player)

    def give_jackpot(self, uuid, players):
        player = players[uuid]
        assert player.card_balance.gold_a_cur > self.params.golden_set, "Player has not golden set, but he wants jackpot!"
        player.card_balance.gold_a_cur -= self.params.golden_set
        self.treasure -= self.params.jackpot
        player.earned_usd += self.params.jackpot

    def _choose_golden_card(self, player, prev_only=False):
        choices = []
        if player.card_balance.gold_a_prev > 0:
            choices.append(GoldenCard.active_prev)
        if not prev_only and player.card_balance.gold_n_cur > 0:
            choices.append(GoldenCard.inactive_cur)
        if player.card_balance.gold_n_prev > 0:
            choices.append(GoldenCard.inactive_prev)

        if len(choices) == 0:
            choice = None
        else:
            choice = random.choice(choices)

        return choice




