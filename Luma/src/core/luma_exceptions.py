from typing import Any
from src.core import tokens
from colorama import Fore, Back
from src.core.debug import PARSER, COMPILER
import sys

class LumaExceptionTypes:
    WAIT_TYPE = f'{Fore.BLACK}wait{Fore.RESET}'
    ERROR_NUMBER = f'{Fore.BLACK}error number{Fore.RESET}'
    ERROR_CHAINGE = f'{Fore.BLACK}error chainge{Fore.RESET}'
    ERROR_NAME = f'{Fore.BLACK}error chainge{Fore.RESET}'
    FOUND_VALUE = f'{Fore.BLACK}found{Fore.RESET}'
    NOT_SUPPORT_OPERATION = f'{Fore.BLACK}not support operation{Fore.RESET}'
    ERROR_ARGUMENTS_COUNT = f'{Fore.BLACK}error arguments count{Fore.RESET}'
    ERROR_TYPED_ARGUMENT = f'{Fore.BLACK}error typed argument{Fore.RESET}'


class BaseLumaException:
    def __init__(self, type: LumaExceptionTypes, file: str, pos: tokens.TokenPosition) -> None:
        self.type = type
        self.file = file
        self.pos = pos
        self.exp_type = PARSER
        self.sum_dx = 0
        self.code_lines = open(self.file, 'r').readlines()

    def raise_(self):
        print(f"{self.exp_type} Exception ({self.type}) with file {Fore.YELLOW}'{self.file}'{Fore.RESET}.")
        print(f'|',' ' * 8, self.code_lines[self.pos.line - 1].replace('\n', ''))
        
        print('|',' ' * 8, ' '*(self.pos.start-3+self.sum_dx), f'{Fore.RED}{str('^'*(self.pos.lenght))}{Fore.RESET}')

    def stop_run_time(self):
        sys.exit(-1)

class WaitException(BaseLumaException):
    def __init__(self, waited_signature: str, file: str | None = None, pos: tokens.TokenPosition | None = None) -> None:
        super().__init__(LumaExceptionTypes.WAIT_TYPE, file, pos)
        self.waited_signature = waited_signature

    def LumaRaise(self):
        self.raise_()
        print(f"|   In position {str(self.pos)} waited [ {Fore.LIGHTMAGENTA_EX}{self.waited_signature}{Fore.RESET} ] signature.")
        self.stop_run_time()
    
class NumberException(BaseLumaException):
    def __init__(self, file: str | None = None, pos: tokens.TokenPosition | None = None) -> None:
        super().__init__(LumaExceptionTypes.ERROR_NUMBER, file, pos)

    def LumaRaise(self):
        self.raise_()
        print(f"|   In position {str(self.pos)} number errored.")
        self.stop_run_time()

class VariableChainge(BaseLumaException):
    def __init__(self, file: str | None = None, pos: tokens.TokenPosition | None = None, var_name: str = '') -> None:
        super().__init__(LumaExceptionTypes.ERROR_CHAINGE, file, pos)
        self.var_name = var_name
        self.exp_type = COMPILER

    def LumaRaise(self):
        self.raise_()
        print(f"|   In position {str(self.pos)} chainge error. Variable {Fore.YELLOW}'{self.var_name}'{Fore.RESET} is not mutable.")
        self.stop_run_time()

class VariableNotFound(BaseLumaException):
    def __init__(self, file: str | None = None, pos: tokens.TokenPosition | None = None, var_name: str = '') -> None:
        super().__init__(LumaExceptionTypes.FOUND_VALUE, file, pos)
        self.var_name = var_name
        self.exp_type = COMPILER
        self.sum_dx = 2
    
    def LumaRaise(self):
        self.raise_()
        print(f"|   In position {str(self.pos)}. Variable {Fore.YELLOW}'{self.var_name}'{Fore.RESET} not found.")
        self.stop_run_time()

