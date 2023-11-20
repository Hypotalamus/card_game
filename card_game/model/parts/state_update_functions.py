def s_update_players(_1, _2, _3, _4, input_policy):
    updated_players = input_policy['updated_players']
    return 'players', updated_players

def s_update_actions(_1, _2, _3, _4, input_policy):
    updated_actions = input_policy['updated_actions']
    return 'actions', updated_actions

def s_update_system(_1, _2, _3, _4, input_policy):
    updated_system = input_policy['updated_system']
    return 'system', updated_system

def s_update_market(_1, _2, _3, _4, input_policy):
    updated_market = input_policy['updated_market']
    return 'market', updated_market

def s_update_day(_1, _2, _3, _4, input_policy):
    updated_day = input_policy['updated_day']
    return 'day', updated_day

def s_update_new_day_flag(_1, _2, _3, _4, input_policy):
    updated_new_day_flag = input_policy['updated_new_day_flag']
    return 'new_day_has_begun', updated_new_day_flag

def s_update_season(_1, _2, _3, _4, input_policy):
    updated_season = input_policy['updated_season']
    return 'season', updated_season

def s_update_new_season_flag(_1, _2, _3, _4, input_policy):
    updated_new_season_flag = input_policy['updated_new_season_flag']
    return 'new_season_has_begun', updated_new_season_flag

def s_update_players_num(_1, _2, _3, _4, input_policy):
    updated_players_num = input_policy['updated_players_num']
    return 'players_num', updated_players_num

def s_update_system(_1, _2, _3, _4, input_policy):
    updated_system = input_policy['updated_system']
    return 'system', updated_system

def s_update_market(_1, _2, _3, _4, input_policy):
    updated_market = input_policy['updated_market']
    return 'market', updated_market

def s_update_collusions_num(_1, _2, _3, state, input_policy):
    updated_collusions_num = state['collusions_num'] + input_policy['new_collusions']
    return 'collusions_num', updated_collusions_num

def s_update_jackpots_num(_1, _2, _3, state, input_policy):
    updated_jackpots_num = state['jackpots_num'] + input_policy['new_jackpots']
    return 'jackpots_num', updated_jackpots_num

def s_update_treasure(_1, _2, _3, _4, input_policy):
    updated_treasure = input_policy['updated_treasure']
    return 'treasure', updated_treasure

def s_update_g_card_marketprice(_1, _2, _3, _4, input_policy):
    updated_g_card_marketprice = input_policy['updated_g_card_marketprice']
    return 'g_card_marketprice', updated_g_card_marketprice

def s_update_card_marketprice(_1, _2, _3, _4, input_policy):
    updated_card_marketprice = input_policy['updated_card_marketprice']
    return 'card_marketprice', updated_card_marketprice

def s_update_sell_g_orders_num(_1, _2, _3, _4, input_policy):
    updated_sell_g_orders_num = input_policy['updated_sell_g_orders_num']
    return 'sell_g_orders_num', updated_sell_g_orders_num

def s_update_buy_g_orders_num(_1, _2, _3, _4, input_policy):
    updated_buy_g_orders_num = input_policy['updated_buy_g_orders_num']
    return 'buy_g_orders_num', updated_buy_g_orders_num

def s_update_sell_orders_num(_1, _2, _3, _4, input_policy):
    updated_sell_orders_num = input_policy['updated_sell_orders_num']
    return 'sell_orders_num', updated_sell_orders_num

def s_update_buy_orders_num(_1, _2, _3, _4, input_policy):
    updated_buy_orders_num = input_policy['updated_buy_orders_num']
    return 'buy_orders_num', updated_buy_orders_num

def s_update_g_cards_max_per_player(_1, _2, _3, _4, input_policy):
    updated_g_cards_max_per_player = input_policy['updated_g_cards_max_per_player']
    return 'g_cards_max_per_player', updated_g_cards_max_per_player