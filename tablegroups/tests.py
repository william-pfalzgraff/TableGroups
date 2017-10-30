import unittest
import string
# from .group_building import optimize
from .Student import Student
from .Classroom import Classroom
import random
import numpy as np


# class Testgroup(unittest.TestCase):
#
#
#     def setUp(self):
#         random.seed(230814)
#         self.ids = []
#         self.scores = {}
#         # Generate some fake student data
#         for _ in range(101):
#             my_id = random.randint(50000000,60000000)
#             self.ids.append(my_id)
#             self.scores[my_id] = int(np.floor(random.gauss(70.,12.)))
#
#     def test_group_students(self):
#         best_groups = optimize(self.ids, self.scores)
#
#         for group in best_groups:
#             scores_in_group = []
#             for student in group:
#                 scores_in_group.append(self.scores[student])
#             print(scores_in_group)

class TestStudent(unittest.TestCase):

    def test_student(self):
        s = Student(ID='ABCD', score=85)
        print(s.ID)
        print(s.score)


class TestClassroom(unittest.TestCase):

    def setUp(self):
        self.students = [Student(ID=ID,
                                 score=int(np.floor(random.gauss(70.,12.))))
                         for ID in string.ascii_uppercase]
        print(self.students)


    def test_init(self):
        c = Classroom(self.students)
        print(c)



if __name__ == '__main__':
    unittest.main()
