"""
given a set of transforms, how much ore do we need for 1 fuel?

how do we work backwards?


sample:

10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL

can I do this by "expanding" everything?

1 FUEL
7 A, 1 E
7 A + 7A + 1D
14A + 1D
14A + 7A + 1C
21A + 1C
21A + 7A + 1 B
28A + 1B
31 ore (with 2 a leftover)

"""
import unittest

from collections import namedtuple, defaultdict
from math import ceil

Reaction = namedtuple(
    'Reaction', 'output_chemical input_chemicals output_yield')


def expand(desired, reactions, precursors):
    """
    given a dict desired containing chemical => quantity, and a list of chemicals to precursor reactions
    return a new dict where each chemical it's precursor chemicals

    eg: expand(foo = {'FUEL': 2'}, reactions = {'FUEL': [(10, 'A')]}
        returns {'A': 20} 
    """
    result = defaultdict(int)
    for chemical, quantity in desired.items():
        if chemical in reactions:
            reaction = reactions[chemical]

            dont_expand = False
            for x in desired.keys():
                if chemical in precursors.get(x, set()):
                    dont_expand = True

            if dont_expand:
                result[chemical] += quantity
            else:
                num = ceil(quantity / reaction.output_yield)
                for input_chemical_tuple in reaction.input_chemicals:
                    result[input_chemical_tuple[0]
                           ] += input_chemical_tuple[1] * num
        else:
            result[chemical] += quantity

    return dict(result)


def looped_expand(desired, reactions, precursors):
    "expand until we can't no more"
    old = desired
    new = expand(desired, reactions, precursors)
    while old != new:
        old = new
        new = expand(old, reactions, precursors)

    return new


def precursor_chain(reactions):
    "given a set of reactions, make a dict of each chemical to a list of all of it's precussors"
    result = defaultdict(set)
    for chemical in reactions:
        to_visit = [chemical[0]
                    for chemical in reactions[chemical].input_chemicals]
        while to_visit:
            current = to_visit.pop()
            result[chemical].add(current)
            if current == 'ORE':
                continue
            to_add = set(
                [x[0] for x in reactions[current].input_chemicals]) - result[chemical]
            to_visit += list(to_add)

    return dict(result)


def ore_cost(reactions):
    desired = {'FUEL': 1}
    precursors = precursor_chain(reactions)
    almost = looped_expand(desired, reactions, precursors)
    return almost['ORE']


def parse_chem(raw_chem):
    "from '10 A' return ('A', 10)"
    quantity, chem = raw_chem.split(" ")
    return (chem, int(quantity))


def parse(raw):
    lines = list(
        filter(None,
               map(str.strip,
                   raw.split("\n"))))

    result = {}
    for line in lines:
        raw_chem_in, raw_chem_out = line.split(" => ")
        chem_in = list(map(parse_chem, raw_chem_in.split(", ")))
        chem_out, out_yield = parse_chem(raw_chem_out)
        result[chem_out] = Reaction(chem_out, chem_in, out_yield)

    return result


