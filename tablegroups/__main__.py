import click
import pandas as pd

from .group_building import group_students



@click.command()
@click.argument('path', type=click.Path())
def cli(path):
    student_data = pd.read_csv(path)
    scores = {idx:score for idx, score in zip(student_data.id, student_data.score)}
    best_groups = group_students(student_data.id, scores)
    for group in best_groups:
        click.echo(list(group))

if __name__ == '__main__':
    cli()
