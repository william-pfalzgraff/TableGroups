from collections import namedtuple
import random
from itertools import zip_longest
import numpy as np
from .BaseCost import BasicCost

Student = namedtuple('Student', ['ID', 'score'])
Trade = namedtuple('Trade', ['group_a', 'student_a', 'new_group_a',
                             'group_b', 'student_b', 'new_group_b',
                             'cost'])


class Classroom:

    score = 0
    best_score = 0
    groups = None
    best_groups = None
    history = None

    # Maximum number of Monte Carlo iterations
    MAX_ITERATIONS = 300000
    # MAX_ITERATIONS = 300
    # Accept the current seats if you can't improve the score after
    # this many MC iterations
    MAX_WAIT = 15000
    # Determines the acceptance probability for Metropolis Monte Carlo.
    # Smaller values of BETA mean only moves that actually improve the score
    # will be accepted but the algorithm might fall into a local minimum
    # that it can't get out of. Larger values of BETA make the algorithm
    # more likely to find the global minimum, but too large a value of
    # BETA basically means you are just shuffling the tables without
    # improving them.  Empiricaly, BETA = 4.5 works pretty well.
    BETA = 4.5

    def __init__(self, students, group_size=4, cost_function=None):
        self._group_size = group_size
        self._make_groups(students)
        self.best_groups = self.groups
        self._coster = BasicCost()

        # self._score = sum([g.score() for g in self])

    def __repr__(self):
        return 'Classroom(\n{}\n)'.format('\n'.join([str(g) for g in self.groups]))

    def _make_groups(self, students):
        random.shuffle(students)
        # Magic incantation based on https://docs.python.org/3.6/library/itertools.html
        # Grouper function. It isn't pretty, but it splits the students simply and in the
        # Correct orientation. Inserts None to even up the group size
        groups =  list(zip(*zip_longest(*[iter(students)]*(len(students)//self._group_size), fillvalue=None)))
        # Remove Nones
        groups = [[s for s in group if s is not None] for group in groups]
        # Convert to a set of frozensets
        self.groups = set([frozenset(students) for students in groups])

    def __iter__(self):
        yield from self._groups

    def cost(self, group=None):
        if group is None:
            return sum(self.cost(g) for g in self.groups)
        return self._coster.cost(group)

    def random_trade(self):
        group_a, group_b = random.sample(self.groups,2)

        student_a = random.sample(group_a, 1)
        student_b = random.sample(group_b, 1)

        new_group_a = group_a.difference(student_a).union(student_b)
        new_group_b = group_b.difference(student_b).union(student_a)

        cost_difference = self.cost(new_group_a) + self.cost(new_group_b)
        cost_difference -= self.cost(group_a) + self.cost(group_b)

        trade = Trade(group_a=group_a, student_a=student_a, new_group_a=new_group_a,
                      group_b=group_b, student_b=student_b, new_group_b=new_group_b,
                      cost=cost_difference)

        return trade

    def iter_trade(self):
        while True:
            yield self.random_trade()

    def apply_trade(self, trade):
        self.groups.remove(trade.group_a)
        self.groups.remove(trade.group_b)
        self.groups.add(trade.new_group_a)
        self.groups.add(trade.new_group_b)
        self.score += trade.cost

    def optimize(self):

        iterations_since_last_improvement = 0

        for iteration, trade in enumerate(self.iter_trade()):

            if trade.cost < 0:
                accept_probability = 1
            else:
                accept_probability = np.exp(self.BETA*(trade.cost))

            if (random.random() < accept_probability):
                # print('trading {} for {}. Improving by {}'.format(trade.student_a, trade.student_b, trade.cost))
                self.apply_trade(trade)
                if self.score < self.best_score:
                    # Print some progress about how the score is improving
                    print("Best score: {0}\r".format(int(self.best_score)))
                    iterations_since_last_improvement = 0
                    self.best_score = self.score
                    self.best_groups = self.groups
            iterations_since_last_improvement += 1

            if iteration >= self.MAX_ITERATIONS:
                print('Reached maximum iteration number.')
                break
            elif iterations_since_last_improvement > self.MAX_WAIT:
                print('Reached maximum iterations without improvement.')
                break

        # Optinally shuffle the order of groups before returning
        self.best_groups = random.sample(self.best_groups, len(self.best_groups))
        return self.best_groups
