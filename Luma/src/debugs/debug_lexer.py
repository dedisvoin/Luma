import sys
sys.path.extend('../')
from colorama import Fore

from src.core import tokens
from src.core.debug import DEBUG

def debug_first_stage_tokens(tokens: list[tokens.Token]):
    print(f'{DEBUG} first stage tokens', '-'*95)
    for i, token in enumerate(tokens):
        print(f'\
|   index > {Fore.GREEN}{i:<3}{Fore.RESET} \
|   type > {Fore.YELLOW}{token.signature:<30}{Fore.RESET} \
|   value > {Fore.MAGENTA}{token.value:<20}{Fore.RESET} \
|   position > {Fore.CYAN}{f'[{token.position.line:>3},{token.position.start:>3},{token.position.lenght:>3}]':<17}{Fore.RESET}|')
    print('-'*124)

def debug_second_stage_tokens(tokens:list[tokens.Token]):
    print(f'{DEBUG} second stage tokens', '-'*94)
    for i, token in enumerate(tokens):
        print(f'\
|   index > {Fore.GREEN}{i:<3}{Fore.RESET} \
|   type > {Fore.YELLOW}{token.signature:<30}{Fore.RESET} \
|   value > {Fore.MAGENTA}{token.value:<20}{Fore.RESET} \
|   position > {Fore.CYAN}{f'[{token.position.line:>3},{token.position.start:>3},{token.position.lenght:>3}]':<17}{Fore.RESET}|')
    print('-'*124)