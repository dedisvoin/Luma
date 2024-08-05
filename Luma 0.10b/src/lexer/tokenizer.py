from copy import copy
import sys
sys.path.extend('../')

from src.core import tokens
from src.core import lexems
from src.debugs import debug_lexer

class Tokenizer:
    def __init__(self) -> None:
        self.__code = []
        self.__pos = 0
        self.__code_lenght = 0
        self.__this_line = 0
        self.__this_pos = 0
        self.__tokens: list[tokens.Token] = []
        self.__standart_tokens: list[tokens.Token] = []
        self.__file_name = ''
        
    def debug_first_stage_tokens(self):
        debug_lexer.debug_first_stage_tokens(self.__tokens)

    def debug_second_stage_tokens(self):
        debug_lexer.debug_second_stage_tokens(self.__standart_tokens)

    @property
    def basic_tokens(self) -> list[tokens.Token]:
        return self.__tokens
    
    @property
    def standert_tokens(self) -> list[tokens.Token]:
        return self.__standart_tokens

    @property
    def file_name(self) -> str:
        return self.__file_name
    
    @file_name.setter
    def file_name(self, value: str):
        self.__file_name = value

    def reinit(self):
        self.__code = []
        self.__pos = 0

    def load_file(self, file_name: str):
        self.reinit()
        self.__code = ''.join(open(file_name, 'r').readlines()) + '\n'
        self.__code_lenght = len(self.__code)
        self.__file_name = file_name

    def load_string(self, string: str):
        self.reinit()
        self.__code = string
        self.__code_lenght = len(self.__code)

    def next_sym(self):
        self.__this_pos += 1 
        if self.get_sym() == '\n':
            self.__this_line += 1
            self.__this_pos = 0
        self.__pos += 1

    def before_sym(self):
        self.__pos -= 1

    def get_sym(self, offset: int = 0) -> str:
        return self.__code[self.__pos + offset]
    
    def is_char(self) -> bool:
        if self.get_sym() in lexems.CHARS: return True
        return False
    
    def is_number(self) -> bool:
        if self.get_sym() in lexems.NUMBERS: return True
        return False
    
    def is_thunder(self) -> bool:
        if self.get_sym() in lexems.THUNDER: return True
        return False
    
    def is_dot(self) -> bool:
        if self.get_sym() in lexems.DOT: return True
        return False
    
    def is_marks(self) -> bool:
        if self.get_sym() in lexems.MARKS: return True
        return False
    
    def is_operator(self) -> bool:
        if self.get_sym() in lexems.SYMVOLS: return True
        return False
    
    def is_bracket(self) -> bool:
        if self.get_sym() in lexems.BRACKETS: return True
        return False
    
    def is_comment_basic_start(self) -> bool:
        if self.get_sym() == '/' and self.get_sym(1) == '/':
            return True
        return False
    
    def is_comment_multiline_start(self) -> bool:
        if self.get_sym() == '/' and self.get_sym(1) == '*':
            return True
        return False

    def tokenize_word(self):
        data = ''
        pos = copy(self.__this_pos)
        
        while True:
            data += self.get_sym()
            self.next_sym()
            if (not self.is_char()) and (not self.is_number()) and (not self.is_thunder()):
                break
        
        self.__tokens.append(
            tokens.Token(
                tokens.TokenSignature.WORD,
                data,
                tokens.TokenPosition(self.__this_line, pos, len(data))
            )
        )
    
    def tokenize_number(self):
        data = ''
        pos = copy(self.__this_pos)

        while True:
            data += self.get_sym()
            self.next_sym()
            if (not self.is_number()) and (not self.is_dot()):  
                break

        self.__tokens.append(
            tokens.Token(
                tokens.TokenSignature.NUMBER,
                data,
                tokens.TokenPosition(self.__this_line, pos, len(data))
            )
        )

    def tokenize_text(self):
        data = ''
        self.next_sym()
        pos = copy(self.__this_pos)

        while (not self.is_marks()):
            data += self.get_sym()
            self.next_sym()

        self.__tokens.append(
            tokens.Token(
                tokens.TokenSignature.STRING,
                data,
                tokens.TokenPosition(self.__this_line, pos, len(data))
            )
        )

    def tokenize_operator(self):
        data = ''
        pos = copy(self.__this_pos)

        while True:
            data += self.get_sym()
            self.next_sym()

            if (not self.is_operator()): 
                break

        self.__tokens.append(
            tokens.Token(
                tokens.TokenSignature.OPERATOR,
                data,
                tokens.TokenPosition(self.__this_line, pos, len(data))
            )
        )
        self.before_sym()
        
    def tokenize_bracket(self):
        data = ''

        pos = copy(self.__this_pos)
        data += self.get_sym()

        
        self.__tokens.append(
            tokens.Token(
                tokens.TokenSignature.BRACKET,
                data,
                tokens.TokenPosition(self.__this_line, pos, len(data))
            )
        )

    def tokenize_basic_comment(self):
        self.next_sym()
        self.next_sym()
        while self.get_sym() != '\n':
            self.next_sym()
        
    def tokenize_multiline_comment(self):
        self.next_sym()
        self.next_sym()
        while not (self.get_sym() == '*' and self.get_sym(1) == '/'):
            self.next_sym()
        self.next_sym()
        self.next_sym()

    def tokenize(self):
        while self.__pos < self.__code_lenght:
            if self.is_comment_basic_start():
                self.tokenize_basic_comment()
            if self.is_comment_multiline_start():
                self.tokenize_multiline_comment()
            if self.is_char():
                self.tokenize_word()
            if self.is_number():
                self.tokenize_number()
            if self.is_marks():
                self.tokenize_text()
            if self.is_operator():
                self.tokenize_operator()
            if self.is_bracket():
                self.tokenize_bracket()
            
            self.next_sym()

    def convert_signatures(self):
        self.__standart_tokens = []
        for token in self.__tokens:
            self.__standart_tokens.append(
                tokens.signature_convert(token)
            )
        self.__standart_tokens.append(
            tokens.Token(
                tokens.TokenSignature.EOF, 'eof', tokens.TokenPosition(-2, -1, -1)
            )
        )
        