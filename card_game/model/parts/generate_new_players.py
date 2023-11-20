from card_game.types.player import Player
from uuid import uuid4
from .utils import get_new_players_count, get_new_payable_players_count

def p_generate_new_players(params, _2, _3, state):
    conversion_factor = params['to_payable_conversion_factor']
    player_coeffs = params['player_coeffs']
    betatest_enabled = params['betatest_enabled']
    betatest_limit = params['betatest_limit']

    today = state['day']
    system = state['system']
    new_day_has_begun =  state['new_day_has_begun']
    updated_players = state['players']

    if new_day_has_begun:
        new_players_count = get_new_players_count(today)
        new_playable_players_count = get_new_payable_players_count(new_players_count, conversion_factor)

        if betatest_enabled:
            players_num = len(updated_players)
            new_playable_players_count = max(0, min(new_playable_players_count, betatest_limit - players_num))

        for ii in range(new_playable_players_count):
            new_uuid = uuid4()
            player = Player(new_uuid, player_coeffs)
            # get one box to player FOR FREE
            system.open_box(player)
            assert player.card_balance.ordinary > 0, \
                f"Player has {player.card_balance.ordinary} cards after open box." 
            assert updated_players.get(new_uuid, 0) == 0, f"Step {ii}: unique Id is not unique!"
            updated_players[new_uuid] = player

    return {'updated_players': updated_players}