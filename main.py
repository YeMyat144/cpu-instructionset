from instructionset import InstructionSet
from registers import Registers

def main():
    regs = [Registers(0, f"r{i}") for i in range(8)]
    steps = []
    step = 0

    print("Enter inputs(eg. mov r1 10/ stop with [end 0 0]) : ")

    while True:
        instruction = input()
        if instruction == "end 0 0":
            break

        input_list = instruction.split(" ")
        opcode, operand, operand2 = input_list[0], input_list[1], input_list[2]
        desti_reg = next((reg for reg in regs if reg.get_reg_adr() == operand), None)

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
                steps.append(InstructionSet(step, opcode, desti_reg, 3))
            elif opcode == "mul":
                desti_reg.set_reg_val(desti_reg.get_reg_val() * value)
                steps.append(InstructionSet(step, opcode, desti_reg, 4))
            elif opcode == "div":
                desti_reg.set_reg_val(desti_reg.get_reg_val() // value)
                steps.append(InstructionSet(step, opcode, desti_reg, 4))
        except ValueError:
            source_reg = next((reg for reg in regs if reg.get_reg_adr() == operand2), None)
            if opcode == "mov":
                desti_reg.set_reg_val(source_reg.get_reg_val())
                steps.append(InstructionSet(step, opcode, desti_reg, 1))
            elif opcode == "add":
                desti_reg.set_reg_val(desti_reg.get_reg_val() + source_reg.get_reg_val())
                steps.append(InstructionSet(step, opcode, desti_reg, 2))
            elif opcode == "sub":
                desti_reg.set_reg_val(desti_reg.get_reg_val() - source_reg.get_reg_val())
                steps.append(InstructionSet(step, opcode, desti_reg, 3))
            elif opcode == "mul":
                desti_reg.set_reg_val(desti_reg.get_reg_val() * source_reg.get_reg_val())
                steps.append(InstructionSet(step, opcode, desti_reg, 4))
            elif opcode == "div":
                desti_reg.set_reg_val(desti_reg.get_reg_val() // source_reg.get_reg_val())
                steps.append(InstructionSet(step, opcode, desti_reg, 4))
        step += 1

    display_results(steps, regs, step)

def display_results(steps, regs, step):
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

main()
