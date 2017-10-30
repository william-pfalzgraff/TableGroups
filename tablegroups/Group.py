import numpy as np
# from collections.abc import Sequence, Set

class Group(frozenset):
    pass
    # _members = None

    # All groups share a cache dictionary of costs
    # _cache = dict()

    # def __init__(self, members):
    #     self._members = set([m for m in members if m is not None])
    #
    # def __len__(self):
    #     return len(self._members)
    #
    # def __repr__(self):
    #     return 'Group(size={})'.format(len(self))
    #
    # def __iter__(self):
    #     yield from self._members
    #
    # def __hash__(self):
    #     return hash(''.join([str(m.ID) for m in self]))
    #
    # def __len__(self):
    #     return len(self._members)
    #
    # def __getitem__(self, idx):
    #     return self._members[idx]
    #
    # def __contains__(self, member):
    #     return member in self._members
    #
    # def scores(self):
    #     return np.array([st.score for st in self])
    #
    # def max_difference(self):
    #     return np.max(self.scores()) - np.min(self.scores())
    #
    # def min_difference(self):
    #     return np.min(np.diff(np.sort(self.scores())))
    #
    # def mean(self):
    #     return np.mean(self.scores())
    #
    # def pop(self):
    #     pass
    #
    # def add(self):
    #     pass
    #
    # def replace(self, old_member, new_member):
    #     self.add(new_member)
    #     return self.pop(old_member)
    #
    # def cost(self):
    #     if repr(self) not in self._cache:
    #         # TODO: unpack
    #         cost = 0
    #         self._cache[repr(self)] = cost
    #     return self._cache[repr(self)]
