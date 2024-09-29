import json

class CPU:
        pass

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
                        17:"DIV",   #DIVIDE the values of two Registers
                        18:"CMP",   #COMPARE two registers
                        19:"GOTO",  #GO TO LABEL unconditionally
                        20:"WEQ",   #GO TO LABEL if f(Z) = 1
                        21:"WGT",   #GO TO LABEl if f(Z) = 0 and f(S) = 0
                        22:"WLT"
                }                  

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

                self.flags = {
                        "Z":0, #Zero Flag
                        "S":0, #Negative flag
                        "C":0, #Carry flag
                        "O":0  #Overflow Flag
                }
