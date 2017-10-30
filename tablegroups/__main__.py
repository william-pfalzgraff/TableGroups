import click
import pandas as pd

from .Classroom import Classroom, Student


@click.command()
@click.argument('path', type=click.Path())
@click.option('--size', '-s', type=int, default=4)
@click.option('--beta', '-b', type=float, default=4.5)
def cli(path, size, beta):
    student_data = pd.read_csv(path)
    students = [Student(str(idx), score) for idx, score in zip(student_data.id, student_data.score)]
    c = Classroom(students, group_size=size, beta=beta)
    c.optimize()
    print('Best cost: {}'.format(c.best_score))
    for group in c.best_groups:
        click.echo(list(group))

if __name__ == '__main__':
    cli()
