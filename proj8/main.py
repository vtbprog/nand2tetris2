#!/usr/bin/python

import vm_parser
import code_writer
import argparse
import os
from vm_translator_constants import CommandType

def main():
    print("Hello world!")

    # Parse command-line args
    argparser = argparse.ArgumentParser()
    required_cmd_args = argparser.add_argument_group('Required Arguments')
    optional_cmd_args = argparser.add_argument_group('Optional Arguments')

    optional_cmd_args.add_argument("-v", "--vm_file", help="Path to input .vm file")
    optional_cmd_args.add_argument("-d", "--vm_dir", help="Path to directory containing .vm files")
    required_cmd_args.add_argument("-a", "--asm_file", help="Path to output .asm file", required=True)

    cmd_args = argparser.parse_args()

    if (cmd_args.vm_file):
        print("vm_file path is ", cmd_args.vm_file)
    if (cmd_args.vm_dir):
        print("vm_dir path is ", cmd_args.vm_dir)

    print("asm_file path is ", cmd_args.asm_file)

    # Instantiate VM parser
    my_vm_parser = vm_parser.VmParser()
    if (cmd_args.vm_file):
        my_vm_parser.parse_vm_file(cmd_args.vm_file)
    elif (cmd_args.vm_dir):
        for file in os.listdir(cmd_args.vm_dir):
            if file.endswith(".vm"):
                my_vm_parser.parse_vm_file(os.path.join(cmd_args.vm_dir, file))
    else:
        print("Invalid args specified!")
        assert(False);

    # Instantiate Code Writer
    my_code_writer = code_writer.CodeWriter(cmd_args.asm_file)

    # Dump commands
    my_vm_parser.dump_commands()

    # Setup bootcode
    my_code_writer.setup_bootcode()

    while (my_vm_parser.has_more_commands()):

        # Get command type
        command_type = my_vm_parser.get_command_type()

        # Get arg0, arg1, arg2
        arg0 = my_vm_parser.get_arg0()
        arg1 = my_vm_parser.get_arg1()
        arg2 = my_vm_parser.get_arg2()

        # Get vm filename
        vm_fname = my_vm_parser.get_vm_fname()

        # ask codewriter to process command
        my_code_writer.process_command(command_type, arg0, arg1, arg2, vm_fname)

        # advance
        my_vm_parser.advance()

if __name__ == "__main__":
    main()
