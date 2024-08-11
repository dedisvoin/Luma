import sys

sys.path.extend('../')

from copy import copy

from src.core import tokens
from src.core import lexems
from src.analize import loader


class Tokenizer:
    """
    A class for tokenizing source code.

    This class is responsible for breaking down source code into individual tokens,
    which can then be used for further processing in a compiler or interpreter.
    """

    def __init__(self) -> None:
        """
        Initialize the Tokenizer with default values.
        """
        self.__pos = 0
        self.__this_line = 0
        self.__this_pos = 0
        self.__tokens: list[tokens.Token] = []
        self.__standart_tokens: list[tokens.Token] = []
        self.__file = None

    @property
    def basic_tokens(self) -> list[tokens.Token]:
        """
        Get the list of basic tokens.

        Returns:
            list[tokens.Token]: The list of basic tokens.
        """
        return self.__tokens
    
    @property
    def standert_tokens(self) -> list[tokens.Token]:
        """
        Get the list of standard tokens.

        Returns:
            list[tokens.Token]: The list of standard tokens.
        """
        return self.__standart_tokens

    @property
    def file(self) -> str:
        """
        Get the name of the file being tokenized.

        Returns:
            str: The name of the file.
        """
        return self.__file
    
    @file.setter
    def file(self, value: loader.LumaFile):
        """
        Set the name of the file being tokenized.

        Args:
            value (str): The name of the file.
        """
        self.__file = value

    def reinit(self):
        """
        Reinitialize the Tokenizer, clearing the code and resetting the position.
        """
        self.__pos = 0

    def next_sym(self):
        """
        Move to the next symbol in the code.
        """
        self.__this_pos += 1 
        if self.get_sym() == '\n':
            self.__this_line += 1
            self.__this_pos = 0
        self.__pos += 1

    def before_sym(self):
        """
        Move to the previous symbol in the code.
        """
        self.__pos -= 1
        self.__this_pos -=1

    def get_sym(self, offset: int = 0) -> str:
        """
        Get the symbol at the current position plus an optional offset.

        Args:
            offset (int, optional): The offset from the current position. Defaults to 0.

        Returns:
            str: The symbol at the specified position.
        """
        return self.__file.code[self.__pos + offset]
    
    def is_char(self) -> bool:
        """
        Check if the current symbol is a character.

        Returns:
            bool: True if the current symbol is a character, False otherwise.
        """
        if self.get_sym() in lexems.CHARS: return True
        return False
    
    def is_number(self) -> bool:
        """
        Check if the current symbol is a number.

        Returns:
            bool: True if the current symbol is a number, False otherwise.
        """
        if self.get_sym() in lexems.NUMBERS: return True
        return False
    
    def is_thunder(self) -> bool:
        """
        Check if the current symbol is a thunder symbol.

        Returns:
            bool: True if the current symbol is a thunder symbol, False otherwise.
        """
        if self.get_sym() in lexems.THUNDER: return True
        return False
    
    def is_dot(self) -> bool:
        """
        Check if the current symbol is a dot.

        Returns:
            bool: True if the current symbol is a dot, False otherwise.
        """
        if self.get_sym() in lexems.DOT: return True
        return False
    
    def is_marks(self) -> bool:
        """
        Check if the current symbol is a mark.

        Returns:
            bool: True if the current symbol is a mark, False otherwise.
        """
        if self.get_sym() in lexems.MARKS: return True
        return False
    
    def is_operator(self) -> bool:
        """
        Check if the current symbol is an operator.

        Returns:
            bool: True if the current symbol is an operator, False otherwise.
        """
        if self.get_sym() in lexems.SYMVOLS: return True
        return False
    
    def is_bracket(self) -> bool:
        """
        Check if the current symbol is a bracket.

        Returns:
            bool: True if the current symbol is a bracket, False otherwise.
        """
        if self.get_sym() in lexems.BRACKETS: return True
        return False
    
    def is_comment_basic_start(self) -> bool:
        """
        Check if the current position marks the start of a basic comment.

        Returns:
            bool: True if it's the start of a basic comment, False otherwise.
        """
        
        if self.get_sym() == '/' and self.get_sym(1) == '/':
            return True
        return False
    
    def is_comment_multiline_start(self) -> bool:
        """
        Check if the current position marks the start of a multiline comment.

        Returns:
            bool: True if it's the start of a multiline comment, False otherwise.
        """
        if self.get_sym() == '/' and self.get_sym(1) == '*':
            return True
        return False

    def tokenize_word(self):
        """
        Tokenize a word and add it to the list of tokens.
        """
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
        """
        Tokenize a number and add it to the list of tokens.
        """
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
        """
        Tokenize a string and add it to the list of tokens.
        """
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
        """
        Tokenize an operator and add it to the list of tokens.
        """
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
        """
        Tokenize a bracket and add it to the list of tokens.
        """
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
        """
        Tokenize a basic (single-line) comment.
        """
        self.next_sym()
        self.next_sym()
        while self.get_sym() != '\n':
            self.next_sym()
        
    def tokenize_multiline_comment(self):
        """
        Tokenize a multiline comment.
        """
        self.next_sym()
        self.next_sym()
        while not (self.get_sym() == '*' and self.get_sym(1) == '/'):
            self.next_sym()
        self.next_sym()
        self.next_sym()

    def tokenize(self):
        self.__tokens = []
        """
        Tokenize the entire code, identifying and categorizing each token.
        """
        while self.__pos < self.__file.code_lenght:
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
        """
        Convert the basic tokens to standard tokens and add an EOF token.
        """
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
