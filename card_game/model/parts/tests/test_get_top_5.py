import random
from uuid import uuid4

from card_game.types.player import Player
from card_game.model.parts.utils import get_top_5
from card_game.model.params import DEFAULT_PLAYER_COEFFS 

def test_get_top_5():
    random.seed(12345)
    players_num = 10
    top_5_inds = random.sample(list(range(players_num)), k=5)
    top_5_g_cards_sum = 0
    ref_top_5 = []
    players = dict()

    for ii in range(players_num):
        new_uuid = uuid4()
        player = Player(new_uuid, DEFAULT_PLAYER_COEFFS)
        g_cards_num = random.randint(0, 30)
        if ii in top_5_inds:
            g_cards_num += 50
            top_5_g_cards_sum += g_cards_num
            ref_top_5.append((new_uuid, g_cards_num)) 
        player.card_balance.gold_a_cur = g_cards_num
        players[new_uuid] = player
    ref_top_5 = sorted(ref_top_5, key=lambda x: x[1], reverse=True)
    ref_top_5 = list(el[0] for el in ref_top_5)
    ref_top_5 = (ref_top_5, top_5_g_cards_sum)

    res = get_top_5(list(players.values()))

    assert res[1] == ref_top_5[1], f"Sum of cards mismatch: {res[1]} != {ref_top_5[1]}"
    for ii, (uuid, ref_uuid) in enumerate(zip(res[0], ref_top_5[0])):
        assert uuid == ref_uuid, f"Element {ii}: {uuid} != {ref_uuid}"

