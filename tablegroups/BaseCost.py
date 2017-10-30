import numpy as np


class BaseCost:

    _cache = None

    def __init__(self):
        self._cache = dict()

    def cost(self, group):
        if group not in self._cache:
            self._cache[group] = self._cost(group)
        return self._cache[group]

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

    def scores(self, group):
        return np.array([st.score for st in group])

    def max_difference(self, group):
        return (np.max(self.scores(group)) -
                np.min(self.scores(group))
                )

    def min_difference(self, group):
        return np.min(np.diff(np.sort(self.scores(group))))

    def mean(self, group):
        return np.mean(self.scores(group))

    def _cost(self, group):
        if len(group)<=2:
            return float('inf')
        score = 0.
        if self.max_difference(group) > self.DESIRED_MAX:
            score += self.DESIRED_MAX - self.max_difference(group)
        if self.min_difference(group) < self.DESIRED_MIN:
            score += 8*(self.min_difference(group) - self.DESIRED_MIN)
        if self.mean(group) <= self.DESIRED_MINIMUM_TABLE_MEAN:
            score += -6*(abs(self.mean(group) - self.DESIRED_MINIMUM_TABLE_MEAN))
        return score
