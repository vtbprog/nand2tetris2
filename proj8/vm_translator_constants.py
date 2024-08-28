#!/usr/bin/python

from enum import Enum

class CommandType(Enum):
    C_ARITHEMATIC = 1
    C_PUSH = 2
    C_POP = 3
    C_IF = 4
    C_LABEL = 5
    C_GOTO = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9


