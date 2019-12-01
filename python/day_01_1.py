import math
import sys
import unittest


def fuel(mass):
    return math.floor(mass / 3.0) - 2


def fuel_sum(masses):
    total_fuel = 0
    for mass in masses:
        total_fuel += fuel(int(mass))

    return total_fuel


class Test(unittest.TestCase):
    def test_test(self):
        self.assertEqual(fuel(12), 2)
        self.assertEqual(fuel(100756), 33583)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("please pass the input as an argument to this script")
        sys.exit(-1)
    argument = sys.argv[1]

    with open(argument) as f:
        lines = f.readlines()

    print(fuel_sum(lines))
