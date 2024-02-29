class InstructionSet:
    def __init__(self, step, opcode, register, clkcyc, operand=""):
        self.step = step
        self.opcode = opcode
        self.register = register
        self.clkcyc = clkcyc
        self.value = int(register.get_reg_val()) 
        self.operand = operand

    def get_step(self):
        return self.step

    def get_opcode(self):
        return self.opcode

    def get_register(self):
        return self.register

    def get_clkcyc(self):
        return self.clkcyc

    def get_operand(self):
        return self.operand

    def get_value(self):
        return self.value

    def five_bit_opcode(self):
        opcode_map = {
            "mov": "00001",
            "add": "00010",
            "mul": "00100",
            "sub": "00011",
            "div": "00101"
        }
        return opcode_map.get(self.opcode, "end 0 0")

    def to_16_bit_val(self):
        if self.value >= 0:
            return format(self.value, '016b')
        else:
            return bin(self.value & 0b1111111111111111)[2:].zfill(16)

    def __str__(self):
        if self.operand == "":
            return f"[{self.step}] {self.opcode}{self.register.get_reg_adr():<5}{self.value:<4},  {self.five_bit_opcode():<5}{self.register.to_3_bit_adr():<7}{self.clkcyc:<5}"
        else:
            return f"[{self.step}] {self.opcode}{self.register.get_reg_adr():<5}{self.operand:<4},  {self.five_bit_opcode():<5}{self.register.to_3_bit_adr():<7}{self.to_16_bit_val():<22}{self.clkcyc}"


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

    def to_16_bit_val(self):
        if self.reg_val >= 0:
            return format(self.reg_val, '016b')
        else:
            return bin(self.reg_val & 0b1111111111111111)[2:].zfill(16)

    def to_3_bit_adr(self):
        adr_map = {
            "r0": "000",
            "r1": "001",
            "r2": "010",
            "r3": "011",
            "r4": "100",
            "r5": "101",
            "r6": "110",
            "r7": "111"
        }
        return adr_map.get(self.reg_adr, "")


if __name__ == "__main__":
    instruction = ""
    opcode = ""
    operand = ""
    operand2 = ""
    regs = [Registers(0, f"r{i}") for i in range(8)]
    steps = []
    step = 0

    print("Enter inputs(eg. mov r1 10/ stop with [end 0 0]) : ")

    while not (opcode == "end" and operand == "0" and operand2 == "0"):
        instruction = input()
        if instruction == "end 0 0":
            break
        else:
            input_list = instruction.split(" ")
            opcode = input_list[0]
            operand = input_list[1]
            operand2 = input_list[2]
            desti_reg = None
            for reg in regs:
                if reg.get_reg_adr() == operand:
                    desti_reg = reg
                    break
            try:
                value = int(operand2)
                if opcode == "mov":
                    desti_reg.set_reg_val(value)
                    steps.append(InstructionSet(step, opcode, desti_reg, 1))
                elif opcode == "add":
                    desti_reg.set_reg_val(desti_reg.get_reg_val() + value)
                    steps.append(InstructionSet(step, opcode, desti_reg, 2))
                elif opcode == "sub":
                    desti_reg.set_reg_val(desti_reg.get_reg_val() - value)
                    desti_reg.to_3_bit_adr()
                    steps.append(InstructionSet(step, opcode, desti_reg, 3))
                elif opcode == "mul":
                    desti_reg.set_reg_val(desti_reg.get_reg_val() * value)
                    steps.append(InstructionSet(step, opcode, desti_reg, 4))
                elif opcode == "div":
                    desti_reg.set_reg_val(desti_reg.get_reg_val() // value)
                    steps.append(InstructionSet(step, opcode, desti_reg, 4))
            except ValueError:
                source_reg = None
                for reg in regs:
                    if reg.get_reg_adr() == operand2:
                        source_reg = reg
                        break
                if opcode == "mov":
                    desti_reg.set_reg_val(source_reg.get_reg_val())
                    steps.append(InstructionSet(step, opcode, desti_reg, 1))
                elif opcode == "add":
                    desti_reg.set_reg_val(desti_reg.get_reg_val() + source_reg.get_reg_val())
                    steps.append(InstructionSet(step, opcode, desti_reg, 2))
                elif opcode == "sub":
                    desti_reg.set_reg_val(desti_reg.get_reg_val() - source_reg.get_reg_val())
                    desti_reg.to_3_bit_adr()
                    steps.append(InstructionSet(step, opcode, desti_reg, 3))
                elif opcode == "mul":
                    desti_reg.set_reg_val(desti_reg.get_reg_val() * source_reg.get_reg_val())
                    steps.append(InstructionSet(step, opcode, desti_reg, 4))
                elif opcode == "div":
                    desti_reg.set_reg_val(desti_reg.get_reg_val() / source_reg.get_reg_val())
                    steps.append(InstructionSet(step, opcode, desti_reg, 4))
        step += 1

    print("\n%-12s%-19s%-28s%s" % ("  PC ", "  Decoded: ", "  Encoded instruction: ", "   Clock Cycles\n"))
    for s in steps:
        print("%-12s%-4s%-5s%-10s%-6s%-4s%-28s%s" % ("PC[" + str(s.get_step()) + "]->", s.get_opcode(), s.get_register().get_reg_adr(),
                                                  s.get_value(), s.five_bit_opcode(), s.get_register().to_3_bit_adr(),
                                                  s.to_16_bit_val(), s.get_clkcyc()))
    
    print("\nAfter the program execution contents of the registers are..........\n")
    for s in steps:
        print(f"{s.get_register().get_reg_adr()} = {s.get_value()}   [{s.get_register().to_16_bit_val()}]")

    print("\nAfter the program execution values of the registers are..........\n")
    for reg in regs:
        print(f"{reg.get_reg_adr()}   {reg.get_reg_val()}  [{reg.to_16_bit_val()}]")

    total_clk_cycs = sum(s.get_clkcyc() for s in steps)
    cpi = total_clk_cycs / step if step else 0  
    print("") 
    print(f"Total clock cycles = {total_clk_cycs}, Step = {step}")
    print("CPI of the program..........")
    print("CPI =", cpi)

    clkcys_with_pipeline = len(steps) + 3
    print("\nPipelined Execution of the program")
    print("=" * 38)
    print("%17s" % "", end="")
    for x in range(1, clkcys_with_pipeline + 1):
        print("%5d" % x, end="")
    for s in steps:
        if s.get_operand() == "":
            print(f"\n{s.get_step() + 1}. {s.get_opcode()}{s.get_register().get_reg_adr()} {s.get_value()} :", end="")
        else:
            print(f"\n{s.get_step() + 1}. {s.get_opcode()}{s.get_register().get_reg_adr()}{s.get_operand()} :", end="")
        for y in range(s.get_step() + 1):
            print("%5s" % "", end="")
        print("IF | ID | EX | WB", end="")
    print(
    f"\n\nThe program execution completed in {clkcys_with_pipeline} clock cycles under the pipeline")

