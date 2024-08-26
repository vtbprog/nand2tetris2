#!/usr/bin/python

from vm_translator_constants import CommandType
import vm_parser
import os

class CodeWriter:
    asm_file = None
    asm_fd = None
    eq_index = 0
    gt_index = 0
    lt_index = 0

    def __init__(self, asm_file):
        print("Hello from Code Writer!")
        print("ASM file path is ", asm_file)
        CodeWriter.asm_file = asm_file
        CodeWriter.asm_fd = open(asm_file, 'w')
        CodeWriter.eq_index = 0
        CodeWriter.gt_index = 0
        CodeWriter.lt_index = 0

    def __del__(self):
        print("Closing asm file ", CodeWriter.asm_file)
        CodeWriter.asm_fd.close()

    @staticmethod
    def process_push_constant(arg):
        """
        pseudocode:

        *SP=arg
        SP++
        """
        file = CodeWriter.asm_fd
        file.write("// push constant " + arg + "\n")
        file.write("@" + arg + "\n")
        file.write("D=A\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("M=D\n")
        file.write("@SP\n")
        file.write("M=M+1\n")

    @staticmethod
    def process_push_norm_mem_seg(arg1, arg2):
        """
        pseudocode:

        addr = segmentptr + i
        *SP = *addr
        SP++
        """
        file = CodeWriter.asm_fd
        file.write("// push "+ arg1 + " "  + arg2 + "\n")
        file.write("@" + arg2 + "\n");
        file.write("D=A\n")
        if arg1 == "local":
            file.write("@LCL\n")
        elif arg1 == "argument":
            file.write("@ARG\n")
        elif arg1 == "this":
            file.write("@THIS\n")
        elif arg1 == "that":
            file.write("@THAT\n")
        else:
            print("Received invalid memory segment. Please check implementation!")
            assert(False)
        file.write("A=M+D\n")
        file.write("D=M\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("M=D\n")
        file.write("@SP\n")
        file.write("M=M+1\n")

    @staticmethod
    def process_push_temp(arg):
        """
        pseudocode:

        addr = 5 + i
        *SP = *addr
        SP++
        """
        file = CodeWriter.asm_fd
        file.write("// push temp " + arg + "\n")
        file.write("@" + arg + "\n");
        file.write("D=A\n")
        file.write("@5\n")
        file.write("D=D+A\n")
        file.write("A=D\n")
        file.write("D=M\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("M=D\n")
        file.write("@SP\n")
        file.write("M=M+1\n")

    @staticmethod
    def process_push_static(arg):
        """
        pseudocode:

        D = variable with name "Foo.arg" where Foo is name of file
        *SP = D
        SP++
        """
        file = CodeWriter.asm_fd
        file.write("// push static " + arg + "\n")
        name = os.path.basename(CodeWriter.asm_file).split('.')[0]
        file.write("@" + name + "." + arg + "\n");
        file.write("D=M\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("M=D\n")
        file.write("@SP\n")
        file.write("M=M+1\n")

    @staticmethod
    def process_push_pointer(arg):
        """
        pseudocode:

        *SP = THIS/THAT
        SP++
        """
        file = CodeWriter.asm_fd
        file.write("// push pointer " + arg + "\n")
        if arg == "0":
            file.write("@THIS\n")
        elif arg == "1":
            file.write("@THAT\n")
        else:
            print("Invalid pointer arg\n")
            assert(False)
        file.write("D=M\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("M=D\n")
        file.write("@SP\n")
        file.write("M=M+1\n")

    @staticmethod
    def process_pop_norm_mem_seg(arg1, arg2):
        """
        pseudocode:

        addr = segmentptr + i
        SP--
        *addr = *SP
        """
        file = CodeWriter.asm_fd
        file.write("// pop "+ arg1 + " "  + arg2 + "\n")

        file.write("@" + arg2 + "\n");
        file.write("D=A\n")
        if arg1 == "local":
            file.write("@LCL\n")
        elif arg1 == "argument":
            file.write("@ARG\n")
        elif arg1 == "this":
            file.write("@THIS\n")
        elif arg1 == "that":
            file.write("@THAT\n")
        else:
            print("Received invalid memory segment. Please check implementation!")
            assert(False)
        file.write("A=M+D\n")
        file.write("D=A\n")
        file.write("@13\n")
        file.write("M=D\n")
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("A=M\n")
        file.write("D=M\n")
        file.write("@13\n")
        file.write("A=M\n")
        file.write("M=D\n")

    @staticmethod
    def process_pop_temp(arg):
        """
        pseudocode:

        addr = 5 + i
        SP--
        *addr = *SP
        """
        file = CodeWriter.asm_fd
        file.write("// pop temp " + arg + "\n")
        file.write("@" + arg + "\n");
        file.write("D=A\n")
        file.write("@5\n")
        file.write("D=D+A\n")
        file.write("@13\n")
        file.write("M=D\n")
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("A=M\n")
        file.write("D=M\n")
        file.write("@13\n")
        file.write("A=M\n")
        file.write("M=D\n")

    @staticmethod
    def process_pop_static(arg):
        """
        pseudocode:

        SP--
        D=*SP
        variable with name "Foo.arg" where Foo is name of file = D
        """
        file = CodeWriter.asm_fd
        file.write("// pop static " + arg + "\n")
        name = os.path.basename(CodeWriter.asm_file).split('.')[0]
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("A=M\n")
        file.write("D=M\n")
        file.write("@" + name + "." + arg + "\n");
        file.write("M=D\n")

    @staticmethod
    def process_pop_pointer(arg):
        """
        pseudocode:

        SP--
        THIS/THAT = *SP
        """
        file = CodeWriter.asm_fd
        file.write("// pop pointer " + arg + "\n")
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("A=M\n")
        file.write("D=M\n")

        if arg == "0":
            file.write("@THIS\n")
        elif arg == "1":
            file.write("@THAT\n")
        else:
            print("Invalid pointer arg\n")
            assert(False)
        file.write("M=D\n")

    @staticmethod
    def process_push(arg1, arg2):
        if arg1 == "constant":
            CodeWriter.process_push_constant(arg2)
        elif arg1 == "local" or arg1 == "argument" or arg1 == "this" or arg1 == "that":
            CodeWriter.process_push_norm_mem_seg(arg1, arg2)
        elif arg1 == "temp":
            CodeWriter.process_push_temp(arg2)
        elif arg1 == "static":
            CodeWriter.process_push_static(arg2)
        elif arg1 == "pointer":
            CodeWriter.process_push_pointer(arg2)
        else:
            print("Invalid push command\n")
            assert(False)

    @staticmethod
    def process_pop(arg1, arg2):
        if arg1 == "constant":
            print("Received invalid pop constant command")
            assert(False)
        elif arg1 == "local" or arg1 == "argument" or arg1 == "this" or arg1 == "that":
            CodeWriter.process_pop_norm_mem_seg(arg1, arg2)
        elif arg1 == "temp":
            CodeWriter.process_pop_temp(arg2)
        elif arg1 == "static":
            CodeWriter.process_pop_static(arg2)
        elif arg1 == "pointer":
            CodeWriter.process_pop_pointer(arg2)
        else:
            print("Invalid pop command\n")
            assert(False)

    @staticmethod
    def process_add():
        """
        pseudocode:

        SP--
        a=*SP
        SP--
        b=*SP
        c=a+b
        *SP=c
        SP++
        """
        file = CodeWriter.asm_fd
        file.write("// add\n")
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("D=M\n")
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("D=D+M\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("M=D\n")
        file.write("@SP\n")
        file.write("M=M+1\n")


    @staticmethod
    def process_sub():
        """
        pseudocode:
        sp--
        a=*sp
        sp--
        b=*sp
        a=b-a
        *sp=a
        sp++
        """
        file = CodeWriter.asm_fd
        file.write("// sub\n")
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("D=M\n")
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("D=M-D\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("M=D\n")
        file.write("@SP\n")
        file.write("M=M+1\n")


    @staticmethod
    def process_eq():
        """
        pseudocode:
        sp--
        a=*sp
        sp--
        b=*sp
        a=(a==b)
        *sp=a
        sp++
        """
        file = CodeWriter.asm_fd
        file.write("// eq\n")
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("D=M\n")
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("D=D-M\n")
        file.write("@EQ_"+ str(CodeWriter.eq_index) + "\n")
        file.write("D;JEQ\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("M=0\n")
        file.write("@ENDEQ_" + str(CodeWriter.eq_index) + "\n")
        file.write("0;JMP\n")
        file.write("(EQ_" + str(CodeWriter.eq_index) + ")\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("M=-1\n")
        file.write("(ENDEQ_"+ str(CodeWriter.eq_index) + ")\n")
        file.write("@SP\n")
        file.write("M=M+1\n")

        CodeWriter.eq_index += 1

    @staticmethod
    def process_gt():
        """
        pseudocode:
        sp--
        a=*sp
        sp--
        b=*sp
        a=(b>a)
        *sp=a
        sp++
        """
        file = CodeWriter.asm_fd
        file.write("// gt\n")
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("D=M\n")
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("D=M-D\n")
        file.write("@GT_"+ str(CodeWriter.gt_index) + "\n")
        file.write("D;JGT\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("M=0\n")
        file.write("@ENDGT_" + str(CodeWriter.gt_index) + "\n")
        file.write("0;JMP\n")
        file.write("(GT_" + str(CodeWriter.gt_index) + ")\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("M=-1\n")
        file.write("(ENDGT_"+ str(CodeWriter.gt_index) + ")\n")
        file.write("@SP\n")
        file.write("M=M+1\n")

        CodeWriter.gt_index += 1

    @staticmethod
    def process_lt():
        """
        pseudocode:
        sp--
        a=*sp
        sp--
        b=*sp
        a=(b<a)
        *sp=a
        sp++
        """
        file = CodeWriter.asm_fd
        file.write("// lt\n")
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("D=M\n")
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("D=D-M\n")
        file.write("@LT_"+ str(CodeWriter.lt_index) + "\n")
        file.write("D;JGT\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("M=0\n")
        file.write("@ENDLT_" + str(CodeWriter.lt_index) + "\n")
        file.write("0;JMP\n")
        file.write("(LT_" + str(CodeWriter.lt_index) + ")\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("M=-1\n")
        file.write("(ENDLT_"+ str(CodeWriter.lt_index) + ")\n")
        file.write("@SP\n")
        file.write("M=M+1\n")

        CodeWriter.lt_index += 1

        pass

    @staticmethod
    def process_not():
        """
        pseudocode:

        sp--
        a=*sp
        a=!a
        *sp=a
        sp++
        """
        file = CodeWriter.asm_fd
        file.write("// not\n")
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("D=M\n")
        file.write("D=!D\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("M=D\n")
        file.write("@SP\n")
        file.write("M=M+1\n")

    @staticmethod
    def process_and():
        """
        pseudocode:

        sp--
        a=*sp
        sp--
        b=*sp
        a=a&b
        *sp=a
        sp++
        """
        file = CodeWriter.asm_fd
        file.write("// and\n")
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("D=M\n")
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("D=D&M\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("M=D\n")
        file.write("@SP\n")
        file.write("M=M+1\n")

    @staticmethod
    def process_or():
        """
        pseudocode:

        sp--
        a=*sp
        sp--
        b=*sp
        a=a|b
        *sp=a
        sp++
        """
        file = CodeWriter.asm_fd
        file.write("// or\n")
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("D=M\n")
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("D=D|M\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("M=D\n")
        file.write("@SP\n")
        file.write("M=M+1\n")

    @staticmethod
    def process_neg():
        """
        pseudocode:

        sp--
        a=*sp
        a=-a
        *sp=a
        sp++
        """
        file = CodeWriter.asm_fd
        file.write("// neg\n")
        file.write("@SP\n")
        file.write("M=M-1\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("D=M\n")
        file.write("D=-D\n")
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("M=D\n")
        file.write("@SP\n")
        file.write("M=M+1\n")


    @staticmethod
    def process_arithematic(arg):
        print("process_arithematic ", arg)
        if arg.startswith("add"):
            print("received add command")
            CodeWriter.process_add()
        elif arg.startswith("sub"):
            print("received sub command")
            CodeWriter.process_sub()
        elif arg.startswith("eq"):
            print("received eq command")
            CodeWriter.process_eq()
        elif arg.startswith("gt"):
            print("received gt command")
            CodeWriter.process_gt()
        elif arg.startswith("lt"):
            print("received lt command")
            CodeWriter.process_lt()
        elif arg.startswith("not"):
            print("received not command")
            CodeWriter.process_not()
        elif arg.startswith("and"):
            print("received and command")
            CodeWriter.process_and()
        elif arg.startswith("or"):
            print("received or command")
            CodeWriter.process_or()
        elif arg.startswith("neg"):
            print("received neg command")
            CodeWriter.process_neg()
        else:
            # Should not reach here
            assert(True)

    def process_command(self, command_type, arg0, arg1, arg2):
        if command_type == CommandType.C_PUSH:
            print("Received push command")
            CodeWriter.process_push(arg1, arg2)
        if command_type == CommandType.C_POP:
            print("Received pop command")
            CodeWriter.process_pop(arg1, arg2)
        if command_type == CommandType.C_ARITHEMATIC:
            print("Received arithematic/logical command")
            CodeWriter.process_arithematic(arg0)
            pass

