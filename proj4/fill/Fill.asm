// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.

// while 1
//     if (key pressed)
//          fill_screen()
//     else
//          blank_screen()

@8192
D=A
@count
M=D

@i
M=0

(MAIN_LOOP)
@KBD
D=M
@FILL
D;JNE

// Fill white
@i
M=0

(INNER_FW_LOOP)
@i
D=M
@SCREEN
A=A+D
M=0
@i
M=M+1
@i
D=M
@count
D=D-M
@MAIN_LOOP
D;JEQ
@INNER_FW_LOOP
0;JMP

// Fill black
(FILL)
@i
M=0

(INNER_FB_LOOP)
@i
D=M
@SCREEN
A=A+D
M=-1
@i
M=M+1
@i
D=M
@count
D=D-M
@MAIN_LOOP
D;JEQ
@INNER_FB_LOOP
0;JMP

