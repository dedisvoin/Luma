import sys
sys.path.extend('../')


from colorama import Fore
from src.core.debug import HELP

def help_file_load():
    print(f'''{HELP} 
|   The extension of your source code file must be {Fore.YELLOW}'.lm'{Fore.RESET}. 
|   Try renaming your file and installing the correct extension for it.''')