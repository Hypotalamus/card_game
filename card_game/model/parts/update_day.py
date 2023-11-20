def p_update_day(params, _2, _3, state):
    steps_per_day = params['steps_per_day']
    days_per_season = params['days_per_season']

    timestep = state['timestep']
    updated_day = state['day']
    updated_new_day_flag = False
    updated_season = state['season']
    updated_new_season_flag = False

    updated_new_day_flag = (timestep % steps_per_day == 0)
    if updated_new_day_flag:
        updated_new_season_flag = (updated_day % days_per_season == 0)
        updated_day += 1
        if updated_new_season_flag:
            updated_season += 1

    return {
        'updated_day': updated_day,
        'updated_new_day_flag': updated_new_day_flag,
        'updated_season': updated_season,
        'updated_new_season_flag': updated_new_season_flag,
    }