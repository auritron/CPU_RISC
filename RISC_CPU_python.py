import json

class System:

        def __init__(self) -> None:
                self.memory = Memory()
                self.instructions = Instructions()
                self.executing = False
                self.interpreter = Interpreter(self.memory, self.instructions, self.executing)
                self.cpu = CPU(self.interpreter)
                
        def run(self):
                self.cpu.run()


class CPU:

        def __init__(self, interpreter) -> None:
                
                self.interpreter = interpreter

        def run(self):

                self.interpreter.executing = True
                while self.interpreter.executing:
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
                        29:"END",   #TERMINATE program
                        30:"RUN"    #RUN program

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
                self.ins_stack = []

class Interpreter:      #Interprets, tokenizes and error handles user input

        def __init__(self, memory, instructions, executing) -> None:
                
                self.ins_stack_count = 1
                self.memory = memory
                self.instructions = instructions
                self.executing = executing
                self.token_stack = []     #token stack
                self.temp_ins = []

        def tokenizer(self):    #tokenize input into token stack
                
                self.temp_ins.clear()
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
                no_error = True
                while i < len(self.token_stack):
                        if i == 0:
                                if self.token_stack[i] in self.instructions.instructions.values():
                                        self.temp_ins.append(find_key(self.instructions.instructions, self.token_stack[i]))
                                        #print("Hallelujah!")
                                        #check
                                else:
                                        no_error = False
                                        #print("bepis")
                                        break

                        else:
                                if self.chk_error(i):
                                        self.temp_ins.append(self.token_stack[i])
                                        #print("yes")
                                else:
                                        no_error = False
                                        #print("nom")
                                        break

                        i += 1

                if no_error:
                        self.memory.ins_stack.append(self.temp_ins[:])  #append copy of temp_ins to ins_stack

                print(self.memory.ins_stack)        

        def chk_error(self, index) -> bool:     #return True if no error, return False if there is

                ins_key = self.temp_ins[0]

                if ins_key in {1,2,3,6}:                        #type XXX R1 > R2
                        if len(self.token_stack) == 4:
                                if index in {1,3}:
                                        if tkn_type(self.token_stack[index]) == 1:
                                                return True
                                elif index == 2:
                                        if tkn_type(self.token_stack[index]) == 2:
                                                return True
                        return False

                elif ins_key in {7,8,9,14,15,16,17,18}:         #type XXX R1 & R2 > R3
                        
                        if len(self.token_stack) == 6:
                                if index in {1,3,5}:
                                        if tkn_type(self.token_stack[index]) == 1:
                                                return True
                                elif index == 2:
                                        if tkn_type(self.token_stack[index]) == 3:
                                                return True
                                elif index == 4:
                                        if tkn_type(self.token_stack[index]) == 2:
                                                return True
                        return False

                elif ins_key in {10,11,12,13}:                  #type XXX R1 & %(n)

                        if len(self.token_stack) == 4:
                                if index == 1:
                                        if tkn_type(self.token_stack[index]) == 1:
                                                return True
                                elif index == 2:
                                        if tkn_type(self.token_stack[index]) == 3:
                                                return True
                                elif index == 3:
                                        if tkn_type(self.token_stack[index]) == 4:
                                                return True
                        return False

                elif ins_key in {20,21,22,23,24,25,26,27,28}:   #type XXX @LABEL

                        if len(self.token_stack) == 2:
                                if index == 1:
                                        if tkn_type(self.token_stack[index]) == 5:
                                                return True
                        return False
                
                elif ins_key == 4:                              #type XXX R1/bit1
                        return False

                elif ins_key == 5:                              #type XXX R1/bit,bit2
                        return False

                elif ins_key == 19:                             #type XXX R1 & R2
                        if len(self.token_stack) == 4:
                                if index in {1,3}:
                                        if tkn_type(self.token_stack[index]) == 1:
                                                return True
                                elif index == 2:
                                        if tkn_type(self.token_stack[index]) == 3:
                                                return True
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