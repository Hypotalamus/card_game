from card_game.model.parts.update_day import p_update_day
from card_game.model.params import DAYS_PER_MONTH

def test_update_day():
    steps_num = 9000
    steps_per_day = 30
    steps_per_season = steps_per_day * DAYS_PER_MONTH

    # Generate reference values
    ref_days = [ii // steps_per_day + 1 for ii in range(steps_num)]
    ref_seasons = [ii // steps_per_season + 1 for ii in range(steps_num)]

    ref_new_day_flag = steps_num * [0]
    ref_new_day_flag[0] = 1
    for ii in range(1, steps_num):
        ref_new_day_flag[ii] = ref_days[ii] - ref_days[ii - 1]
    ref_new_day_flag = [bool(el) for el in ref_new_day_flag]

    ref_new_season_flag = steps_num * [0]
    ref_new_season_flag[0] = 1
    for ii in range(1, steps_num):
        ref_new_season_flag[ii] = ref_seasons[ii] - ref_seasons[ii - 1]
    ref_new_season_flag = [bool(el) for el in ref_new_season_flag]

    # test function
    params = {
        'steps_per_day': steps_per_day,
        'days_per_season': DAYS_PER_MONTH,
    }

    state = {
        'day': 0,
        'season': 0,
        'timestep': 0,
    }

    for ii in range(steps_num):
        res = p_update_day(params, None, None, state)

        assert res['updated_day'] == ref_days[ii], \
            f"Error in days, step {ii}: {res['updated_day']} != {ref_days[ii]}"
        assert res['updated_new_day_flag'] == ref_new_day_flag[ii], \
            f"Error in new_day_flag, step {ii}: {res['updated_new_day_flag']} != {ref_new_day_flag[ii]}"
        assert res['updated_season'] == ref_seasons[ii], \
            f"Error in seasons, step {ii}: {res['updated_season']} != {ref_seasons[ii]}"
        assert res['updated_new_season_flag'] == ref_new_season_flag[ii], \
            f"Error in new_season_flag, step {ii}: {res['updated_new_season_flag']} != {ref_new_season_flag[ii]}"
        
        state = {
            'day': res['updated_day'],
            'season': res['updated_season'],
            'timestep': ii + 1,
        }