import random
import math
from uuid import UUID 

from card_game.types.player import Player
from card_game.types.misc_types import Action

def get_avg_new_players(today) -> int:
    assert today >= 0, "day must be positive"
    return int(150.0 * 1.005**math.log(today + 1.0))

def get_new_players_count(today) -> int:
    avg_players_count = get_avg_new_players(today)
    new_players_count = random.randint(avg_players_count - 50, avg_players_count + 50)
    return new_players_count


def get_new_payable_players_count(new_players_count, conversion_factor) -> int:
    new_payable_players_count = int(conversion_factor * new_players_count)
    return new_payable_players_count

def get_top_5(players: list[Player]) -> tuple[list[UUID], int]:
    sorted_attribute = lambda x: x.card_balance.gold_a_cur
    players = sorted(players, key=sorted_attribute, reverse=True)
    top_5_sum = 0
    top_5_list = []
    for player in players[:5]:
        top_5_sum += player.card_balance.gold_a_cur
        top_5_list.append(player.uuid)

    return top_5_list, top_5_sum

def execute_action(action, system, market, players, gamers, conspirators) -> bool:
    uuid, action = action
    jackpot_issued = False
    if action == Action.LEAVE_GAME:
        # sell all golden cards to game - the worst scenario
        market.cancel_bids(uuid, players)
        system.buy_all_golden_cards(uuid, players)
        players.pop(uuid)
    elif action == Action.SELL_GOLDEN_CARD_TO_GAME:
        system.buy_golden_card(uuid, players)
    elif action == Action.BUY_BOX:
        system.sell_box(uuid, players)
    elif action == Action.PLAY_IN_GOLDEN_LEAGUE:
        gamers.append( (uuid, True) )
    elif action == Action.PLAY_IN_COMMON_LEAGUE:
        gamers.append( (uuid, False) )
    elif action == Action.BUY_GOLDEN_CARD_FROM_GAME:
        system.sell_golden_card(uuid, players)
    elif action == Action.CHANGE_CARDS_TO_GOLDEN:
        system.change_cards_to_golden(uuid, players)
    elif action == Action.CONVERT_PAST_GOLDEN_CARDS_TO_CURRENT:
        system.convert_past_golden_cards_to_current(uuid, players)
    elif action == Action.EXCHANGE_GOLDEN_CARD_TO_BOXES:
        system.exchange_golden_card_to_boxes(uuid, players)
    elif action == Action.BUY_GOLDEN_CARD_FROM_MARKET:
        market.send_golden_card_purchase_bid(uuid, players)
    elif action == Action.BUY_CARD_FROM_MARKET:
        market.send_card_purchase_bid(uuid, players)
    elif action == Action.SELL_GOLDEN_CARD_TO_MARKET:
        market.send_golden_card_sale_bid(uuid, players)
    elif action == Action.SELL_CARD_TO_MARKET:
        market.send_card_sale_bid(uuid, players)
    elif action == Action.TRY_COLLUSION:
        conspirators.append(uuid)
    elif action == Action.GET_JACKPOT:
        system.give_jackpot(uuid, players)
        jackpot_issued = True
    else:
        assert False, "Illegal action: {action}"

    return jackpot_issued

def process_collusions(system, players, conspirators) -> int:
    golden_set = system.params.golden_set
    jackpot = system.params.jackpot
    golden_set_collected = False
    cards_needed = golden_set
    g_set_participants = []
    for c in conspirators:
        player = players[c]
        g_cards = player.card_balance.gold_a_cur
        if g_cards <= cards_needed:
            g_set_participants.append( (c, g_cards) )
            cards_needed -= g_cards
        else:
            g_set_participants.append( (c, cards_needed) )
            cards_needed = 0

        if cards_needed == 0:
            golden_set_collected = True
            break
    
    if golden_set_collected:
        system.treasure -= jackpot
        for c, g_cards in g_set_participants:
            player = players[c]
            player.card_balance.gold_a_cur -= g_cards
            player.earned_usd += jackpot * g_cards / golden_set
        
        return 1 + process_collusions(system, players, conspirators)
    else:
        return 0

