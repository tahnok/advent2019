import unittest


def valid(code):
    return has_double(code) and no_decrease(code)


def has_double(code):
    results = dict()
    for x, y in pairwise(digits(code)):
        if x == y:
            count = results.get(x, 0)
            results[x] = count + 1
    return 1 in results.values()


def no_decrease(code):
    for x, y in pairwise(digits(code)):
        if x > y:
            return False
    else:
        return True


def digits(code):
    return [int(d) for d in str(code)]


def pairwise(list):
    return [(list[i], list[i+1]) for i in range(len(list) - 1)]


class Test(unittest.TestCase):
    def test_test(self):
        self.assertEqual([1, 2, 3, 4], digits(1234))

    def test_pairwise(self):
        self.assertEqual([(1, 2), (2, 3), (3, 4)], pairwise([1, 2, 3, 4]))

    def test_has_double(self):
        self.assertEqual(True, has_double(112367))
        self.assertEqual(False, has_double(123456))

    def test_no_decrease(self):
        self.assertEqual(True, no_decrease(1234567899))
        self.assertEqual(False, no_decrease(1297))
        self.assertEqual(False, no_decrease(1290))

    def test_valid(self):
        self.assertEqual(True, valid(112233))
        self.assertEqual(False, valid(123444))
        self.assertEqual(True, valid(111122))


if __name__ == "__main__":
    start = 271973
    end = 785961
    found = 0

    for code in range(start, end + 1):
        if valid(code):
            found += 1

    print(found)
