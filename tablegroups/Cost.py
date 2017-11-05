import numpy as np


class BaseCost:

    _cache = None
    _cache_hits = 0
    _calculations = 0

    _weights = None

    def __init__(self):
        self._cache = dict()

    def cost(self, group):
        self._calculations += 1
        if group not in self._cache:
            self._cache[group] = self._cost(group)
        else:
            self._cache_hits += 1

        # NOTE: Typically running 70% cache hits using default parameters, 2017-10-29
        # if self._calculations%1000 == 0:
            # print('{}/{} ({:.2%})'.format(self._cache_hits, self._calculations, self._cache_hits/self._calculations))

        return self._cache[group]

    # Any cost function will require iterating over scores
    def _scores(self, group):
        return np.array([student.score for student in group])

    def _cost(self, group):
        raise NotImplementedError


class BasicCost(BaseCost):

    # Desired max difference in score between members of a group.
    DESIRED_MAX = 20.
    # Desired min difference in score between members of a group.
    DESIRED_MIN = 3.
    # Impose an additional penalty if the average score of the table
    # is below this:
    DESIRED_MINIMUM_TABLE_MEAN = 60.

    def __init__(self):
        # TODO: Make these alterable at runtime
        self._weight = {'max_difference': 1,
                        'min_difference': 8,
                        'mean': 6}

        self._threshold = {'max_difference': 20,
                           'min_difference': 3,
                           'mean': 60}

        super(BasicCost, self).__init__()


    def _max_difference(self, group):
        return (np.max(self._scores(group)) -
                np.min(self._scores(group))
                )

    def _min_difference(self, group):
        return np.min(np.diff(np.sort(self._scores(group))))

    def _mean(self, group):
        return np.mean(self._scores(group))

    def _cost(self, group):
        if len(group)<=2:
            return float('inf')
        score = 0.

        max_difference = self._max_difference(group)
        min_difference = self._min_difference(group)
        mean = self._mean(group)

        if max_difference > self._threshold['max_difference']:
            score += self._threshold['max_difference'] - max_difference
        if min_difference < self._threshold['min_difference']:
            score += 8*(min_difference - self._threshold['min_difference'])
        if mean < self._threshold['mean']:
            score += 6*(mean - self._threshold['mean'])
        return score
