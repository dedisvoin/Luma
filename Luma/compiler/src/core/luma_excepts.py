from colorama import Fore
from src.core import tokens
from src.analize import loader
import os

class LumaExceptionType:
    PARSER = f'[ {Fore.CYAN}parser{Fore.RESET} ]'
    COMPILE = f'[ {Fore.YELLOW}compile{Fore.RESET} ]'
    EXECUTE = f'[ {Fore.BLUE}execute{Fore.RESET} ]'

class ExceptionColor:
    RED = Fore.RED
    YELLOW = Fore.YELLOW

class BaseLumaException():
    def __init__(self, file: loader.LumaFile, except_type: LumaExceptionType, text: str) -> None:
        self.__except_type = except_type
        self.__text = text
        self.__file = file
        self.__color = ExceptionColor.RED

    @property
    def color(self) -> str: return self.__color

    @color.setter
    def color(self, value: str):
        self.__color = value

    def __call__(self, pos: tokens.TokenPosition, exiting = True) -> str:
        error_or_waring = "error" if self.__color == ExceptionColor.RED else 'warining'
        print( f'''Exception {self.__except_type} [ {Fore.BLACK}{self.__file.code_file}{Fore.RESET} ] {str(pos)}

''')
        print(f'          {self.__file.code_to_lines[pos.line]}')
        print(f'          {" " * pos.start + f"{self.__color}▲{Fore.RESET}" * pos.lenght}')
        print(f'          {" " * (pos.start+pos.lenght-1) + f"{self.__color}┃{Fore.RESET}"}')
        print(f'          {" " * (pos.start+pos.lenght-1) + f"{self.__color}┗{Fore.RESET}"} {self.__color}━━━< {error_or_waring} > {Fore.RESET}{self.__text}')
        if exiting:
            os._exit(-1)


def call_exception_not_suport_operation(file, operation, value_left, value_right, pos):
    BaseLumaException(file, LumaExceptionType.EXECUTE, f'The operation {Fore.YELLOW}"{operation}"{Fore.RESET} is not supported between {Fore.BLUE}<{value_left.get_type().name}>{Fore.RESET} and {Fore.BLUE}<{value_right.get_type().name}>{Fore.RESET}')(pos)

def call_exception_base_vaiable_not_found(file, var_name, pos):
    BaseLumaException(file, LumaExceptionType.EXECUTE, f'Variable {Fore.YELLOW}"{var_name}"{Fore.RESET} not found')(pos)

def call_exception_diapozon_generate_fail(file, start_pos, type_1, type_2, type_3):
    BaseLumaException(file, LumaExceptionType.COMPILE, f'Diapozon generate fail, [ {Fore.BLUE}<{type_1.name}>{Fore.RESET} -> {Fore.BLUE}<{type_2.name}>{Fore.RESET} : {Fore.BLUE}<{type_3.name}>{Fore.RESET} ] types not supported to be generate')(start_pos)

def call_exception_wait(file, signature, pos_minus_1):
    BaseLumaException(file, LumaExceptionType.PARSER, f'Waited {Fore.YELLOW}"{signature.value}"{Fore.RESET} signature')(
        tokens.TokenPosition(pos_minus_1.line, pos_minus_1.start + pos_minus_1.lenght, 1)
    )

def call_exeception_base_variable_not_mutable(file, var_name, pos):
    BaseLumaException(file, LumaExceptionType.EXECUTE, f'Variable {Fore.YELLOW}"{var_name}"{Fore.RESET} is not mutable')(pos)

def call_warning_arguments_generate(file, start_pos, end_pos, exiting: bool = False):
    excep = BaseLumaException(file, LumaExceptionType.PARSER, f'Arguments generate not been')
    excep.color = ExceptionColor.YELLOW
    excep(tokens.TokenPosition(start_pos.line, start_pos.start, end_pos.start - start_pos.start), exiting)

def call_warning_variable_is_not_callable(file, pos, var_name, value):
    BaseLumaException(file, LumaExceptionType.EXECUTE, f'Variable {Fore.YELLOW}"{var_name}"{Fore.RESET} {Fore.BLUE}<{value.get_type().name}>{Fore.RESET} type is not callable')(pos)

def call_exceprion_callable_error_argument_count(file, pos, name, wait_args_count, these_args_count):
    BaseLumaException(file, LumaExceptionType.COMPILE, f'{Fore.YELLOW}"{name}"{Fore.RESET} {Fore.BLUE}waited [ {wait_args_count} ]{Fore.RESET} args count, you {Fore.BLUE}get [ {these_args_count} ]{Fore.RESET} args count')(pos)

def call_warning_args_count(file, pos):
    excep = BaseLumaException(file, LumaExceptionType.COMPILE, 'Error arguments count')
    excep.color = ExceptionColor.YELLOW
    excep(pos, False)