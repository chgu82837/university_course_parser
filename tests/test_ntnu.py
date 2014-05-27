import sys
sys.path.append('/home/cjhwong/Workspace/GitHub/subjects')

import unittest
from subjects.ntnu.course_parser import Parser


class parser_test(unittest.TestCase):
    def test_format_time(self):
        target = Parser()
        self.assertEqual(target.format_time('四 6-8 校外 校外教室,'), '4678')
        self.assertEqual(target.format_time('二 3-4 公館 Ｅ101,五 7 公館 Ｅ101,'), '234,57')

if __name__ == '__main__':
    unittest.main()
