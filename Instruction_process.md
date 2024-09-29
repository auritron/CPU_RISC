Instructions -
('-' represents a bullet point, '>' represents pseudocode)

1. LOAD - (LOAD R1 > R2 ; R1 is in RAM and R2 is in Cache)
> Locate memory address from RAM(from function)
> Copy into temp array
> Copy temp array into respective cache address
> Reset temp array

2. SEND - (SEND R2 > R1 ; R1 is in RAM and R2 is in Cache)
> Locate memory address in cache(from function)
> Copy into temp array
> Copy temp array into respective RAM address
> Reset temp array

3. COPY - (COPY R1 > R2 ; Copy from R1 to R2)
> Locate memory address 1
> Copy into temp array
> Copy temp array into memory address 2
> Reset temp array

4. SET - (SET R1/bit1 = (0 or 1) ; Set 'bit1' in R1 as 0 or 1)
> Locate memory address 1
> Locate bit in memory address 1
> Set bit to 0 or 1 as specified by user(from function)

5. SETR - (SETR R1/bit1,bit2 = (0 or 1) ; Set all bits in range bit1 to bit2 (inclusive) as 0 or 1)
> Locate memory address 1
> Locate bits 1 and 2 in memory address
> Using slice assignment, set all bits between 1 and 2 to 0

6. NOT - (NOT R1 > R2 ; Sets R2 as bitwise NOT of R1)
> Locate memory address 1
> Perform NOT on each individual bit(NOT 0 = 1 , NOT 1 = 0)
> Result is in temp array
> Copy temp array to memory address 2

7. AND - (AND R1 & R2 > R3; Sets R3 as bitwise AND of R1 and R2)
> Locate memory address 1 and 2
> Perform AND on each individual bit between the two(0 AND 0 = 0 , 0 AND 1 = 0, 1 AND 0 = 0 , 1 AND 1 = 1)
> Result is in temp array
> Copy temp array to memory address 3

8. OR - (OR R1 & R2 > R3; Sets R3 as bitwise OR of R1 and R2)
> Locate memory address 1 and 2
> Perform AND on each individual bit between the two(0 OR 0 = 0 , 0 OR 1 = 1, 1 OR 0 = 1 , 1 OR 1 = 1)
> Result is in temp array
> Copy temp array to memory address 3

9. XOR - (XOR R1 & R2 > R3; Sets R3 as bitwise XOR of R1 and R2)
> Locate memory address 1 and 2
> Perform AND on each individual bit between the two(0 XOR 0 = 0 , 0 XOR 1 = 1, 1 XOR 0 = 1 , 1 XOR 1 = 0)
> Result is in temp array
> Copy temp array to memory address 3

4. ADD - (ADD R1 & R2 > R3 ; Add R1 and R2 into R3)
> Locate memory address 1 and 2
> If value is immediate value, convert to binary
> Use arithmetic rules to find binary sum (0+0 = 0, 1+0 = 1, 0+1 = 1, 1+1 = 10)
> If MSB is 10, set MSB to 0 and carry flag to 1. Else, set it to 0.
> Store sum in temp array
> Copy temp array into memory address 3

5. SUB - (SUB R1 & R2 > R3 ; Subtract R2 from R1 into R3)
> Locate memory address 1 and 2
> If value is immediate value, convert to binary
> Use arithmetic rules to find binary difference (0-0 = 0, 1-0 = 1, 1-1 = 0, 0-1 = 1 with 1 borrow)
> If a borrow unit is required for the MSB, set carry flag to 1. Else, set it to 0.
> Store difference in temp array
> Copy temp array into memory address 3

6. MUL - (MUL R1 & R2 > R3 ; Multiply R1 and R2 into R3)
