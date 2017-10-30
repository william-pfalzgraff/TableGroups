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


class BasicCost:

    # Desired max difference in score between members of a group.
    DESIRED_MAX = 20.
    # Desired min difference in score between members of a group.
    DESIRED_MIN = 3.
    # Impose an additional penalty if the average score of the table
    # is below this:
    DESIRED_MINIMUM_TABLE_MEAN = 60.

    def _cost(self, group):
        pass

    def scores(self):
        return np.array([st.score for st in self])

    def max_difference(self):
        return np.max(self.scores()) - np.min(self.scores())

    def min_difference(self):
        return np.min(np.diff(np.sort(self.scores())))

    def mean(self):
        return np.mean(self.scores())

    def pop(self):
        pass

    def add(self):
        pass

    def replace(self, old_member, new_member):
        self.add(new_member)
        return self.pop(old_member)

    def cost(self):
        if repr(self) not in self._cache:
            # TODO: unpack
            cost = 0
            self._cache[repr(self)] = cost
        return self._cache[repr(self)]

    def _cost_2(self, group):
        if len(group)<=2:
            return float('inf')
        score = 0.
        if group.max_difference() > DESIRED_MAX:
            score += DESIRED_MAX - group.max_difference()
        if group.min_difference() < DESIRED_MIN:
            score += 8*(group.min_difference() - DESIRED_MIN)
        if group.mean() <= DESIRED_MINIMUM_TABLE_MEAN:
            score += -6*(abs(group.mean() - DESIRED_MINIMUM_TABLE_MEAN))
        return score
