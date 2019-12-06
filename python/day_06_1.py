import unittest


def count(orbits):
    """
    given a dict of edges in a tree (hopefull),
    count the number of paths from each node to the
    root of the tree (COM)
    """
    count = 0

    for body in orbits.keys():
        parent = orbits.get(body, None)
        while parent is not None:
            count += 1
            parent = orbits.get(parent, None)

    return count


def orbits(lines):
    """
    take an array of ["AAA)BBB"] where AAA is the orbited and BBB is
    the orbiter and return a dict of { orbiter: orbited}
    """
    orbitDict = {}

    for line in lines:
        orbited, orbiter = line.strip().split(")")
        orbitDict[orbiter] = orbited

    return orbitDict


class Test(unittest.TestCase):
    def testEdges(self):
        raw = [
            "COM)B",
            "B)C",
            "C)D",
            "D)E",
            "E)F",
            "B)G",
            "G)H",
            "D)I",
            "E)J",
            "J)K",
            "K)L",
        ]
        expected = {
            'B': 'COM',
            'C': 'B',
            'D': 'C',
            'E': 'D',
            'F': 'E',
            'G': 'B',
            'H': 'G',
            'I': 'D',
            'J': 'E',
            'K': 'J',
            'L': 'K'
        }
        actual = orbits(raw)
        self.assertEqual(expected, actual)

    def testCountOrbits(self):
        edges = {
            'C': 'B',
            'D': 'C',
            'E': 'D',
            'F': 'E',
            'G': 'B',
            'B': 'COM',
            'H': 'G',
            'I': 'D',
            'J': 'E',
            'K': 'J',
            'L': 'K'
        }
        self.assertEqual(42, count(edges))


if __name__ == "__main__":
    # unittest.main()
    with open("inputs/day06.txt") as f:
        source = f.readlines()

    print(count(orbits(source)))
