import unittest
from .group_building import group_students
import random
import numpy as np


class Testgroup(unittest.TestCase):


    def setUp(self):
        random.seed(230814)
        self.ids = []
        self.scores = {}
        # Generate some fake student data
        for _ in range(100):
            my_id = random.randint(50000000,60000000)
            self.ids.append(my_id)
            self.scores[my_id] = int(np.floor(random.gauss(70.,12.)))

    def test_group_students(self):
        best_groups = group_students(self.ids, self.scores)

        for group in best_groups:
            scores_in_group = []
            for student in group:
                scores_in_group.append(self.scores[student])
            print(scores_in_group)

if __name__ == '__main__':
    unittest.main()
