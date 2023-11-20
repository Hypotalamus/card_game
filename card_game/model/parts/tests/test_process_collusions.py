from uuid import uuid4


from card_game.model.parts.utils import process_collusions
from card_game.types.system import System
from card_game.types.player import Player
from card_game.model.params import DEFAULT_SYSTEM_PARAMS, DEFAULT_PLAYER_COEFFS

PLAYERS_NUM = 5

test_cases = [
    [10, 10, 10, 10, 10],
    [30, 40, 30, 20, 10],
    [99, 20, 30, 51, 20],
    [50, 40, 40, 85, 90],
]

ref_res = [0, 1, 2, 3]

ref_treasure = [50000.0, 45000.0, 40000.0, 35000.0]

ref_cards = [
    [10, 10, 10, 10, 10],
    [0, 0, 0, 20, 10],
    [0, 0, 0, 0, 20],
    [0, 0, 0, 0, 5],
]

ref_earned = [
    [0, 0, 0, 0, 0],
    [30/100 * 5000.0, 40/100 * 5000.0, 30/100 * 5000.0, 0, 0],
    [99/100 * 5000.0, 20/100 * 5000.0, 30/100 * 5000.0, 51/100 * 5000.0, 0],
    [50/100 * 5000.0, 40/100 * 5000.0, 40/100 * 5000.0, 85/100 * 5000.0, 85/100 * 5000.0]
]


def test_process_collusions():
    for ii, (test, ref, ref_tr, ref_g, ref_ea) in \
            enumerate( zip(test_cases, ref_res, ref_treasure, ref_cards, ref_earned) ):
        
        system = System(DEFAULT_SYSTEM_PARAMS, 900)
        system.treasure = 50000.0
        players = dict()
        conspirators = []

        for kk in range(PLAYERS_NUM):
            uuid = uuid4()
            player = Player(uuid, DEFAULT_PLAYER_COEFFS)
            player.card_balance.gold_a_cur = test[kk]
            conspirators.append(uuid)
            players[uuid] = player

        res = process_collusions(system, players, conspirators)

        assert res == ref, f"Test {ii}: Result mismatch: {res} != {ref}"
        assert system.treasure == ref_tr, f"Test {ii}: Treasure mismatch: {system.treasure} != {ref_tr}"

        for jj, uuid in enumerate(conspirators):
            player = players[uuid]
            g_cards = player.card_balance.gold_a_cur
            earned = player.earned_usd

            assert g_cards == ref_g[jj], f"Test {ii}, player {jj}: Cards mismatch: {g_cards} != {ref_g[jj]}"
            assert earned == ref_ea[jj], f"Test {ii}, player {jj}: Earned mismatch: {earned} != {ref_ea[jj]}"
