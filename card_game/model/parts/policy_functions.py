import random
from uuid import UUID

from card_game.types.system import System
from card_game.types.market import Market
from card_game.model.params import PLAYERS_PER_GAME
from card_game.model.parts.utils import get_top_5, execute_action, process_collusions

def p_init(params, _2, _3, state):
    system_params = params['system_params']
    market_params = params['market_params']
    steps_per_day = params['steps_per_day']
    days_per_season = params['days_per_season']
    steps_per_season = steps_per_day * days_per_season

    timestep = state['timestep']
    simulation = state['simulation']
    subset = state['subset']
    run = state['run']

    updated_system = state['system']
    updated_market = state['market']

    if timestep == 0:
        random.seed(simulation + subset + run)
        updated_system = System(system_params, steps_per_season - 1)
        updated_market = Market(market_params)
    
    return {
        'updated_system': updated_system,
        'updated_market': updated_market,
    }

def p_choose_actions(params, _2, _3, state):
    collusion_enabled = params['collusion_enabled']
    market_enabled = params['market_enabled']

    system = state['system']
    market = state['market']
    players = state['players']
    updated_actions = []

    top_5 = get_top_5(list(players.values()))
    for id, player in players.items():
        action = player.choose_action(system, market, top_5, collusion_enabled,
                                      market_enabled)
        updated_actions.append((id, action))

    return {'updated_actions': updated_actions}

def p_execute_actions(_1, _2, _3, state):
    updated_actions = state['actions']
    updated_system = state['system']
    updated_market = state['market']
    updated_players = state['players']
    conspirators: list[UUID] = []
    # bool - does player want to play in golden league? True - yes, False - no. 
    gamers: list[tuple[UUID, bool]] = []
    new_jackpots = 0

    random.shuffle(updated_actions)
    while len(updated_actions) > 0:
        action = updated_actions.pop()
        jackpot_issued = execute_action(action, updated_system, updated_market, 
                                        updated_players, gamers, conspirators)
        if jackpot_issued:
            new_jackpots += 1

    # play all games
    golden_league_players = [ uuid for uuid, is_golden_league in gamers if is_golden_league ]
    ordinary_league_players = [ uuid for uuid, is_golden_league in gamers if not is_golden_league ]

    games_num = len(golden_league_players) // PLAYERS_PER_GAME
    for ii in range(games_num):
        gamers = golden_league_players[PLAYERS_PER_GAME * ii:PLAYERS_PER_GAME * (ii + 1)]
        updated_system.play_round_in_golden_league(gamers, updated_players)

    games_num = len(ordinary_league_players) // PLAYERS_PER_GAME
    for ii in range(games_num):
        gamers = ordinary_league_players[PLAYERS_PER_GAME * ii:PLAYERS_PER_GAME * (ii + 1)]
        updated_system.play_round_in_ordinary_league(gamers, updated_players)

    # Realize collusions
    new_collusions = process_collusions(updated_system, updated_players, conspirators)
    new_jackpots += new_collusions

    return {
        'updated_actions': updated_actions,
        'updated_system': updated_system,
        'updated_market': updated_market,
        'updated_players': updated_players,
        'new_collusions': new_collusions,
        'new_jackpots': new_jackpots,
    }

def p_calculate_metrics(_1, _2, _3, state):
    players = state['players']
    system = state['system']
    market = state['market']

    updated_players_num = len(players)
    updated_treasure = system.treasure
    updated_g_card_marketprice = market.get_g_card_price()
    updated_card_marketprice = market.get_card_price()
    updated_sell_g_orders_num = len(market.sell_g_cards_book)
    updated_buy_g_orders_num = len(market.buy_g_cards_book)
    updated_sell_orders_num = len(market.sell_cards_book)
    updated_buy_orders_num = len(market.buy_cards_book)
    updated_g_cards_max_per_player = 0

    for player in players.values():
        if player.card_balance.gold_a_cur > updated_g_cards_max_per_player:
            updated_g_cards_max_per_player = player.card_balance.gold_a_cur

    return {
        'updated_players_num': updated_players_num,
        'updated_treasure': updated_treasure,
        'updated_g_card_marketprice': updated_g_card_marketprice,
        'updated_card_marketprice': updated_card_marketprice,
        'updated_sell_g_orders_num': updated_sell_g_orders_num,
        'updated_buy_g_orders_num': updated_buy_g_orders_num,
        'updated_sell_orders_num': updated_sell_orders_num,
        'updated_buy_orders_num': updated_buy_orders_num,
        'updated_g_cards_max_per_player': updated_g_cards_max_per_player,
    }

def p_end_cycle_jobs(params, _2, _3, state):
    steps_per_day = params['steps_per_day']
    days_per_season = params['days_per_season']
    steps_per_season = steps_per_day * days_per_season

    updated_system = state['system']
    updated_players = state['players']
    updated_market = state['market']
    new_season_flag = state['new_season_has_begun']
    step = state['timestep']

    for player in updated_players.values():
        player.steps_passed += 1

    if new_season_flag:
        updated_system.steps_until_season_end = steps_per_season
    updated_system.steps_until_season_end -= 1
    assert updated_system.steps_until_season_end >= 0, f"Steps can not be negative: {step}"

    if updated_system.steps_until_season_end == 0:
        for player in updated_players.values():
            # All bids from market will be canceled in the end of season
            uuid = player.uuid
            updated_market.cancel_bids(uuid, updated_players)

            # Cards of current season will become previous
            player.card_balance.gold_a_prev += player.card_balance.gold_a_cur
            player.card_balance.gold_a_cur = 0
            player.card_balance.gold_n_prev += player.card_balance.gold_n_cur
            player.card_balance.gold_n_cur = 0 

    return {
        'updated_system': updated_system,
        'updated_players': updated_players,
        'updated_market': updated_market,       
    }

def p_trade_on_market(_1, _2, _3, state):
    updated_system = state['system']
    updated_market = state['market']

    updated_market.process_bids(updated_system)
    updated_market.update_prices()

    return {
        'updated_system': updated_system,
        'updated_market': updated_market,
    }