class NotSupportedUnaryOperation(BaseLumaException):
    def __init__(self, file: str | None = None, pos: tokens.TokenPosition | None = None, operation: str = '', value: Any = None) -> None:
        super().__init__(LumaExceptionTypes.NOT_SUPPORT_OPERATION, file, pos)
        self.operation = operation
        self.value = value
        self.exp_type = COMPILER
    
    def LumaRaise(self):
        self.raise_()
        print(f"|   In position {str(self.pos)}. [ {Fore.LIGHTMAGENTA_EX}{self.value.type.name}{Fore.RESET} ] type value not support '{self.operation}' operation.")
        self.stop_run_time()

class NotSupportedBinareOperation(BaseLumaException):
    def __init__(self, file: str | None = None, pos: tokens.TokenPosition | None = None, operation: str = '', value_left: Any = None, value_right: Any = None) -> None:
        super().__init__(LumaExceptionTypes.NOT_SUPPORT_OPERATION, file, pos)
        self.operation = operation
        self.value_left = value_left
        self.value_right = value_right
        self.exp_type = COMPILER

    def LumaRaise(self):
        self.raise_()
        print(f"|   In position {str(self.pos)}. [ {Fore.LIGHTMAGENTA_EX}{self.value_left.type.name}{Fore.RESET} ] type and [ {Fore.LIGHTMAGENTA_EX}{self.value_right.type.name}{Fore.RESET} ] type values not support '{self.operation}' operation.")
        self.stop_run_time()

class IncorrectDefinitionArgument(BaseLumaException):
    def __init__(self, file: str | None = None, pos: tokens.TokenPosition | None = None, name: str = '') -> None:
        super().__init__(LumaExceptionTypes.ERROR_NAME, file, pos)
        self.name = name
        self.exp_type = PARSER

    def LumaRaise(self):
        self.raise_()
        print(f"|   In position {str(self.pos)}. Incorrect argument name definition {Fore.YELLOW}'{self.name}'{Fore.RESET}")
        self.stop_run_time()

class ArgumentCountError(BaseLumaException):
    def __init__(self, file: str | None = None, pos: tokens.TokenPosition | None = None, name: str = '', arguments_count: int = 0, waited_arguments_count: int = 0) -> None:
        super().__init__(LumaExceptionTypes.ERROR_ARGUMENTS_COUNT, file, pos)
        self.name = name
        self.exp_type = COMPILER
        self.args_count = arguments_count
        self.waited_args_count = waited_arguments_count
    
    def LumaRaise(self):
        self.raise_()
        print(f"|   In position {str(self.pos)}. Incorrect argument count definition {Fore.YELLOW}'{self.name}'{Fore.RESET} waited {self.waited_args_count} you set {self.args_count}.")
        self.stop_run_time()

class FileNotFound(BaseLumaException):
    def __init__(self, file: str | None = None, pos: tokens.TokenPosition | None = None, name: str = '') -> None:
        super().__init__(LumaExceptionTypes.FOUND_VALUE, file, pos)
        self.name = name
        self.exp_type = COMPILER
    
    def LumaRaise(self):
        self.raise_()
        print(f"|   In position {str(self.pos)}. File {Fore.YELLOW}'{self.name}'{Fore.RESET} not found.")
        self.stop_run_time()

class ErrorTypedArg(BaseLumaException):
    def __init__(self, file: str | None = None, pos: tokens.TokenPosition | None = None, name: str = '', type_name: str = '', arg_index = 0) -> None:
        super().__init__(LumaExceptionTypes.ERROR_TYPED_ARGUMENT, file, pos)
        self.name = name
        self.arg_index = arg_index
        self.type_name = type_name
        self.exp_type = COMPILER

    def LumaRaise(self):
        self.raise_()

        tps = []
        for obj in self.name.value.value.types:
            obj_t = []
            for t in obj:
                obj_t.append(t.name)
            tps.append(obj_t)

        print(f"|   In position {str(self.pos)}. Function {Fore.YELLOW}'{self.name.value.value.name}'{Fore.RESET} [ {self.arg_index} ] index argument type is {Fore.LIGHTMAGENTA_EX}{obj_t}{Fore.RESET} but mustn't be {Fore.YELLOW}'{self.type_name.value.type.name}'{Fore.RESET}.")
        self.stop_run_time()