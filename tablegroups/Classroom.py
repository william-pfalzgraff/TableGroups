from .Cost import BasicCost

import random
import numpy as np
from click import progressbar
from collections import namedtuple
# This is to support python2.
try:
    from itertools import zip_longest as zip_longest
except:
    from itertools import izip_longest as zip_longest


Student = namedtuple('Student', ['ID', 'score'])
Trade = namedtuple('Trade', ['group_a', 'student_a', 'new_group_a',
                             'group_b', 'student_b', 'new_group_b',
                             'cost'])


class Classroom:

    score = 0
    best_score = 0
    groups = None
    best_groups = None

    # TODO: Provide a full history
    history = None

    # Maximum number of Monte Carlo iterations
    MAX_ITERATIONS = 100000
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

    def __init__(self, students, group_size=4, beta=4.5, cost_calculator=BasicCost):
        self._group_size = group_size
        self.BETA = beta

        # Initialize a cost calculation object. Necessary for the cache
        self._cost_calculator = cost_calculator()

        self._make_groups(students)
        self.score = self.best_score = self.cost()

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
        self.best_groups = self.groups = set([frozenset(students) for students in groups])

    def __iter__(self):
        # TODO: this requries python 3.
        #yield from self.groups
        for group in self.groups:
            yield group

    def cost(self, group=None):
        if group is None:
            return sum(self.cost(g) for g in self.groups)
        return self._cost_calculator.cost(group)

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
        for _ in range(self.MAX_ITERATIONS):
            yield self.random_trade()
        print('Reached maximum iteration number.')

    def apply_trade(self, trade):
        self.groups.remove(trade.group_a)
        self.groups.remove(trade.group_b)
        self.groups.add(trade.new_group_a)
        self.groups.add(trade.new_group_b)
        self.score += trade.cost

    def optimize(self):

        iterations_since_last_improvement = 0

        with progressbar(enumerate(self.iter_trade()),
                         length=self.MAX_ITERATIONS,
                         label='Maximum {} iterations:'.format(self.MAX_ITERATIONS)) \
                         as bar:
            for iteration, trade in bar:

                if trade.cost < 0:
                    accept_probability = 1
                else:
                    accept_probability = np.exp(self.BETA*(trade.cost))

                if (random.random() < accept_probability):
                    self.apply_trade(trade)
                    if self.score < self.best_score:
                        # Print some progress about how the score is improving
                        # print("Best score: {0}\r".format(int(self.best_score)))
                        iterations_since_last_improvement = 0
                        self.best_score = self.score
                        self.best_groups = frozenset(self.groups)
                    iterations_since_last_improvement = 0
                else:
                    iterations_since_last_improvement += 1

                if iterations_since_last_improvement > self.MAX_WAIT:
                    print('\nReached maximum {} iterations without improvement.'.format(self.MAX_WAIT))
                    break

        # Optinally shuffle the order of groups before returning
        self.best_groups = self.groups = random.sample(self.best_groups, len(self.best_groups))
