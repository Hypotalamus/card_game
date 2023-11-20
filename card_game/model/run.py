import os
from datetime import datetime
from pathlib import Path
import papermill as pm
from cadCAD_tools import easy_run

from card_game.model.state_variables import state_variables
from card_game.model.params import params
from card_game.model.partial_state_update_blocks import partial_state_update_blocks

TIMESTEPS_NUM = 3000
RUNS_NUM = 1

def run(timesteps_num=0):
    if timesteps_num == 0: timesteps_num = TIMESTEPS_NUM

    res = easy_run(
        state_variables,
        params,
        partial_state_update_blocks,
        timesteps_num,
        RUNS_NUM,
        drop_substeps=True,
        assign_params=False,
    )
    return res

def generate_report(timesteps_num=0):
    if timesteps_num == 0: timesteps_num = TIMESTEPS_NUM

    cwd = Path(os.getcwd())
    runtime = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    input_nb_path = (cwd / 'card_game/templates/report_template.ipynb').expanduser()
    output_nb_path = (cwd / f'reports/{runtime}-report.ipynb').expanduser()
    pm.execute_notebook(
        input_nb_path,
        output_nb_path,
        parameters=dict(steps_num=timesteps_num)
    )

    export_cmd = f"jupyter nbconvert {output_nb_path} --to html "
    os.system(export_cmd)
    os.remove(output_nb_path)

