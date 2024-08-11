from colorama import Fore

class DebugSignatures:
    """
    A class containing debug message signatures with colored formatting.
    """
    MESSAGE_DEBUG = f'[{Fore.LIGHTBLACK_EX} DEBUG {Fore.RESET}]'
    MESSAGE_TOKENIZER = f'[{Fore.LIGHTBLACK_EX} TOKENIZER {Fore.RESET}]'
    MESSAGE_LOADER = f'[{Fore.LIGHTBLACK_EX} LOADER {Fore.RESET}]'
    MESSAGE_PARSER = f'[{Fore.LIGHTBLACK_EX} PARSER {Fore.RESET}]'
    MESSAGE_MEMORY = f'[{Fore.LIGHTBLACK_EX} MEMORY {Fore.RESET}]'

    NO = f'[{Fore.RED} no {Fore.RESET}]'
    YES = f'[{Fore.GREEN} yes {Fore.RESET}]'
    WARNING = f'[{Fore.YELLOW} warning {Fore.RESET}]'

debug_log = False

def set_debug_log(value: bool):
    """
    Set the debug log status.
    """
    global debug_log
    debug_log = value

class DebugMessage:
    """
    A class for handling debug messages with specific signatures.
    """

    def __init__(self, debug_signature: DebugSignatures) -> None:
        """
        Initialize a DebugMessage instance.

        Args:
            debug_signature (DebugSignatures): The debug signature to use for messages.
        """
        self.__debug_signature = debug_signature
        self.out_funct = None
        self.__messages = []

    def add_message(self, message: str):
        """
        Add a debug message to the internal message list.

        Args:
            message (str): The message to add.
        """
        self.__messages.append(f'[ {Fore.CYAN}DEBUG{Fore.RESET} ] {self.__debug_signature} {message}')

    def __call__(self, *args):
        """
        Print all stored debug messages and call the output function.

        Args:
            *args: Variable length argument list to pass to the output function.
        """
        if debug_log:
            for mess in self.__messages:
                print(mess)
            self.out_funct(*args)
            print('')