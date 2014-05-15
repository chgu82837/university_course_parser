import unittest
from ntnu import parser


class parser_test(unittest.TestCase):
    def test_normalize(self):
        target = parser
        self.assertEqual(target._normalize('四 6-8 校外 校外教室,'), '4678')
        self.assertEqual(target._normalize('二 3-4 公館 Ｅ101,五 7 公館 Ｅ101,'), '234,57')

if __name__ == '__main__':
    unittest.main()
