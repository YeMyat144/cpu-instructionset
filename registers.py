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
