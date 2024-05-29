#!/usr/bin/python

from vm_translator_constants import CommandType

class VmParser:
    vm_file = None
    commands = list()
    command_idx = 0
    total_commmand_count = 0

    def __init__(self, vm_file):
        print("Hello from Parser init!")
        print("VM file path is ", vm_file)
        VmParser.vm_file = vm_file
        VmParser.command_idx = 0
        VmParser.total_command_count = 0

    def parse_vm_file(self):
        print("Reading VM file...")
        print("VM file contains...")
        with open(VmParser.vm_file) as file:
            for line in file:
                # Filter trailing comments on any line
                line, sep, tail = line.partition("//")
                # Remove leading and trailing whitespaces
                line = line.strip()
                # Check for a "legitimate" line i.e. ignore blank lines and
                # comments
                if ( line != '' ) and (not line.startswith("//")):
                    print(line)
                    command = line.split()
                    # Add command to commands list
                    #command = line.strip()
                    VmParser.commands.append(command)
                    VmParser.total_command_count += 1

    def get_arg0(self):
        command = VmParser.commands[VmParser.command_idx]
        return command[0]

    def get_arg1(self):
        command = VmParser.commands[VmParser.command_idx]
        if (len(command) >= 2):
            return command[1]
        return None

    def get_arg2(self):
        command = VmParser.commands[VmParser.command_idx]
        if (len(command) == 3):
            return command[2]
        return None

    def get_command_type(self):
        command = VmParser.commands[VmParser.command_idx]
        command_type = None

        if (command[0] == "push"):
            command_type = CommandType.C_PUSH
        elif (command[0] == "pop"):
            command_type = CommandType.C_POP
        elif (command[0] == "add"):
            command_type = CommandType.C_ARITHEMATIC
        elif (command[0] == "sub"):
            command_type = CommandType.C_ARITHEMATIC
        elif (command[0] == "neg"):
            command_type = CommandType.C_ARITHEMATIC
        elif (command[0] == "eq"):
            command_type = CommandType.C_ARITHEMATIC
        elif (command[0] == "gt"):
            command_type = CommandType.C_ARITHEMATIC
        elif (command[0] == "lt"):
            command_type = CommandType.C_ARITHEMATIC
        elif (command[0] == "and"):
            command_type = CommandType.C_ARITHEMATIC
        elif (command[0] == "or"):
            command_type = CommandType.C_ARITHEMATIC
        elif (command[0] == "not"):
            command_type = CommandType.C_ARITHEMATIC

        # TODO: need to implement branching and function command types

        return command_type

    def has_more_commands(self):
        return (VmParser.command_idx != VmParser.total_command_count)

    def advance(self):
        VmParser.command_idx += 1

    def dump_commands(self):
        print("total command count = ", VmParser.total_command_count)
        print("Commands : ")
        for item in VmParser.commands:
            print(item)
