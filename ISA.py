class Registers:
    def __init__(self, reg_val, reg_adr):
        self.reg_val = reg_val
        self.reg_adr = reg_adr

    def set_reg_adr(self, reg_adr):
        self.reg_adr = reg_adr

    def get_reg_adr(self):
        return self.reg_adr

    def set_reg_val(self, reg_val):
        self.reg_val = reg_val

    def get_reg_val(self):
        return self.reg_val

    def to_32bit_val(self):
        if self.reg_val >= 0:
            return f"{self.reg_val:032b}"
        else:
            return bin(self.reg_val & 0xFFFFFFFF)[2:]

    def to_3bit_adr(self):
        reg_map = {"r0": "000", "r1": "001", "r2": "010", "r3": "011", "r4": "100", "r5": "101", "r6": "110", "r7": "111"}
        return reg_map.get(self.reg_adr, "")

class Memory:
    def __init__(self, size):
        self.size = size
        self.memory = [0] * size

    def read_memory(self, address):
        if 0 <= address < self.size:
            return self.memory[address]
        else:
            print("Error: Invalid memory address")
            return None

    def write_memory(self, address, value):
        if 0 <= address < self.size:
            self.memory[address] = value
        else:
            print("Error: Invalid memory address")

class InstructionSet:
    def __init__(self, step, opcode, register, clkcyc, operand="", value=None):
        self.step = step
        self.opcode = opcode
        self.register = register
        self.clkcyc = clkcyc
        self.operand = operand
        self.value = value if value is not None else register.get_reg_val()

    def five_bit_opcode(self):
        opcode_map = {
            "mov": "00001",
            "add": "00010",
            "mul": "00100",
            "sub": "00011",
            "div": "00101",
        }
        return opcode_map.get(self.opcode, "00000")

    def encode_instruction(self):
        opcode = self.five_bit_opcode()
        operand1 = self.register.to_3bit_adr()
        operand2 = self.to_32bit_val()#[-16:]
        return f"[{opcode} {operand1} {operand2}]"

    def to_32bit_val(self):
        if self.value >= 0:
            return f"{self.value:032b}"
        else:
            return bin(self.value & 0xFFFFFFFF)[2:]

def main():
    regs = [Registers(0, f"r{i}") for i in range(8)]
    instructions = []
    memory = Memory(1024)
    print("Enter instructions(eg. mov r1 10):")
    step = 0

    while True:
        instruction = input()
        if instruction == "end 0 0":
            break

        opcode, operand1, operand2 = instruction.split()
        operand2_reg = None
        register = None

        for reg in regs:
            if reg.get_reg_adr() == operand1:
                register = reg
            if reg.get_reg_adr() == operand2:
                operand2_reg = reg

        if operand2_reg is None:
            operand2_reg = Registers(int(operand2), operand2)

        if operand1 != operand2:
            operation_mapping = {
                "mov": lambda dest, src: dest.set_reg_val(src.get_reg_val()),
                "add": lambda dest, src: dest.set_reg_val(dest.get_reg_val() + src.get_reg_val()),
                "sub": lambda dest, src: dest.set_reg_val(dest.get_reg_val() - src.get_reg_val()),
                "mul": lambda dest, src: dest.set_reg_val(dest.get_reg_val() * src.get_reg_val()),
                "div": lambda dest, src: dest.set_reg_val(dest.get_reg_val() // src.get_reg_val()),
            }
            operation_mapping[opcode](register, operand2_reg)
            instructions.append(InstructionSet(
                step, opcode, register, 1, operand2_reg.get_reg_adr(), operand2_reg.get_reg_val()))
        step += 1

    print("\n  PC     Decoded:            Encoded instructions(32-bit):          Clock Cycles\n")
    for instruction in instructions:
        pc_str = f"PC[{instruction.step}]->"
        decoded_form = f"{pc_str} {instruction.opcode} {instruction.register.get_reg_adr()}"
        if instruction.operand != "":
            decoded_form += f" {instruction.operand}"
        decoded_form = decoded_form.ljust(20)
        encoded_form = instruction.encode_instruction().ljust(40)
        print(f"{decoded_form}: {encoded_form}       {instruction.clkcyc}")

    print("\nSteps of the Register\n")
    for instruction in instructions:
        reg_adr = instruction.register.to_3bit_adr()
        reg_val = instruction.register.get_reg_val()
        print(
            f"{reg_adr} = {reg_val:2} [{instruction.register.to_32bit_val()}]")

    print("\nContents of Main Memory\n")
    for i in range(10):
        print(f"Memory[{i}]: {memory.read_memory(i)}")

    print("\nAfter the program execution contents of the registers are..........\n")
    for reg in regs:
        reg_adr = reg.get_reg_adr()
        reg_val = reg.get_reg_val()
        print(f"{reg_adr} = {reg_val:3}  [{reg.to_32bit_val()}]")

    total_clk_cycles = sum(instruction.clkcyc for instruction in instructions)
    total_instructions = len(instructions)
    cpi = total_clk_cycles / total_instructions if total_instructions > 0 else 0
    print("\nCPI of the program..........\n")
    print("CPI =", cpi)

    clkcys_with_pipeline = len(instructions) + 3
    print("\nPipelined Execution of the program")
    print("=" * 38)
    print(f"{'':17}", end="")
    for x in range(1, clkcys_with_pipeline + 1):
        print(f"{x:5d}", end="")

    for instruction in instructions:
        if instruction.operand == "":
            print(
                f"\n{instruction.step + 1}. {instruction.opcode}{instruction.register.get_reg_adr()}{instruction.value:2}", end=" ")
        else:
            print(
                f"\n{instruction.step + 1}. {instruction.opcode}{instruction.register.get_reg_adr()}{instruction.operand}", end=" ")
        for _ in range(instruction.step + 1):
            print(" " * 5, end="")
        print("IF | ID | EX | WB", end="")

    print(
    f"\n\nThe program execution completed in {clkcys_with_pipeline} clock cycles under the pipeline")


if __name__ == "__main__":
    main()
