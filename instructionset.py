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
