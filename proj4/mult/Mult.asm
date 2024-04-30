// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

//// Replace this comment with your code.
// sum = 0
// count = r1
// i = 0
// while count > 0:
//     sum += r0
//     count--
//
// Example:
//     r0 = 2, r1 = 3
//     count = 3
//     sum = 0
//     iter 0: sum = 2, count = 2
//     iter 1: sum = 4, count = 1
//     iter 2: sum = 6, count = 0


@R2
M=0

@R1
D=M
@count
M=D

(LOOP)
@count
D=M
@END
D;JEQ
@R0
D=M
@R2
D=D+M
@R2
M=D
@count
M=M-1
@LOOP
0;JMP

(END)
@END
0;JMP

