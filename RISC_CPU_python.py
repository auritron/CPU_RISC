import json
import pandas

class System:

        def __init__(self) -> None:
                self.memory = Memory()
                self.instructions = Instructions(self.memory)
                self.alu = ALU(self.memory)
                self.executing = True
                self.interpreter = Interpreter(self.memory, self.instructions, self.executing)
                self.cpu = CPU(self.interpreter, self.instructions, self.alu, self.memory)
                
        def run(self):
                while True:
                        self.cpu.interpret()
                        self.cpu.execute()
                        self.memory.ins_stack.clear()

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
                        if len(self.memory.ins_stack) != 0 and self.memory.ins_stack[-1] == []:
                                self.memory.ins_stack.pop()
                        print(self.memory.ins_stack)
                print("OVER!")

        def execute(self):
                for ins in self.memory.ins_stack:
                        if ins[0] == 1:
                                self.instructions.load(ins[1],ins[3])
                        elif ins[0] == 2:
                                self.instructions.send(ins[3],ins[1])
                        elif ins[0] == 3:
                                self.instructions.copy(ins[1],ins[3])
                        elif ins[0] == 4:
                                self.instructions.set(ins[1],ins[3],ins[5])
                        elif ins[0] == 6:
                                self.alu.l_not(ins[1],ins[3])
                        elif ins[0] == 7:
                                self.alu.l_and(ins[1],ins[3],ins[5])
                        elif ins[0] == 8:
                                self.alu.l_or(ins[1],ins[3],ins[5])
                        elif ins[0] == 9:
                                self.alu.l_xor(ins[1],ins[3],ins[5])
                        elif ins[0] == 33:
                                self.instructions.to_int(ins[1],ins[3])

class Instructions:

        def __init__(self, memory) -> None:

                self.memory = memory

                #instructions list
                self.instructions = {
                        1:"LOAD",   #LOAD from RAM to Cache
                        2:"SEND",   #SEND from Cache to RAM
                        3:"COPY",   #COPY the data from Register to another in the Cache
                        4:"SET",    #SET VALUE of bit in a register to 0 or 1 
                        5:"SETR",   #SET Multiple VALUES in a range of bits in a single register to 0 or 1 (NOT IMPLMENTING)
                        6:"NOT",    #BITWISE NOT
                        7:"AND",    #BITWISE AND
                        8:"OR",     #BITWISE OR
                        9:"XOR",    #BITWISE XOR
                        10:"STL",   #SHIFT bits LEFT (NOT IMPLMENTING FOR SCHOOL)
                        11:"STR",   #SHIFT bits RIGHT (NOT IMPLMENTING FOR SCHOOL)
                        12:"RTL",   #ROTATE bits LEFT (NOT IMPLMENTING FOR SCHOOL)
                        13:"RTR",   #ROTATE bits RIGHT (NOT IMPLMENTING FOR SCHOOL)
                        14:"ADD",   #ADD the values of two Registers
                        15:"SUB",   #SUBTRACT the values of two Registers
                        16:"MUL",   #MULTIPLY the values of two Registers
                        17:"DIV",   #DIVIDE the values of two Registers and store quotient (NOT IMPLMENTING FOR SCHOOL)
                        18:"MOD",   #DIVIDE the values of two registers and store remainder (NOT IMPLMENTING FOR SCHOOL)
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
                                #^^^ NOT TO BE IMPLEMENTED FOR SCHOOL PROJECT ^^^
                        29:"END",   #TERMINATE program
                        30:"DISP",  #Display Cache Values
                        31:"CLRC",  #Clear the Cache(Set all values to 0)
                        32:"CLRR",  #Clear the RAM(Set all values to 0)
                        33:"TOINT"    #Convert register to integer    

                }

        #access RAM and move data
        def load(self, loc_mem: str, loc_cache: int) -> None:   #load from RAM to cache
                with open('RAM.json', 'r') as ram:
                        mem = json.load(ram)
                temp = mem[str(hexToAddress(loc_mem)[0])][str(hexToAddress(loc_mem)[1])]
                self.memory.cache[hexToAddress(loc_cache)[1]] = temp

        def send(self, loc_mem: int, loc_cache: int) -> None:   #save to RAM from cache
                with open('RAM.json', 'r') as ram:
                        mem = json.load(ram)
                temp = self.memory.cache[hexToAddress(loc_cache)[1]]
                mem[str(hexToAddress(loc_mem)[0])][str(hexToAddress(loc_mem)[1])] = temp
                with open('RAM.json' , 'w') as ram:
                        json.dump(mem, ram, indent = 4)

        def copy(self, locA: int , locB: int) -> None:
                temp = self.memory.cache[hexToAddress(locA)[1]]
                self.memory.cache[hexToAddress(locB)[1]] = temp

        def set(self, mem: int, pos:int, val: int) -> None:
                if pos < 15 or pos > 0:
                        if val in {0,1}:
                                self.memory.cache[hexToAddress(mem)[1]][pos] = val
                        else:
                                return None
                return None
        
        def to_int(self, mem: int, pos: int) -> None:
                binary_str = ''.join(str(bit) for bit in self.memory.cache[hexToAddress(mem)[1]])
                print(int(binary_str, 2))
                          
