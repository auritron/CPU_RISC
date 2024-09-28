import json

instructions = {1:"LOAD",   #LOAD from RAM to Cache
                2:"SEND",   #SEND from Cache to RAM
                3:"SWAP",   #SWAP the data in two Registers
                4:"ADD",    #ADD the values of two Registers
                5:"SUB",    #SUBTRACT the values of two Registers
                6:"MUL",    #MULTIPLY the values of two Registers
                7:"DIV",    #DIVIDE the values of two Registers
                8:"NOT",    #BITWISE NOT
                9:"AND",    #BITWISE AND
                10:"OR",    #BITWISE OR
                11:"XOR",   #BITWISE XOR
                12:"SET",   #SET VALUE of bit in a register to 0 or 1 
                13:"SETR",  #SET Multiple VALUES in a range of bits in a single register to 0 or 1
                14:"STL",   #SHIFT bits LEFT
                15:"STR",   #SHIFT bits RIGHT
                16:"RTL",   #ROTATE bits LEFT
                17:"RTR"    #ROTATE bist RIGHT
                } 

cache = {
        1:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        2:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        3:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        4:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        5:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        6:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        7:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        8:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        }

flags = {
        "zero":0,  #Zero Flag
        "ngtve":0, #Negative flag
        "carry":0, #Carry flag
        "ovflw":0  #Overflow Flag
        }