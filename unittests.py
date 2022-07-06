import unittest
from moodparser import songmood


class TestFileName(unittest.TestCase):
    def test_function1(self):
        (self.assertEqual(songmood("The Beatles","A Day in the Life"), [33,107]))


if __name__ == '__main__':
    unittest.main() 