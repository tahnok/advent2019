from collections import defaultdict
import unittest


def transferPath(start, end, paths):
    """
    given a dict of bodies : paths to com
    find the intersection body, and return the number of
    transfers from start to intersection + intersection to end
    """
    start_path = paths[start]
    end_path = paths[end]
    for distance, body in enumerate(start_path):
        if body in end_path:
            return distance + end_path.index(body)
    else:
        raise ValueError(f"No intersection between {start} and {end}")


def pathsToCom(orbits):
    """
    given a dict of edges in a tree (hopefull),
    return a dict of the path from each body to COM
    """
    paths = defaultdict(list)
    for body in orbits.keys():
        parent = orbits.get(body, None)
        while parent is not None:
            paths[body].append(parent)
            parent = orbits.get(parent, None)

    return dict(paths)


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

    def testPaths(self):
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
            "K)YOU",
            "I)SAN",
        ]
        expected = {
            'B': ['COM'],
            'C': ['B', 'COM'],
            'D': ['C', 'B', 'COM'],
            'E': ['D', 'C', 'B', 'COM'],
            'F': ['E', 'D', 'C', 'B', 'COM'],
            'G': ['B', 'COM'],
            'H': ['G', 'B', 'COM'],
            'I': ['D', 'C', 'B', 'COM'],
            'J': ['E', 'D', 'C', 'B', 'COM'],
            'K': ['J', 'E', 'D', 'C', 'B', 'COM'],
            'L': ['K', 'J', 'E', 'D', 'C', 'B', 'COM'],
            'YOU': ['K', 'J', 'E', 'D', 'C', 'B', 'COM'],
            'SAN': ['I', 'D', 'C', 'B', 'COM']
        }
        actual = pathsToCom(orbits(raw))
        self.assertEqual(expected, actual)

    def testTransferPath(self):
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
            "K)YOU",
            "I)SAN",
        ]
        paths = pathsToCom(orbits(raw))
        self.assertEqual(4, transferPath("YOU", "SAN", paths))


if __name__ == "__main__":
    # unittest.main()
    with open("inputs/day06.txt") as f:
        source = f.readlines()

    print(transferPath("YOU", "SAN", pathsToCom(orbits(source))))
