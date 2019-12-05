"""
Implement and Intcode machine, which I think is probably just a tape-based
turing machine ish thing

How to implement:

parse source into the memory, a list of integers

create an instruction pointer (ip), which points at the
current instruction address

while we haven't hit the 99 instruction (or run off the end of memory):
    look at / parse current instruction
    update memory
    advance ip
    (4 at the moment, but that will change in day 5)
"""
import itertools
import unittest


class Intcode:
    def __init__(self, raw_source):
        self.raw_source = raw_source
        self.memory = self._parse(raw_source)
        self.ip = 0

    """
    Execute the current instruction at ip

    Returns either the next value of ip, or None when opcode 99 is reached

    May also raise ValueError if the current instruction pointed
    at by ip is invalid
    """
    def step(self):
        current_instruction = self.memory[self.ip]
        if current_instruction == 99:
            return None
        elif current_instruction == 1:
            # handle ADD
            addr_1, addr_2, save_addr = self.memory[self.ip + 1:self.ip + 4]
            param_1 = self.memory[addr_1]
            param_2 = self.memory[addr_2]

            self.memory[save_addr] = param_1 + param_2

            return self.ip + 4
        elif current_instruction == 2:
            # handle multiply
            addr_1, addr_2, save_addr = self.memory[self.ip + 1:self.ip + 4]
            param_1 = self.memory[addr_1]
            param_2 = self.memory[addr_2]

            self.memory[save_addr] = param_1 * param_2

            return self.ip + 4
        else:
            raise ValueError(
                f'Invalid opcode {current_instruction} at {self.ip}')

    def run(self):
        while True:
            result = self.step()
            if result is None:
                break
            self.ip = result

    def _parse(self, raw):
        return list(map(int, raw.split(",")))


class Test(unittest.TestCase):
    EXAMPLE = "1,9,10,3,2,3,11,0,99,30,40,50"

    def test_parse(self):
        self.assertEqual(
            [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
            Intcode(self.EXAMPLE).memory)

    def test_add_step_size(self):
        machine = Intcode(self.EXAMPLE)
        self.assertEqual(4, machine.step())

    def test_add_step(self):
        machine = Intcode(self.EXAMPLE)
        machine.step()
        self.assertEqual(70, machine.memory[3])

    def test_multiply_step_size(self):
        machine = Intcode(self.EXAMPLE)
        machine.ip = 4
        self.assertEqual(8, machine.step())

    def test_multiply_step(self):
        machine = Intcode(self.EXAMPLE)
        machine.ip = 4
        machine.step()
        self.assertEqual(150, machine.memory[0])

    def test_run_simple_add(self):
        machine = Intcode("1,0,0,0,99")
        machine.run()
        self.assertEqual([2, 0, 0, 0, 99], machine.memory)

    def test_run_simple_multiply(self):
        machine = Intcode("2,3,0,3,99")
        machine.run()
        self.assertEqual([2, 3, 0, 6, 99], machine.memory)

    def test_run_simple_multiple_2(self):
        machine = Intcode("2,4,4,5,99,0")
        machine.run()
        self.assertEqual([2, 4, 4, 5, 99, 9801], machine.memory)

    def test_run_1(self):
        machine = Intcode("1,1,1,4,99,5,6,0,99")
        machine.run()
        self.assertEqual([30, 1, 1, 4, 2, 5, 6, 0, 99], machine.memory)

    def test_run_2(self):
        machine = Intcode(self.EXAMPLE)
        machine.run()
        self.assertEqual(
            [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
            machine.memory)


if __name__ == "__main__":
    # unittest.main()
    with open("inputs/day02.txt") as f:
        source = f.read()

    needed_output = 19690720
    for noun in itertools.count():  # from 0 to infinity
        for verb in range(0, noun + 1):
            machine = Intcode(source)
            machine.memory[1] = noun
            machine.memory[2] = verb

            machine.run()

            if machine.memory[0] == needed_output:
                print(f"found {noun * 100 + verb}: {noun=} {verb=}")
                exit()