class ALU: 

        def __init__(self, memory) -> None:

                self.memory = memory

        #logic
        def l_not(self, mem: int, loc: int) -> None:
                i = 0
                while i < len(self.memory.cache[hexToAddress(mem)[1]]):
                        if self.memory.cache[hexToAddress(mem)[1]][i] == 0:
                                self.memory.cache[hexToAddress(loc)[1]][i] = 1
                        else:
                                self.memory.cache[hexToAddress(loc)[1]][i] = 0
                        i += 1

        def l_or(self, memA: int, memB: int, loc: int) -> None:
                i = 0
                while i < len(self.memory.cache[hexToAddress(memA)[1]]):
                        if self.memory.cache[hexToAddress(memA)[1]][i] == 0:
                                if self.memory.cache[hexToAddress(memB)[1]][i] == 0:
                                        self.memory.cache[hexToAddress(loc)[1]][i] = 0
                                else:
                                        self.memory.cache[hexToAddress(loc)[1]][i] = 1
                        else:
                                self.memory.cache[hexToAddress(loc)[1]][i] = 1
                        i += 1                                         

        def l_and(self, memA: int, memB: int, loc: int) -> None:
                i = 0
                while i < len(self.memory.cache[hexToAddress(memA)[1]]):
                        if self.memory.cache[hexToAddress(memA)[1]][i] == 0:
                                self.memory.cache[hexToAddress(loc)[1]][i] = 0
                        else:
                                if self.memory.cache[hexToAddress(memB)[1]][i] == 0:
                                        self.memory.cache[hexToAddress(loc)[1]][i] = 0
                                else:
                                        self.memory.cache[hexToAddress(loc)[1]][i] = 1
                        i += 1

        def l_xor(self, memA: int, memB: int, loc: int) -> None:
                i = 0
                while i < len(self.memory.cache[hexToAddress(memA)[1]]):
                        if self.memory.cache[hexToAddress(memA)[1]][i] == 0:
                                if self.memory.cache[hexToAddress(memB)[1]][i] == 0:
                                        self.memory.cache[hexToAddress(loc)[1]][i] = 0
                                else:
                                        self.memory.cache[hexToAddress(loc)[1]][i] = 1
                        else:
                                if self.memory.cache[hexToAddress(memB)[1]][i] == 0:
                                        self.memory.cache[hexToAddress(loc)[1]][i] = 1
                                else:
                                        self.memory.cache[hexToAddress(loc)[1]][i] = 0
                        i += 1

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
                        0:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        1:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        2:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        3:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        4:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        5:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        6:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        7:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        8:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        9:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        10:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        11:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        12:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        13:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        14:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        15:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
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
                                if self.token_stack[i] == "RUN":        #check for running
                                        self.executing = True
                                        break

                                elif self.token_stack[i] == "DISP":     #check to display values
                                        for key, val in self.memory.cache.items():
                                                print(f"{key}: {val}")
                                        break

                                elif self.token_stack[i] == "CLRR":     #reset RAM values to 0
                                        with open('Backup_RAM.json', 'r') as backup_ram:
                                                backup_data = json.load(backup_ram)
                                        with open('RAM.json', 'w') as ram:
                                                json.dump(backup_data, ram, indent=4)
                                        break

                                elif self.token_stack[i] in self.instructions.instructions.values():
                                        self.temp_ins.append(findKey(self.instructions.instructions, self.token_stack[i]))
                                        #print("Hallelujah!")
                                else:
                                        no_error = False
                                        #print("GET OUT")
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

                #print(self.memory.ins_stack)

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

                elif ins_key in {4,7,8,9,14,15,16,17,18}:         #type XXX R1 & R2 > R3
                        
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
                
                #elif ins_key == 4:                              #type XXX R1/bit1 = val
                        #return False

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
                #return [int(memAddress,16) // 8, int(memAddress,16) % 8]
                return [int(memAddress,16) // 16, int(memAddress,16) % 16]
        except ValueError:
                return None

system = System()
system.run()