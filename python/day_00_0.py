# import math
import re
import sys
import unittest


class Test(unittest.TestCase):
    def test_test(self):
        self.assertEqual(True, True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("please pass the input as an argument to this script")
        sys.exit(-1)
    argument = sys.argv[1]

    with open(argument) as f:
        lines = f.readlines()

    matches = re.search(r'example', lines[0])

    print("TODO")
