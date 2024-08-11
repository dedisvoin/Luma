from src.core import tokens
from src.analize import loader
from src.core import luma_excepts
from colorama import Fore

class PreProcessor:
    class Commands:
        class CommandDefine:
            def __init__(self, value: str, replace: str, file: loader.LumaFile, this_command_line: int) -> None:
                self.value = value
                self.replace = replace
                self.file = file
                self.this_command_line = this_command_line

            def exec(self):
                self.file.code = self.file.code.replace(self.value, self.replace)
                test_code = self.file.code.split('\n')
                for i in range(len(test_code)):
                    if i == self.this_command_line:
                        test_code[i] = '       '
                
                self.file.code = ''
                
                for line in test_code:
                    if line == '':
                        line = '       '
                        
                    self.file.code += line + '\n'
                self.file.code_lenght = len(self.file.code)
                #print(self.file.code)



    def __init__(self) -> None:
        self.__tokens = []
        self.__processses = []
        self.__pos = 0
        self.__file = None

    @property
    def file(self) -> loader.LumaFile:
        return self.__file
    
    @file.setter
    def file(self, value: loader.LumaFile):
        self.__file = value

    @property
    def standart_tokens(self) -> list[tokens.Token]:
        return self.__tokens
    
    @standart_tokens.setter
    def standart_tokens(self, value: list[tokens.Token]):
        self.__tokens = value

    def next_token(self):
        self.__pos += 1

    def get_token(self, offset: int = 0):
        return self.__tokens[self.__pos + offset]
    
    def get_token_signature(self, offset: int = 0) -> tokens.TokenSignature:
        return self.get_token(offset).signature
    
    def get_token_value(self, offset: int = 0) -> str:
        return self.get_token(offset).value
    
    def get_token_position(self, offset: int = 0) -> tokens.TokenPosition:
        return self.get_token(offset).position
    
    def is_token_signature(self, signature: tokens.TokenSignature, offset: int = 0) -> bool:
        return self.get_token_signature(offset) == signature
    
    def is_token_signatures(self, signatured: list[tokens.TokenSignature], offset: int = 0) -> bool:
        for signature in signatured:
            if self.is_token_signature(signature, offset):
                return True
        return False
    
    def match_token_signature(self, signature: tokens.TokenSignature, offset: int = 0):
        if self.is_token_signature(signature, offset):
            self.next_token()
            return True
        return False
    
    def match_and_wait(self, signature: tokens.SignatureObject, offset: int = 0):
        if self.match_token_signature(signature.signature, offset):
            ...
        else:
            luma_excepts.BaseLumaException(self.__file, luma_excepts.LumaExceptionType.PARSER, f'Waited {Fore.YELLOW}"{signature.value}"{Fore.RESET} signature')(
                tokens.TokenPosition(self.get_token_position(-1).line, self.get_token_position(-1).start + self.get_token_position(-1).lenght, 1)
            )
        
    def is_token_and_wait(self, signature: tokens.SignatureObject, offset: int = 0):
        if self.is_token_signature(signature.signature, offset):
            ...
        else:
            luma_excepts.BaseLumaException(self.__file, luma_excepts.LumaExceptionType.PARSER, f'Waited {Fore.YELLOW}"{signature.value}"{Fore.RESET} signature')(
                tokens.TokenPosition(self.get_token_position(-1).line, self.get_token_position(-1).start + self.get_token_position(-1).lenght, 1)
            )

    
    def parse_commands(self):
        
        if self.is_token_signature(tokens.TokenSignature.OPERATOR_DOLLAR):
            self.next_token()
            self.is_token_and_wait(tokens.SignatureObject(tokens.TokenSignature.WORD, 'preprocessor command'))
            command = self.get_token_value()
            self.next_token()
            if command == 'define':
                self.is_token_and_wait(tokens.SignatureObject(tokens.TokenSignature.WORD, 'replace name'))
                start_value = self.get_token_value()
                self.next_token()
                self.match_and_wait(tokens.get_signature('('))
                
                
                new_value = self.get_token_value()
                self.next_token()
                self.match_and_wait(tokens.get_signature(')'))
                self.is_token_and_wait(tokens.get_signature(';'))
                return self.Commands.CommandDefine(start_value, new_value, self.__file, self.get_token_position().line)
                

    def parse(self):
        while self.__tokens[self.__pos].signature != tokens.TokenSignature.EOF:
            command = self.parse_commands()
            if command is not None:
                self.__processses.append(command)
            self.next_token()

    def execute(self):
        for command in self.__processses:
            command.exec()
        