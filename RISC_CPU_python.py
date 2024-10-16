import json

class System:

        def __init__(self) -> None:
                self.memory = Memory()
                self.instructions = Instructions()
                self.interpreter = Interpreter(self.memory, self.instructions)
                self.cpu = CPU(self.interpreter)
                
        def run(self):
                self.cpu.run()


class CPU:

        def __init__(self, interpreter) -> None:
                
                self.interpreter = interpreter

        def run(self):

                while True:
                        self.interpreter.tokenizer()
                        self.interpreter.error_handler()
                

class Instructions:

        def __init__(self) -> None:

                #instructions list
                self.instructions = {
                        1:"LOAD",   #LOAD from RAM to Cache
                        2:"SEND",   #SEND from Cache to RAM
                        3:"COPY",   #COPY the data from Register to another in the cache
                        4:"SET",    #SET VALUE of bit in a register to 0 or 1 
                        5:"SETR",   #SET Multiple VALUES in a range of bits in a single register to 0 or 1
                        6:"NOT",    #BITWISE NOT
                        7:"AND",    #BITWISE AND
                        8:"OR",     #BITWISE OR
                        9:"XOR",    #BITWISE XOR
                        10:"STL",   #SHIFT bits LEFT
                        11:"STR",   #SHIFT bits RIGHT
                        12:"RTL",   #ROTATE bits LEFT
                        13:"RTR",   #ROTATE bits RIGHT
                        14:"ADD",   #ADD the values of two Registers
                        15:"SUB",   #SUBTRACT the values of two Registers
                        16:"MUL",   #MULTIPLY the values of two Registers
                        17:"DIV",   #DIVIDE the values of two Registers and store quotient
                        18:"MOD",   #DIVIDE the values of two registers and store remainder
                        19:"CMP",   #COMPARE two registers
                        20:"GOTO",  #GO TO LABEL unconditionally
                        21:"WEQ",   #GO TO LABEL if f(Z) = 1
                        22:"WGT",   #GO TO LABEL if f(Z) = 0 and f(S) = 0
                        23:"WLT",   #GO TO LABEL if f(Z) = 0 and f(S) = 1
                        24:"WCY",   #GO TO LABEL if f(C) = 1
                        25:"WOV",   #GO TO LABEL if f(O) = 1
                        26:"WZD",   #GO TO LABEL if f(DZ) = 1
                        27:"CAL",   #GO TO LABEL unconditionally, and set save point
                        28:"RET",   #RETURN to save point set by CAL in the subroutine
                        29:"END"    #TERMINATE program

                }                  
class ALU:
        pass

class Memory:

        def __init__(self) -> None:

                self.cache = {
                        1:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        2:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        3:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        4:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        5:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        6:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        7:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        8:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                }

                self.temp_array = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

                self.flags = {
                        "Z":0,    #Zero Flag
                        "S":0,    #Negative Flag
                        "C":0,    #Carry Flag
                        "O":0,    #Overflow Flag
                        "DZ":0    #Zero Division Flag
                }

                self.call_stack = []
                self.ins_stack = [[]]

class Interpreter:      #Interprets, tokenizes and error handles user input

        def __init__(self, memory, instructions) -> None:
                
                self.ins_stack_count = 1
                self.memory = memory
                self.instructions = instructions
                self.token_stack = []     #token stack

        def tokenizer(self):    #tokenize input into token stack
                
                self.token_stack.clear()
                cmd = input("> ")
                tknstr = ""

                for char in cmd:
                        if char == " ":
                                if tknstr:
                                        self.token_stack.append(tknstr)
                                        tknstr = ""
                        else:
                                tknstr += char

                if tknstr:
                        self.token_stack.append(tknstr)

        def error_handler(self):

                i = 0
                new_ins = True
                while i < len(self.token_stack):
                        if i == 0:
                                if self.token_stack[i] in self.instructions.instructions.values():
                                        self.memory.ins_stack[len(self.memory.ins_stack)-1].append(find_key(self.instructions.instructions, self.token_stack[i]))
                                        print("Hallelujah!")
                                else:
                                        new_ins = False
                                        print("bepis")
                                        break

                        else:
                                if self.chk_error(i):
                                        print("yes", end=' ')
                                else:
                                        print("nom", end=' ')
                                print()
                                self.memory.ins_stack[len(self.memory.ins_stack)-1].append(self.token_stack[i])

                        i += 1

                if new_ins:
                        self.memory.ins_stack.append([])

                print(self.memory.ins_stack)        

        def chk_error(self, index) -> bool:

                ins_stk_ref = self.memory.ins_stack
                ins_key = self.memory.ins_stack[-1][0]

                if ins_key in {1,2,3,6}:                        #type XXX R1 > R2
                        if len(ins_stk_ref) == 4:
                                if index in {1,3}:
                                        if tkn_type(ins_stk_ref[index]) == 1:
                                                return True
                                elif index == 2:
                                        if tkn_type(ins_stk_ref[index]) == 2:
                                                return True
                        return False

                elif ins_key in {7,8,9,14,15,16,17,18}:         #type XXX R1 & R2 > R3
                        if len(ins_stk_ref) == 6:
                                if tkn_type(ins_stk_ref[1]) == tkn_type(ins_stk_ref[3]) == tkn_type(ins_stk_ref[5]) == 1 and tkn_type(ins_stk_ref[2]) == 3 and tkn_type(ins_stk_ref[4]) == 2:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                elif ins_key in {10,11,12,13}:                  #type XXX R1 & %(n)
                        if len(ins_stk_ref) == 4:
                                if tkn_type(ins_stk_ref[1]) == 1 and tkn_type(ins_stk_ref[2]) == 3 and tkn_type(ins_stk_ref[3]) == 4:
                                        return True
                                else:
                                        return False
                        else:
                                return False

                elif ins_key in {20,21,22,23,24,25,26,27,28}:   #type XXX @LABEL
                        return False
                
                elif ins_key == 4:                              #type XXX R1/bit1
                        return False

                elif ins_key == 5:                              #type XXX R1/bit2
                        return False

                elif ins_key == 19:                             #type XXX R1 & R2
                        return False

                else:                                           #error
                        return False

                

#other methods               
def find_key(dict, val): #find key value from dict

        for key, value in dict.items():
                if value == val:
                        return key
        return None

def tkn_type(token) -> int: #assign value to token type - 1 for register, 2 for '>', 3 for '&', 4 for '%', 5 for '@', 0 for none
        if len(token) == 8 and token[0:2] == '0x':
                return 1
        elif token == '>':
                return 2
        elif token == '&':
                return 3
        elif token[0] == '%':
                return 4
        elif token[0] == '@':
                return 5
        else:
                return 0

system = System()
system.run()