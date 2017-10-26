from __future__ import print_function

import numpy as np
import random
from itertools import zip_longest

# Desired max difference in score between members of a group.
DESIRED_MAX = 20.
# Desired min difference in score between members of a group.
DESIRED_MIN = 3.
# Impose an additional penalty if the average score of the table
# is below this:
DESIRED_MINIMUM_TABLE_MEAN = 60.
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

class Student:
    _score = None
    _ID = None

    def __init__(self, ID, score):
        self._ID = ID
        self._score = score

    def ID(self):
        return self._ID

    def score(self):
        return self._score

    def __repr__(self):
        return 'Student(ID={}, score={})'.format(self._ID, self._score)

class Group:
    _members = None

    def __init__(self, members):
        self._members = [m for m in members if m is not None]

    def __len__(self):
        return len(self._members)

    def __repr__(self):
        return 'Group(size={})'.format(len(self))

    def scores(self):
        return np.array([st.score() for st in self._members])

    def max_difference(self):
        return np.max(self.scores()) - np.min(self.scores())

    def min_difference(self):
        return np.min(np.diff(np.sort(self.scores())))

    def mean(self):
        return np.mean(self.scores())




def cost(group):
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


def build_groups(students, group_size=25):
    random.shuffle(students)
    # Magic incantation based on https://docs.python.org/3.6/library/itertools.html
    # Grouper function. It isn't pretty, but it splits the students simply and in the
    # Correct orientation. Inserts None to even up the group size
    groups =  list(zip(*zip_longest(*[iter(students)]*group_size, fillvalue=None)))

    groups = tuple([Group(students) for students in groups])

    print(groups)

    cached_group_scores = [cost(group) for group in groups]
    group_score = sum(cached_group_scores)
    return groups, group_score, cached_group_scores
    #
    # for j in range(num_groups):
    #     start_index = group_size*group_index
    #     end_index = start_index + 4
    #     if (end_index > (len(ids) - 1)):
    #         end_index = len(ids) - 1
    #     group = frozenset(ids[start_index:end_index])
    #     if start_index == end_index:
    #         print("WARNING: student in a group alone.")
    #         print([ids[start_index]])
    #         group = frozenset([ids[start_index]])
    #     assert len(group) != 0
    #     group_index +=1
    #     groups.add(group)
    #     score_for_group = score_group(group,scores)
    #     cached_group_scores[group] = score_for_group
    #     group_score += score_for_group
    # return groups, group_score, cached_group_scores

def optimize(ids, scores):
    students = [Student(idx, score) for idx, score in scores.items()]
    groups, group_score, cached_group_scores = build_groups(students)

    best_score = group_score
    best_groups = groups
    total_score = group_score

    iteration = 1
    iterations_since_last_improvement = 0.
    while iteration < MAX_ITERATIONS:
        if iterations_since_last_improvement > MAX_WAIT:
            break
        group_a, group_b = random.sample(groups,2)
        old_score = cached_group_scores[group_a] + \
                        cached_group_scores[group_b]
        student_1 = random.sample(group_a,1)
        student_2 = random.sample(group_b,1)
        new_group_a = group_a.difference(student_1).union(student_2)
        new_group_b = group_b.difference(student_2).union(student_1)

        new_score = 0.
        for new_group in (new_group_a, new_group_b):
            if new_group in cached_group_scores:
                new_score += cached_group_scores[new_group]
            else:
                score_for_group = score_group(new_group,scores)
                new_score += score_for_group
                cached_group_scores[new_group] = score_for_group

        if (new_score > old_score):
            accept_probability = 1
        else:
            accept_probability = np.exp(BETA*(new_score - old_score))

        iteration += 1
        if (random.random() < accept_probability):
            groups.remove(group_a)
            groups.remove(group_b)
            groups.add(new_group_a)
            groups.add(new_group_b)
            total_score -= old_score
            total_score += new_score
            if total_score > best_score:
                # Print some progress about how the score is improving
                print('\x1b[2K\r')
                print("Best score: {0}\r".format(int(total_score)))
                iterations_since_last_improvement = 0
                best_score = total_score
                best_groups = groups
        iterations_since_last_improvement += 1
    # Optinally shuffle the order of groups before returning
    best_groups = random.sample(best_groups,len(best_groups))
    return best_groups
