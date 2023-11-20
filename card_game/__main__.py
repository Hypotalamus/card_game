import click

from card_game.model.run import run, generate_report

@click.command()
@click.option(
    '-t', '--steps_num', 'steps_num',
    default=0,
    help='Numbers of simulation timesteps',
    type=int
)
@click.option(
    '-r', '--gen_report', is_flag=True,
    help='Generate html report'
)
def main(steps_num, gen_report):
    if gen_report:
        generate_report(timesteps_num=steps_num)
    else:
        run(timesteps_num=steps_num)



if __name__ == "__main__":
    main()