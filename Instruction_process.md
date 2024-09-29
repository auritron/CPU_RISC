Instructions -
('>' represents a bullet point, '-' represents pseudocode)

1. LOAD -
> Locate memory address from RAM(from function)
> Copy into temp array
> Copy temp array into respective cache address
> Reset temp array

2. SEND -
> Locate memory address in cache(from function)
> Copy into temp array
> Copy temp array into respective RAM address
> Reset temp array

3. COPY -
> Locate memory address 1
> Copy into temp array
> Copy temp array into memory address 2
> Reset temp array

4. ADD -
> Locate memory address 1 and 2
> If value is immediate value, convert to binary
> Use arithmetic rules to find binary sum (0+0 = 0, 1+0 = 1, 0+1 = 1, 1+1 = 10)
> If sum doesn't fit, set carry flag to 1. Else, set it to 0.
> Store sum in temp array
> Copy temp array into memory address 3

5. SUB -
> Locate