from .parts.policy_functions import *
from .parts.generate_new_players import p_generate_new_players
from .parts.update_day import p_update_day
from .parts.state_update_functions import *

partial_state_update_blocks: list[dict] = [
    {
        'label': 'Initialization',
        'policies': {
            'init': p_init,
        },
        'variables': {
            'system': s_update_system,
            'market': s_update_market,
        }
    },
    {
        'label': 'Day monitoring',
        'policies': {
            'update_day': p_update_day,
        },
        'variables': {
            'day': s_update_day,
            'new_day_has_begun': s_update_new_day_flag,
            'season': s_update_season,
            'new_season_has_begun': s_update_new_season_flag,
        }
    },
    {
        'label': 'New players come to the game',
        'policies': {
            'generate_new_players': p_generate_new_players,
        },
        'variables': {
            'players': s_update_players,
        }
    },
    {
        'label': 'Players choose actions',
        'policies': {
            'choose_actions': p_choose_actions,
        },
        'variables': {
            'actions': s_update_actions,
        },
    },
    {
        'label': 'Actions execution',
        'policies': {
            'execute_actions': p_execute_actions,
        },
        'variables': {
            'actions': s_update_actions,
            'system': s_update_system,
            'market': s_update_market,
            'players': s_update_players,
            'collusions_num': s_update_collusions_num,
            'jackpots_num': s_update_jackpots_num,
        },
    },
    {
        'label': 'Trading on market',
        'policies': {
            'trade_on_market': p_trade_on_market,
        },
        'variables': {
            'system': s_update_system,
            'market': s_update_market,
        },
    },
    {
        'label': 'Calculate system metrics',
        'policies': {
            'calculate_metrics': p_calculate_metrics,
        },
        'variables': {
            'players_num': s_update_players_num,
            'treasure': s_update_treasure,
            'g_card_marketprice': s_update_g_card_marketprice,
            'card_marketprice': s_update_card_marketprice,
            'sell_g_orders_num': s_update_sell_g_orders_num,
            'buy_g_orders_num': s_update_buy_g_orders_num,
            'sell_orders_num': s_update_sell_orders_num,
            'buy_orders_num': s_update_buy_orders_num,
            'g_cards_max_per_player': s_update_g_cards_max_per_player,
        }
    },
    {
        'label': 'End cycle jobs',
        'policies': {
            'end_cycle_jobs': p_end_cycle_jobs,
        },
        'variables': {
            'system': s_update_system,
            'players': s_update_players,
            'market': s_update_market,
        }
    }
]

partial_state_update_blocks = [
    psub for psub in partial_state_update_blocks if psub.get('enabled', True) == True
]