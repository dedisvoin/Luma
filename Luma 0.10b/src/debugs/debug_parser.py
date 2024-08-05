import sys
import os
sys.path.extend('../')

from colorama import Fore
from src.core.debug import PARSER, YES, NO, DEBUG

def debug_commands(commands):
    print(f'{DEBUG} RunTime commands', '-' * 97)
    for command in commands:
        print(f'|   command > {Fore.GREEN}{command.__class__.__name__:<40}{Fore.RESET} |    position in memory > {Fore.BLUE}{str(str(command).split('object')[1]):<41}{Fore.RESET} |')
    print(f'-' * 124)
    