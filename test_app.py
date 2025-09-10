# test_app.pydds
# CI/CD 실습을 위한 파이썬 단위 테스트 코드ㅇ
import unittest
from app import add, subtract

class TestAppFunctions(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(0, 0), 0)

    def test_add_negative_numbers(self):
        self.assertEqual(add(-1, -1), -2)
        self.assertEqual(add(-5, 3), -2)

    def test_subtract_positive_numbers(self):
        self.assertEqual(subtract(5, 2), 3)
        self.assertEqual(subtract(10, 10), 0)

    def test_subtract_negative_numbers(self):
        self.assertEqual(subtract(2, 5), -3)
        self.assertEqual(subtract(-5, -10), 5)

if __name__ == '__main__':
    unittest.main()