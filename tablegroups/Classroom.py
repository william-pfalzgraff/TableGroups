from collections import namedtuple
import random
from itertools import zip_longest

Trade = namedtuple('Trade', ['group_a', 'student_a', 'group_b', 'student_b'])


class Classroom:

    _groups = None
    _best_groups = None
    _best_score = None
    _score = None
    _history = None

    _cache = None

    # Maximum number of Monte Carlo iterations
    MAX_ITERATIONS = 300000
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
        self._best_group = self._groups

        # self._score = sum([g.score() for g in self])
        # self._cache = dict()

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
        self.groups = groups = set([frozenset(students) for students in groups])

    def __iter__(self):
        yield from self._groups

    def draw(self):
        pass

    def random_trade(self):
        group_a, group_b = random.sample(groups,2)
        student_a = random.choice(group_a)
        student_b = random.choice(group_b)
        trade = Trade(group_A=group_a, group_B=group_b,
                      student_A=student_1, student_B=student_2)
        return trade

    def iter_trade(self):
        while True:
            yield self.random_trade()

    def trade_cost(self, trade):
        new_groups = self.apply_trade(trade)
        old_score = cached_group_scores[group_a] + \
                    cached_group_scores[group_b]
        new_group_a = group_a.difference(student_1).union(student_2)
        new_group_b = group_b.difference(student_2).union(student_1)

        new_score = 0.
        for new_group in (new_group_a, new_group_b):
            if new_group in cached_group_scores:
                new_score += cached_group_scores[new_group]
            else:
                score_for_group = cost(new_group,scores)
                new_score += score_for_group
                cached_group_scores[new_group] = score_for_group

        return self.cost(new_groups) - self.cost(self.groups)

    def prototype_trade(self, trade):
        new_group_a = trade.group_a.swap(trade.student_a, trade.student_b)
        new_group_b = trade.group_b.swap(trade.student_b, trade.student_a)

        cost_difference = new_group_a.cost() + new_group_b.cost()
        cost_difference -= group_a.cost() + group_b.cost()

        return new_group_a, new_group_b, cost_difference

    def apply_trade(self, trade):
        pass
        self.score += cost_difference

    def optimize(self):

        for iteration, trade in enumerate(self.iter_trade()):

            cost_difference = self.trade_cost(trade)

            if cost_difference < 0:
                accept_probability = 1
            else:
                accept_probability = np.exp(BETA*(new_score - old_score))

            if (random.random() < accept_probability):
                self.apply_trade(trade)
                if self.score > self.best_score:
                    # Print some progress about how the score is improving
                    print('\x1b[2K\r')
                    print("Best score: {0}\r".format(int(total_score)))
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
        best_groups = random.sample(best_groups, len(best_groups))
        return best_groups
