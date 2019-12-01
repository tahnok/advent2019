import math
import sys
import unittest


def fuel(mass):
    temp = math.floor(mass / 3.0) - 2
    if temp > 0:
        return temp
    else:
        return 0


def fuel_iterative(mass):
    step_fuel = fuel(mass)
    total = 0
    while step_fuel > 0:
        total += step_fuel
        step_fuel = fuel(step_fuel)

    return total


def fuel_sum(masses):
    total_fuel = 0
    for mass in masses:
        total_fuel += fuel_iterative(int(mass))

    return total_fuel


class Test(unittest.TestCase):
    def test_fuel(self):
        self.assertEqual(fuel(12), 2)
        self.assertEqual(fuel(100756), 33583)
        self.assertEqual(fuel(2), 0)

    def test_fuel_iterative(self):
        self.assertEqual(fuel_iterative(12), 2)
        self.assertEqual(fuel_iterative(1969), 966)
        self.assertEqual(fuel_iterative(100756), 50346)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("please pass the input as an argument to this script")
        sys.exit(-1)
    argument = sys.argv[1]

    with open(argument) as f:
        lines = f.readlines()

    print(fuel_sum(lines))
