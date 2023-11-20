from uuid import uuid4
import random

from card_game.types.player import Player
from card_game.types.system import System
from card_game.model.parts.generate_new_players import p_generate_new_players
from card_game.model.params import DEFAULT_PLAYER_COEFFS, DEFAULT_SYSTEM_PARAMS

def test_previous_players_remain_untouched():
    random.seed(12345)
    init_players_dict = dict()
    new_uuid = uuid4()
    new_player = Player(new_uuid, DEFAULT_PLAYER_COEFFS)
    init_players_dict[new_uuid] = new_player
    test_system = System(DEFAULT_SYSTEM_PARAMS, 900)

    params = {
        'to_payable_conversion_factor': 0.02,
        'player_coeffs': DEFAULT_PLAYER_COEFFS,
        'betatest_enabled': False,
        'betatest_limit': 1000,
    }
    test_state = {
        'day': 50,
        'new_day_has_begun': True,
        'players': init_players_dict,
        'system': test_system
    }

    res = p_generate_new_players(params, None, None, test_state)
    assert len(res['updated_players']) > 1, "New players were not added."
    assert id(res['updated_players'][new_uuid]) == id(new_player), "Old player was lost."
    assert id(res['updated_players']) == id(init_players_dict), "Handlers point to different objectss."