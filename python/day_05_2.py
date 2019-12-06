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
import helpers
import unittest


class Intcode:

    # instructions
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99

    # modes
    POSITION = 0
    IMMEDIATE = 1

    def __init__(self, raw_source, inputs):
        self.raw_source = raw_source
        self.memory = self._parse(raw_source)
        self.ip = 0
        self.input = inputs
        self.output = []

    def step(self):
        # import pdb; pdb.set_trace()
        """
        Execute the current instruction at ip

        Returns either the next value of ip, or None when opcode 99 is reached

        May also raise ValueError if the current instruction pointed
        at by ip is invalid
        """
        current_instruction, modes = self.parse_instruction(
            self.memory[self.ip])

        if current_instruction == self.HALT:
            return None
        elif current_instruction == self.ADD:
            param_1, param_2, save_addr = self.memory[self.ip + 1:self.ip + 4]
            param_1_mode, param_2_mode, save_addr_mode = modes
            param_1 = self.resolve(param_1, param_1_mode)
            param_2 = self.resolve(param_2, param_2_mode)

            self.memory[save_addr] = param_1 + param_2

            return self.ip + 4
        elif current_instruction == self.MULTIPLY:
            param_1, param_2, save_addr = self.memory[self.ip + 1:self.ip + 4]
            param_1_mode, param_2_mode, save_addr_mode = modes
            param_1 = self.resolve(param_1, param_1_mode)
            param_2 = self.resolve(param_2, param_2_mode)

            self.memory[save_addr] = param_1 * param_2

            return self.ip + 4
        elif current_instruction == self.INPUT:
            addr = self.memory[self.ip + 1]
            self.memory[addr] = self.input

            return self.ip + 2
        elif current_instruction == self.OUTPUT:
            param = self.memory[self.ip + 1]
            value = self.resolve(param, modes[0])
            self.output.append(value)

            return self.ip + 2
        elif current_instruction == self.JUMP_IF_TRUE:
            param_1, param_2 = self.memory[self.ip + 1:self.ip + 3]
            param_1_mode, param_2_mode, _ = modes
            param_1 = self.resolve(param_1, param_1_mode)
            param_2 = self.resolve(param_2, param_2_mode)

            if param_1 != 0:
                return param_2
            else:
                return self.ip + 3
        elif current_instruction == self.JUMP_IF_FALSE:
            param_1, param_2 = self.memory[self.ip + 1:self.ip + 3]
            param_1_mode, param_2_mode, _ = modes
            param_1 = self.resolve(param_1, param_1_mode)
            param_2 = self.resolve(param_2, param_2_mode)

            if param_1 == 0:
                return param_2
            else:
                return self.ip + 3
        elif current_instruction == self.LESS_THAN:
            param_1, param_2, save_addr = self.memory[self.ip + 1:self.ip + 4]
            param_1_mode, param_2_mode, save_addr_mode = modes
            param_1 = self.resolve(param_1, param_1_mode)
            param_2 = self.resolve(param_2, param_2_mode)

            if param_1 < param_2:
                output = 1
            else:
                output = 0
            self.memory[save_addr] = output

            return self.ip + 4
        elif current_instruction == self.EQUALS:
            param_1, param_2, save_addr = self.memory[self.ip + 1:self.ip + 4]
            param_1_mode, param_2_mode, save_addr_mode = modes
            param_1 = self.resolve(param_1, param_1_mode)
            param_2 = self.resolve(param_2, param_2_mode)

            if param_1 == param_2:
                output = 1
            else:
                output = 0
            self.memory[save_addr] = output

            return self.ip + 4
        else:
            raise ValueError(
                f'Invalid opcode {current_instruction} at {self.ip}')

    def resolve(self, position_or_immediate, mode):
        if mode == Intcode.IMMEDIATE:
            return position_or_immediate
        elif mode == Intcode.POSITION:
            return self.memory[position_or_immediate]
        else:
            raise ValueError(f"Invalid mode {mode}")

    @staticmethod
    def parse_instruction(instruction):
        """
        take a raw instruction (like 2, or 1002) and return an instruction and
        list of modes
        ie: 2 -> (2, [0, 0, 0])
            1002 -> (2, [0, 1, 0])
        """
        if 0 < instruction < 100:
            return (instruction, [Intcode.POSITION, Intcode.POSITION,
                                  Intcode.POSITION])
        modes = helpers.digits(instruction)

        # combine rightmost 2 digits of instruction into new instruction
        instruction = modes.pop() + (10 * modes.pop())

        modes = list(reversed(modes))

        while len(modes) < 3:
            modes.append(Intcode.POSITION)

        return (instruction, modes)

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
            Intcode(self.EXAMPLE, 0).memory)

    def test_add_step_size(self):
        machine = Intcode(self.EXAMPLE, 0)
        self.assertEqual(4, machine.step())

    def test_add_step(self):
        machine = Intcode(self.EXAMPLE, 0)
        machine.step()
        self.assertEqual(70, machine.memory[3])

    def test_multiply_step_size(self):
        machine = Intcode(self.EXAMPLE, 0)
        machine.ip = 4
        self.assertEqual(8, machine.step())

    def test_multiply_step(self):
        machine = Intcode(self.EXAMPLE, 0)
        machine.ip = 4
        machine.step()
        self.assertEqual(150, machine.memory[0])

    def test_input_step_size(self):
        machine = Intcode("3,0,4,0,99", 0)
        self.assertEqual(2, machine.step())

    def test_input_step(self):
        machine = Intcode("3,0,4,0,99", 42)
        machine.step()
        self.assertEqual(42, machine.memory[0])

    def test_output_step_size(self):
        machine = Intcode("3,0,4,0,99", 0)
        machine.ip = 2
        self.assertEqual(4, machine.step())

    def test_output(self):
        machine = Intcode("3,0,4,0,99", 42)
        machine.run()
        self.assertEqual([42], machine.output)

    def test_parse_instruction_classic(self):
        self.assertEqual(
            (Intcode.ADD, [Intcode.POSITION,
                           Intcode.POSITION, Intcode.POSITION]),
            Intcode.parse_instruction(1)
        )

    def test_parse_instruction_complete(self):
        self.assertEqual(
            (Intcode.MULTIPLY, [Intcode.POSITION,
                                Intcode.IMMEDIATE, Intcode.POSITION]),
            Intcode.parse_instruction(1002)
        )

    # ------------------------------------ runs ---------------------------

    def test_run_simple_add(self):
        machine = Intcode("1,0,0,0,99", 0)
        machine.run()
        self.assertEqual([2, 0, 0, 0, 99], machine.memory)

    def test_run_simple_multiply(self):
        machine = Intcode("2,3,0,3,99", 0)
        machine.run()
        self.assertEqual([2, 3, 0, 6, 99], machine.memory)

    def test_run_simple_multiple_2(self):
        machine = Intcode("2,4,4,5,99,0", 0)
        machine.run()
        self.assertEqual([2, 4, 4, 5, 99, 9801], machine.memory)

    def test_run_1(self):
        machine = Intcode("1,1,1,4,99,5,6,0,99", 0)
        machine.run()
        self.assertEqual([30, 1, 1, 4, 2, 5, 6, 0, 99], machine.memory)

    def test_run_2(self):
        machine = Intcode(self.EXAMPLE, 0)
        machine.run()
        self.assertEqual(
            [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
            machine.memory)

    def test_run_with_modes(self):
        machine = Intcode("1002,4,3,4,33", 0)
        machine.run()
        self.assertEqual(
            [1002, 4, 3, 4, 99],
            machine.memory)

    def test_run_with_modes_negative(self):
        machine = Intcode("1101,100,-1,4,0", 0)
        machine.run()
        self.assertEqual(
            [1101, 100, -1, 4, 99],
            machine.memory
        )

    def test_run_with_equals_position(self):
        machine = Intcode("3,9,8,9,10,9,4,9,99,-1,8", 8)
        machine.run()
        self.assertEqual([1], machine.output)

        machine = Intcode("3,9,8,9,10,9,4,9,99,-1,8", 7)
        machine.run()
        self.assertEqual([0], machine.output)

    def test_run_with_less_than_position(self):
        machine = Intcode("3,9,7,9,10,9,4,9,99,-1,8", 8)
        machine.run()
        self.assertEqual([0], machine.output)

        machine = Intcode("3,9,7,9,10,9,4,9,99,-1,8", 6)
        machine.run()
        self.assertEqual([1], machine.output)

    def test_run_with_equals_immediate(self):
        machine = Intcode("3,3,1108,-1,8,3,4,3,99", 8)
        machine.run()
        self.assertEqual([1], machine.output)

        machine = Intcode("3,3,1108,-1,8,3,4,3,99", 7)
        machine.run()
        self.assertEqual([0], machine.output)

    def test_run_with_less_than_immediate(self):
        machine = Intcode("3,3,1107,-1,8,3,4,3,99", 8)
        machine.run()
        self.assertEqual([0], machine.output)

        machine = Intcode("3,3,1107,-1,8,3,4,3,99", 6)
        machine.run()
        self.assertEqual([1], machine.output)

    def test_run_complex_comparator(self):
        PROGRAM = ("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,"
                   "0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,"
                   "46,1101,1000,1,20,4,20,1105,1,46,98,99")
        machine = Intcode(PROGRAM, 6)
        machine.run()
        self.assertEqual([999], machine.output)

        machine = Intcode(PROGRAM, 8)
        machine.run()
        self.assertEqual([1000], machine.output)
        machine = Intcode(PROGRAM, 999)
        machine.run()
        self.assertEqual([1001], machine.output)


if __name__ == "__main__":
    # unittest.main()
    with open("inputs/day05.txt") as f:
        source = f.read()

    machine = Intcode(source, 5)
    machine.run()

    print(machine.output)
