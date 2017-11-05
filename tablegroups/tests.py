import unittest
import string
from .Classroom import Classroom, Student
from .Cost import BasicCost
import random
import numpy as np



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

    def test_random_trade(self):
        c = Classroom(self.students)
        print(c.random_trade())


    def test_optimize(self):
        c = Classroom(self.students)
        c.optimize()
        print(c)


class TestCost(unittest.TestCase):

    def setUp(self):
        self.group = frozenset([Student(ID=ID,
                                 score=int(np.floor(random.gauss(70.,12.))))
                         for ID in 'ABCDEFGH'])

    def testBasicCost(self):
        b = BasicCost()
        print(b.cost(self.group))


if __name__ == '__main__':
    unittest.main()
