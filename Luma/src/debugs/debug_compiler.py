import sys
import os
sys.path.extend('../')

from colorama import Fore
from src.core.debug import LEXER, YES, NO, PARSER, DEBUG
from src.debugs.debug_helps import *
from src.runtime.memory import MemoryObjectTypes


def debug_file_exception(file_name: str):
    if file_name.split('.')[1] == 'lm': return True
    return False

def debug_file_loading(file_name: str):
    if debug_file_exception(file_name):
        print(f'{LEXER} file {Fore.YELLOW}{file_name}{Fore.RESET} loading... {YES}')
    else:
        print(f'{LEXER} file {Fore.YELLOW}{file_name}{Fore.RESET} loading... {NO}')
        help_file_load()
        os._exit(-1)
    
def debug_tokenize(tokens_count: int, time: float):
    print(f'''{LEXER} Tokenize finished {Fore.BLACK}{round(time, 2)}s{Fore.RESET}. {YES}
|   tokens count {Fore.CYAN}{tokens_count}{Fore.RESET}''')
    
def debug_signatures_converting(tokens_count: int, time: float):
    print(f'''{LEXER} Signatures converting finished {Fore.BLACK}{round(time, 2)}s{Fore.RESET}. {YES}
|   tokens count {Fore.CYAN}{tokens_count}{Fore.RESET}''')
    
def debug_parsing_finished(commands_count: int, time: float):
    print(f'''{PARSER} Tokens Parsing finished {Fore.BLACK}{round(time, 2)}s{Fore.RESET}. {YES}
|   commands count {Fore.CYAN}{commands_count}{Fore.RESET}''')
    
def debug_run_time_memory(memory_):
    print(f'{DEBUG} Memory view', '-' * 102)
    #print([mobj.value.type.name for mobj in memory_])
    for memory_object in memory_:
        if memory_object.type == MemoryObjectTypes.VARIABLE:
            print(f"|   type > {Fore.BLUE}{memory_object.type:<20}{Fore.RESET}|   value > {Fore.YELLOW}{memory_object.value.value:<20}{Fore.RESET}| name > {Fore.YELLOW}{memory_object.name:<18}{Fore.RESET}  | mutable > {memory_object.mutable:<5} |  cc > {memory_object.cached:<5}|")
    
        if memory_object.type == MemoryObjectTypes.LAMBDA:
            print(f"|   type > {Fore.BLUE}{memory_object.type:<20}{Fore.RESET}| {' ':<30}| name > {Fore.YELLOW}{memory_object.name:<18}{Fore.RESET}  | mutable > {memory_object.mutable:<5} |  cc > {memory_object.cached:<5}|")

        if memory_object.type == MemoryObjectTypes.FUNCTION:
            print(f"|   type > {Fore.BLUE}{memory_object.type:<20}{Fore.RESET}| {' ':<30}| name > {Fore.YELLOW}{memory_object.name:<18}{Fore.RESET}  | mutable > {memory_object.mutable:<5} |  cc > {memory_object.cached:<5}|")
           
    print(f'-' * 124)