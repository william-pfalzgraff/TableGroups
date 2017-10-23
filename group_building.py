import numpy as np
import random

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

def scoring_function(max_difference, min_difference, mean_score):
    score = 0.
    if max_difference > DESIRED_MAX:
        score += DESIRED_MAX - max_difference 
    if min_difference < DESIRED_MIN:
        score += 8*(min_difference - DESIRED_MIN)
    if mean_score <= DESIRED_MINIMUM_TABLE_MEAN:
        score += -6*(abs(mean_score - DESIRED_MINIMUM_TABLE_MEAN))
    return score

def score_group(group,scores):
    group_scores = []
    for student in group:
        group_scores.append(scores[student])
    group_scores = np.array(group_scores)        
    max_difference = np.max(group_scores) - np.min(group_scores)
    # TODO: This will fail if the group size is 1.
    min_difference = np.min(np.diff(np.sort(group_scores)))
    mean_score = np.mean(group_scores)
    return scoring_function(max_difference, min_difference, mean_score)


def build_groups(ids,scores,group_size=4):
    groups = set() 
    group_index = 0
    num_groups = int(np.ceil(float(len(ids)) / group_size))
    group_score = 0.
    cached_group_scores = {}
    for j in range(num_groups):
        start_index = group_size*group_index 
        end_index = start_index + 4
        if (end_index > (len(ids) - 1)):
            end_index = len(ids) - 1
        group = frozenset(ids[start_index:end_index])
        if start_index == end_index:
            print "WARNING: student in a group alone."
            print [ids[start_index]]
            group = frozenset([ids[start_index]])
        assert len(group) != 0
        group_index +=1
        groups.add(group)
        score_for_group = score_group(group,scores)
        cached_group_scores[group] = score_for_group 
        group_score += score_for_group
    return groups, group_score, cached_group_scores

def group_students(student_ids,scores):
    ids = student_ids[:]
    random.shuffle(ids)
    groups, group_score, cached_group_scores = build_groups(ids,scores)
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
                print '\x1b[2K\r',
                print "Best score: {0}\r".format(int(total_score)),
                iterations_since_last_improvement = 0
                best_score = total_score
                best_groups = groups
        iterations_since_last_improvement += 1
    # Optinally shuffle the order of groups before returning
    best_groups = random.sample(best_groups,len(best_groups))
    return best_groups

def main():
    random.seed(230814)
    # Generate some fake student data
    ids = []
    scores = {}
    for j in range(100):
        my_id = random.randint(50000000,60000000) 
        ids.append(my_id)
        scores[my_id] = int(np.floor(random.gauss(70.,12.)))

    best_groups = group_students(ids,scores)

    for group in best_groups:
        scores_in_group = []
        for student in group:
            scores_in_group.append(scores[student])
        print scores_in_group
            

if __name__ == "__main__":
    main()
