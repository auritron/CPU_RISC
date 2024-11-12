import json

class System:

        def __init__(self) -> None:
                self.memory = Memory()
                self.instructions = Instructions()
                self.alu = ALU()
                self.executing = True
                self.interpreter = Interpreter(self.memory, self.instructions, self.executing)
                self.cpu = CPU(self.interpreter, self.instructions, self.alu, self.memory)
                
        def run(self):
                self.cpu.interpret()

class CPU:

        def __init__(self, interpreter, instructions, alu, memory) -> None:
                
                self.interpreter = interpreter
                self.instructions = instructions
                self.memory = memory
                self.alu = alu

        def interpret(self):

                self.interpreter.executing = False
                while not self.interpreter.executing:
                        self.interpreter.tokenizer()
                        self.interpreter.errorHandler()
                print("ITS JOEVER!")

        def execute(self):
                for ins in self.memory.ins_stack:
                        if ins[0] == 1:
                                self.instructions.load(hexToAddress(ins[1])[0]) #INCOMPLETE                     

class Instructions:

        def __init__(self) -> None:

                #instructions list
                self.instructions = {
                        1:"LOAD",   #LOAD from RAM to Cache
                        2:"SEND",   #SEND from Cache to RAM
                        3:"COPY",   #COPY the data from Register to another in the cache
                        4:"SET",    #SET VALUE of bit in a register to 0 or 1 
                        5:"SETR",   #SET Multiple VALUES in a range of bits in a single register to 0 or 1 (NOT IMPLMENTING)
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
                                #vvv NOT TO BE IMPLEMENTED FOR SCHOOL PROJECT vvv
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
                        29:"END"   #TERMINATE program

                }

        #access RAM and move data
        def load(self, loc_mem: str, loc_cache: int) -> None:   #load from RAM to cache
                with open('RAM.json') as ram:
                        mem = json.load(ram)
                
                #print(mem["0"]["8"])

        def send(self, loc_mem: int, loc_cache: int) -> None:
                pass

        def copy(self, locA: int , locB: int) -> None:
                pass

        def set(self, mem: int, val: int) -> None:
                pass

                          
class ALU: 

        #logic
        def l_not(self, mem: int, loc: int) -> None:
                pass

        def l_or(self, memA: int, memB: int, loc: int) -> None:
                pass

        def l_and(self, memA: int, memB: int, loc: int) -> None:
                pass

        def l_xor(self, memA: int, memB: int, loc: int) -> None:
                pass

        def a_add(self, memA: int, memB: int, loc: int) -> None:
                pass

        def a_sub(self, memA: int, memB: int, loc: int) -> None:
                pass

        def a_mul(self, memA: int, memB: int, loc: int) -> None:
                pass

        def a_div(self, memA: int, memB: int, loc: int, mod: bool) -> None:
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

        def errorHandler(self):

                i = 0
                no_error = True
                while i < len(self.token_stack):
                        if i == 0:
                                if self.token_stack[i] == "RUN":
                                        self.executing = True
                                        break
                                elif self.token_stack[i] in self.instructions.instructions.values():
                                        self.temp_ins.append(findKey(self.instructions.instructions, self.token_stack[i]))
                                        #print("Hallelujah!")
                                else:
                                        no_error = False
                                        #print("bepis")
                                        break

                        else:
                                if self.chkError(i):
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

        def chkError(self, index) -> bool:     #return True if no error, return False if there is

                ins_key = self.temp_ins[0]

                if ins_key in {1,2,3,6}:                        #type XXX R1 > R2
                        if len(self.token_stack) == 4:
                                if index in {1,3}:
                                        if tknType(self.token_stack[index]) == 1:
                                                return True
                                elif index == 2:
                                        if tknType(self.token_stack[index]) == 2:
                                                return True
                        return False

                elif ins_key in {7,8,9,14,15,16,17,18}:         #type XXX R1 & R2 > R3
                        
                        if len(self.token_stack) == 6:
                                if index in {1,3,5}:
                                        if tknType(self.token_stack[index]) == 1:
                                                return True
                                elif index == 2:
                                        if tknType(self.token_stack[index]) == 3:
                                                return True
                                elif index == 4:
                                        if tknType(self.token_stack[index]) == 2:
                                                return True
                        return False

                elif ins_key in {10,11,12,13}:                  #type XXX R1 & %(n)

                        if len(self.token_stack) == 4:
                                if index == 1:
                                        if tknType(self.token_stack[index]) == 1:
                                                return True
                                elif index == 2:
                                        if tknType(self.token_stack[index]) == 3:
                                                return True
                                elif index == 3:
                                        if tknType(self.token_stack[index]) == 4:
                                                return True
                        return False

                elif ins_key in {20,21,22,23,24,25,26,27,28}:   #type XXX @LABEL

                        if len(self.token_stack) == 2:
                                if index == 1:
                                        if tknType(self.token_stack[index]) == 5:
                                                return True
                        return False
                
                elif ins_key == 4:                              #type XXX R1/bit1
                        return False

                elif ins_key == 5:                              #type XXX R1/bit,bit2
                        return False

                elif ins_key == 19:                             #type XXX R1 & R2
                        if len(self.token_stack) == 4:
                                if index in {1,3}:
                                        if tknType(self.token_stack[index]) == 1:
                                                return True
                                elif index == 2:
                                        if tknType(self.token_stack[index]) == 3:
                                                return True
                        return False     

                else:                                           #error
                        return False

                

#other methods               
def findKey(dict, val) -> int: #find key value from dict

        for key, value in dict.items():
                if value == val:
                        return key
        return None

def tknType(token) -> int: #assign value to token type - 1 for register, 2 for '>', 3 for '&', 4 for '%', 5 for '@', 0 for none
        if len(token) == 6 and token[0:2] == '0x':
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
        
#convert hex code address to int, subAddress represents if it refers to the inner or outer array in RAM
def hexToAddress(memAddress: str) -> list[int]:
        try:
                return [int(memAddress,16) // 8, int(memAddress,16) % 8]
        except ValueError:
                return None

system = System()
system.run()