#!/usr/bin/python

import vm_parser
import code_writer
import argparse
from vm_translator_constants import CommandType

def main():
    print("Hello world!")

    # Parse command-line args
    argparser = argparse.ArgumentParser()
    required_cmd_args = argparser.add_argument_group('Required Arguments')

    required_cmd_args.add_argument("-v", "--vm_file", help="Path to input .vm file", required=True)
    required_cmd_args.add_argument("-a", "--asm_file", help="Path to output .asm file", required=True)
    cmd_args = argparser.parse_args()

    print("vm_file path is ", cmd_args.vm_file)
    print("asm_file path is ", cmd_args.asm_file)

    # Instantiate VM parser
    my_vm_parser = vm_parser.VmParser(cmd_args.vm_file)
    my_vm_parser.parse_vm_file()

    # Instantiate Code Writer
    my_code_writer = code_writer.CodeWriter(cmd_args.asm_file)

    # Dump commands
    my_vm_parser.dump_commands()

    while (my_vm_parser.has_more_commands()):

        # Get command type
        command_type = my_vm_parser.get_command_type()

        # Get arg0, arg1, arg2
        arg0 = my_vm_parser.get_arg0()
        arg1 = my_vm_parser.get_arg1()
        arg2 = my_vm_parser.get_arg2()

        # ask codewriter to process command
        my_code_writer.process_command(command_type, arg0, arg1, arg2)

        # advance
        my_vm_parser.advance()

if __name__ == "__main__":
    main()