class Test(unittest.TestCase):
    simple = """
        10 ORE => 10 A
        1 ORE => 1 B
        7 A, 1 B => 1 C
        7 A, 1 C => 1 D
        7 A, 1 D => 1 E
        7 A, 1 E => 1 FUEL
        """

    medium = """
        9 ORE => 2 A
        8 ORE => 3 B
        7 ORE => 5 C
        3 A, 4 B => 1 AB
        5 B, 7 C => 1 BC
        4 C, 1 A => 1 CA
        2 AB, 3 BC, 4 CA => 1 FUEL
        """

    large = """
        157 ORE => 5 NZVS
        165 ORE => 6 DCFZ
        44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
        12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
        179 ORE => 7 PSHF
        177 ORE => 5 HKGWZ
        7 DCFZ, 7 PSHF => 2 XJWVT
        165 ORE => 2 GPVTF
        3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
        """

    xlarge = """
        2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
        17 NVRVD, 3 JNWZP => 8 VPVL
        53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
        22 VJHF, 37 MNCFX => 5 FWMGM
        139 ORE => 4 NVRVD
        144 ORE => 7 JNWZP
        5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
        5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
        145 ORE => 6 MNCFX
        1 NVRVD => 8 CXFTF
        1 VJHF, 6 MNCFX => 4 RFSQX
        176 ORE => 6 VJHF
        """

    xxlarge = """
        171 ORE => 8 CNZTR
        7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
        114 ORE => 4 BHXH
        14 VRPVC => 6 BMBT
        6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
        6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
        15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
        13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
        5 BMBT => 4 WPTQ
        189 ORE => 9 KTJDG
        1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
        12 VRPVC, 27 CNZTR => 2 XDBXC
        15 KTJDG, 12 BHXH => 5 XCVML
        3 BHXH, 2 VRPVC => 7 MZWV
        121 ORE => 7 VRPVC
        7 XCVML => 6 RJRHP
        5 BHXH, 4 VRPVC => 5 LTCX
        """

    def test_parse(self):
        result = parse(self.simple)
        expected = {
            'A': Reaction(output_chemical='A', input_chemicals=[('ORE', 10)], output_yield=10),
            'B': Reaction(output_chemical='B', input_chemicals=[('ORE', 1)], output_yield=1),
            'C': Reaction(output_chemical='C', input_chemicals=[('A', 7), ('B', 1)], output_yield=1),
            'D': Reaction(output_chemical='D', input_chemicals=[('A', 7), ('C', 1)], output_yield=1),
            'E': Reaction(output_chemical='E', input_chemicals=[('A', 7), ('D', 1)], output_yield=1),
            'FUEL': Reaction(output_chemical='FUEL', input_chemicals=[('A', 7), ('E', 1)], output_yield=1)
        }

        self.assertEqual(expected, result)

    def test_precursor_chain(self):
        reactions = parse(self.simple)
        result = precursor_chain(reactions)
        expected = {
            'A': {'ORE'},
            'B': {'ORE'},
            'C': {'B', 'ORE', 'A'},
            'D': {'B', 'ORE', 'C', 'A'},
            'E': {'C', 'A', 'B', 'D', 'ORE'},
            'FUEL': {'C', 'A', 'B', 'E', 'D', 'ORE'}
        }
        self.assertEqual(expected, result)

    def test_expand_1(self):
        reactions = parse(self.simple)
        precursors = precursor_chain(reactions)
        foo = {'FUEL': 1}
        expected = {'A': 7, 'E': 1}
        result = expand(foo, reactions, precursors)
        self.assertEqual(expected, result)

    def test_expand_2(self):
        reactions = parse(self.simple)
        precursors = precursor_chain(reactions)
        foo = {'FUEL': 1}
        expected = {'A': 14, 'D': 1}
        result = expand(expand(foo, reactions, precursors), reactions, precursors)
        self.assertEqual(expected, result)

    def test_ore_cost_simple(self):
        reactions = parse(self.simple)
        actual = ore_cost(reactions)
        self.assertEqual(31, actual)

    def test_ore_cost_medium(self):
        reactions = parse(self.medium)
        actual = ore_cost(reactions)
        self.assertEqual(165, actual)

    def test_ore_cost_large(self):
        reactions = parse(self.large)
        actual = ore_cost(reactions)
        self.assertEqual(13312, actual)

    def test_ore_cost_xlarge(self):
        reactions = parse(self.xlarge)
        actual = ore_cost(reactions)
        self.assertEqual(180697, actual)

    def test_ore_cost_xxlarge(self):
        reactions = parse(self.xxlarge)
        actual = ore_cost(reactions)
        self.assertEqual(2210736, actual)


if __name__ == "__main__":
    # unittest.main()
    with open("inputs/day14.txt") as f:
        source = f.read()


    print(ore_cost(parse(source)))