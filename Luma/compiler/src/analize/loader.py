from src.debug import loader as debug_loader
from colorama import Fore

class LumaFile:
    def __init__(self, code: str, code_file: str, code_lenght: str) -> None:
        self.code = code
        self.code_file = code_file
        self.code_lenght = code_lenght
        self.code_to_lines = self.code.split('\n')

def LoadLumaFile(file_name: str):

    if file_name.split('.')[-1] == 'lm':
        debug_loader.debug_file_load_succes.out_funct = lambda file_name: print(f'File {Fore.YELLOW}{file_name}{Fore.RESET}.')
        debug_loader.debug_file_load_succes(file_name)
    else:
        debug_loader.debug_file_load_error.out_funct = lambda file_name: print(f'File {Fore.YELLOW}{file_name}{Fore.RESET} extension is not {Fore.YELLOW}".lm"{Fore.RESET}')
        debug_loader.debug_file_load_error(file_name)

    __code = ''.join(open(file_name, 'r').readlines()) + '\n'
    __code_lenght = len(__code)

    return LumaFile(__code, file_name, __code_lenght)
   