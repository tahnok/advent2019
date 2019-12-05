"""
Implement and Intcode machine, which I think is probably just a tape-based
turing machine ish thing

How to implement:

parse source into the tape, a list of integers

create a program counter (pc), which points at the current cell in the tape

while we haven't hit the 99 instruction (or run off the end of the tape):
    look at / parse current instruction
    update the tape
    advance the appropriate number of cells
    (4 at the moment, but that will change in day 5)
"""
import unittest


class Intcode:
    def __init__(self, raw_source):
        self.raw_source = raw_source
        self.tape = self._parse(raw_source)
        self.pc = 0

    """
    Execute the current instruction at pc

    Returns either the next value of PC, or None when opcode 99 is reached

    May also raise ValueError if the current instruction pointed
    at by pc is invalid
    """
    def step(self):
        current_instruction = self.tape[self.pc]
        if current_instruction == 99:
            return None
        elif current_instruction == 1:
            # handle ADD
            addr_1, addr_2, save_addr = self.tape[self.pc + 1:self.pc + 4]
            operand_1 = self.tape[addr_1]
            operand_2 = self.tape[addr_2]

            self.tape[save_addr] = operand_1 + operand_2

            return self.pc + 4
        elif current_instruction == 2:
            # handle multiply
            addr_1, addr_2, save_addr = self.tape[self.pc + 1:self.pc + 4]
            operand_1 = self.tape[addr_1]
            operand_2 = self.tape[addr_2]

            self.tape[save_addr] = operand_1 * operand_2

            return self.pc + 4
        else:
            raise ValueError(
                f'Invalid opcode {current_instruction} at {self.pc}')

    def run(self):
        while True:
            result = self.step()
            if result is None:
                break
            self.pc = result

    def _parse(self, raw):
        return list(map(int, raw.split(",")))


class Test(unittest.TestCase):
    EXAMPLE = "1,9,10,3,2,3,11,0,99,30,40,50"

    def test_parse(self):
        self.assertEqual(
            [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
            Intcode(self.EXAMPLE).tape)

    def test_add_step_size(self):
        machine = Intcode(self.EXAMPLE)
        self.assertEqual(4, machine.step())

    def test_add_step(self):
        machine = Intcode(self.EXAMPLE)
        machine.step()
        self.assertEqual(70, machine.tape[3])

    def test_multiply_step_size(self):
        machine = Intcode(self.EXAMPLE)
        machine.pc = 4
        self.assertEqual(8, machine.step())

    def test_multiply_step(self):
        machine = Intcode(self.EXAMPLE)
        machine.pc = 4
        machine.step()
        self.assertEqual(150, machine.tape[0])

    def test_run_simple_add(self):
        machine = Intcode("1,0,0,0,99")
        machine.run()
        self.assertEqual([2, 0, 0, 0, 99], machine.tape)

    def test_run_simple_multiply(self):
        machine = Intcode("2,3,0,3,99")
        machine.run()
        self.assertEqual([2, 3, 0, 6, 99], machine.tape)

    def test_run_simple_multiple_2(self):
        machine = Intcode("2,4,4,5,99,0")
        machine.run()
        self.assertEqual([2, 4, 4, 5, 99, 9801], machine.tape)

    def test_run_1(self):
        machine = Intcode("1,1,1,4,99,5,6,0,99")
        machine.run()
        self.assertEqual([30, 1, 1, 4, 2, 5, 6, 0, 99], machine.tape)

    def test_run_2(self):
        machine = Intcode(self.EXAMPLE)
        machine.run()
        self.assertEqual(
            [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
            machine.tape)


if __name__ == "__main__":
    # unittest.main()
    with open("inputs/day02.txt") as f:
        source = f.read()

    machine = Intcode(source)
    machine.tape[1] = 12
    machine.tape[2] = 2

    machine.run()

    print(machine.tape[0])
