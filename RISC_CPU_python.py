import json

class System:

class CPU:

        def __init__(self) -> None:
                
                self.interpreter = Interpreter()

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

                self.call_stack = {}
                self.ins_stack = {}

class Interpreter:      #Interprets, tokenizes and error handles user input

        def __init__(self) -> None:
                
                self.intp_memory = Memory()
                self.intp_instructions = Instructions()
                self.token_stack = []     #token stack

        def tokenizer(self):

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
                ins_key = 0
                for i in self.token_stack:
                        if i == 0:
                                if self.token_stack[i] in self.intp_instructions.instructions.values():
                                        
                                        print("Hallelujah!")
                                else:
                                        print("haydeen moment")
                                        break
                        else:

cpu = CPU()
cpu.run()