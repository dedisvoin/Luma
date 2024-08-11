from copy import copy
from colorama import Fore

class TokenSignature:
    """
    Enumeration of token types used in the lexical analysis.
    """
    # basic tokens
    NUMBER = 'NUMBER'
    WORD = 'WORD'
    STRING = 'STRING'
    OPERATOR = 'OPERATOR'
    BRACKET = 'BRACKET'
    EOF = 'EOF'
    TRUE = 'TRUE'
    FALSE = 'FALSE'

    # brackets
    BRACKET_LEFT_STANDART = 'BRACKET_LEFT_STANDART'
    BRACKET_RIGHT_STANDART = 'BRACKET_RIGHT_STANDART'
    BRACKET_LEFT_CURLY = 'BRACKET_LEFT_CURLY'
    BRACKET_RIGHT_CURLY = 'BRACKET_RIGHT_CURLY'
    BRACKET_LEFT_RECT = 'BRACKET_LEFT_RECT'
    BRACKET_RIGHT_RECT = 'BRACKET_RIGHT_RECT'

    # operators
    OPERATOR_EQUAL = 'EQUAL'
    OPERATOR_PLUS = 'PLUS'
    OPERATOR_MINUS = 'MINUS'
    OPERATOR_MUL = 'MUL'
    OPERATOR_DIV = 'DIV'
    OPERATOR_DOT_AND_COMMA = 'DOT_AND_COMMA'
    OPERATOR_DOT_AND_DOT = 'DOT_AND_DOT'
    OPERATOR_COMMA = 'COMMA'
    OPERATOR_DOT = 'DOT'
    OPERATOR_SMALLEST = 'SMALLEST'
    OPERATOR_BIGGEST = 'BIGGEST'
    OPERATOR_SMALLEST_EQUAL = 'SMALLEST_EQUAL'
    OPERATOR_BIGGEST_EQUAL = 'BIGGEST_EQUAL'
    OPERATOR_PER = 'PER'
    OPERATOR_STRELA_RIGHT = 'STRELA_RIGHT'
    OPERATOR_SNAKE = 'SNAKE'
    OPERATOR_DOLLAR = 'DOLLAR'

    OPERATOR_EQUAL_EQUAL = 'EQUAL_EQUAL'
    OPERATOR_NOT_EQUAL = 'NOT_EQUAL'
    OPERATOR_AND = 'AND'
    OPERATOR_OR = 'OR'

    # keywords
    KEYWORD_VAR = 'VAR'
    KEYWORD_VAL = 'VAL'
    KEYWORD_MUT = 'MUT'
    KEYWORD_IF = 'IF'
    KEYWORD_ELSE = 'ELSE'
    KEYWORD_FOR = 'FOR'
    KEYWORD_WHILE = 'WHILE'
    KEYWORD_FUN = 'FUN'
    KEYWORD_IN = 'IN'
    KEYWORD_RETURN = 'RETURN'
    KEYWORD_LAMBDA = 'LAMBDA'
    KEYWORD_DEL = 'DEL'
    KEYWORD_USING = 'USING'
    KEYWORD_TRY = 'TRY'
    KEYWORD_CATCH = 'CATCH'
    
class SignatureObject:
    """
    Represents a token signature with its corresponding value.
    """
    def __init__(self, signature: TokenSignature, value: str) -> None:
        """
        Initialize a SignatureObject.

        Args:
            signature (TokenSignature): The token signature.
            value (str): The corresponding value.
        """
        self.__signature = signature
        self.__value = value

    @property
    def signature(self) -> str:
        """Get the token signature."""
        return self.__signature

    @property
    def value(self) -> str:
        """Get the token value."""
        return self.__value



SIGNATURES = [
    SignatureObject(TokenSignature.KEYWORD_VAL, 'val'),
    SignatureObject(TokenSignature.KEYWORD_VAR, 'var'),
    SignatureObject(TokenSignature.KEYWORD_MUT, 'mut'),
    SignatureObject(TokenSignature.KEYWORD_IF, 'if'),
    SignatureObject(TokenSignature.KEYWORD_ELSE, 'else'),
    SignatureObject(TokenSignature.KEYWORD_FOR, 'for'),
    SignatureObject(TokenSignature.KEYWORD_WHILE, 'while'),
    SignatureObject(TokenSignature.KEYWORD_FUN, 'fun'),
    SignatureObject(TokenSignature.KEYWORD_IN, 'in'),
    SignatureObject(TokenSignature.KEYWORD_DEL, 'del'),
    SignatureObject(TokenSignature.KEYWORD_LAMBDA, 'lambda'),
    SignatureObject(TokenSignature.KEYWORD_RETURN, '|>'),
    SignatureObject(TokenSignature.KEYWORD_USING, 'using'),
    SignatureObject(TokenSignature.KEYWORD_TRY, 'try'),
    SignatureObject(TokenSignature.KEYWORD_CATCH, 'catch'),
    SignatureObject(TokenSignature.OPERATOR_DOLLAR, '$'),

    SignatureObject(TokenSignature.TRUE, 'true'),
    SignatureObject(TokenSignature.FALSE, 'false'),

    SignatureObject(TokenSignature.OPERATOR_PLUS, '+'),
    SignatureObject(TokenSignature.OPERATOR_DIV, '/'),
    SignatureObject(TokenSignature.OPERATOR_EQUAL, '='),
    SignatureObject(TokenSignature.OPERATOR_MUL, '*'),
    SignatureObject(TokenSignature.OPERATOR_PER, '%'),
    SignatureObject(TokenSignature.OPERATOR_MINUS, '-'),
    SignatureObject(TokenSignature.OPERATOR_DOT_AND_COMMA, ';'),
    SignatureObject(TokenSignature.OPERATOR_DOT, '.'),
    SignatureObject(TokenSignature.OPERATOR_COMMA, ','),
    SignatureObject(TokenSignature.OPERATOR_BIGGEST, '>'),
    SignatureObject(TokenSignature.OPERATOR_SMALLEST, '<'),
    SignatureObject(TokenSignature.OPERATOR_BIGGEST_EQUAL, '>='),
    SignatureObject(TokenSignature.OPERATOR_SMALLEST_EQUAL, '<='),
    SignatureObject(TokenSignature.OPERATOR_EQUAL_EQUAL, '=='),
    SignatureObject(TokenSignature.OPERATOR_NOT_EQUAL, '!='),
    SignatureObject(TokenSignature.OPERATOR_OR, '||'),
    SignatureObject(TokenSignature.OPERATOR_AND, '&&'),
    SignatureObject(TokenSignature.OPERATOR_STRELA_RIGHT, '->'),
    SignatureObject(TokenSignature.OPERATOR_SNAKE, '~'),
    SignatureObject(TokenSignature.OPERATOR_DOT_AND_DOT, ':'),
    
    SignatureObject(TokenSignature.BRACKET_LEFT_STANDART, '('),
    SignatureObject(TokenSignature.BRACKET_RIGHT_STANDART, ')'),
    SignatureObject(TokenSignature.BRACKET_LEFT_RECT, '['),
    SignatureObject(TokenSignature.BRACKET_RIGHT_RECT, ']'),
    SignatureObject(TokenSignature.BRACKET_LEFT_CURLY, '{'),
    SignatureObject(TokenSignature.BRACKET_RIGHT_CURLY, '}'),
]

def get_signature(string: str):
    for signature in SIGNATURES:
        if signature.value == string:
            return signature

class TokenPosition:
    """
    Represents the position of a token in the source code.
    """
    def __init__(self, gline: int, start: int, lenght: int) -> 'TokenPosition':
        """
        Initialize a TokenPosition.

        Args:
            line (int): The line number (1-indexed).
            start (int): The starting position of the token.
            lenght (int): The length of the token.
        """
        self.__line = gline
        self.__start = start
        self.__lenght = lenght

    @property
    def line(self) -> int:
        """Get the line number."""
        return self.__line

    @property
    def start(self) -> int:
        """Get the starting position."""
        return self.__start

    @property
    def lenght(self) -> int:
        """Get the length of the token."""
        return self.__lenght

    def __str__(self) -> str:
        """
        Return a string representation of the token position.

        Returns:
            str: A formatted string with line and position information.
        """
        return f'(line {Fore.MAGENTA}{self.line + 1}{Fore.RESET} : pos {Fore.MAGENTA}{self.start}{Fore.RESET} : lenght {Fore.MAGENTA}{self.lenght}{Fore.RESET})'
    
def TokensLinePos(token_pos_start: TokenPosition, token_pos_end: TokenPosition) -> TokenPosition:
    """
    Calculate the position of a token span.

    Args:
        token_pos_start (TokenPosition): The starting position of the span.
        token_pos_end (TokenPosition): The ending position of the span.

    Returns:
        TokenPosition: A new TokenPosition representing the span.
    """
    return TokenPosition(token_pos_start.line - 1, token_pos_start.start, token_pos_end.start - token_pos_start.start - token_pos_end.lenght)



class Token:
    """
    Represents a token in the source code.
    """
    def __init__(self, signature: TokenSignature, value: str, position: TokenPosition) -> 'Token':
        """
        Initialize a Token.

        Args:
            signature (TokenSignature): The token's signature.
            value (str): The token's value.
            position (TokenPosition): The token's position in the source code.
        """
        self.__signature = signature
        self.__value = value
        self.__position = position

    @property
    def signature(self) -> str:
        """Get the token's signature."""
        return self.__signature

    @property
    def value(self) -> str:
        """Get the token's value."""
        return self.__value

    @property
    def position(self) -> TokenPosition:
        """Get the token's position."""
        return self.__position



def signature_convert(token: Token) -> Token:
    """
    Convert a token's signature based on its value.

    Args:
        token (Token): The token to convert.

    Returns:
        Token: A new token with the converted signature.
    """
    if token.signature == TokenSignature.STRING:
        return token
    elif token.signature == TokenSignature.NUMBER:
        return token
    elif token.signature in [TokenSignature.OPERATOR, TokenSignature.WORD, TokenSignature.BRACKET]:

        for signature in SIGNATURES:
            if signature.value == token.value:
                dummy_token = Token(
                    copy(signature.signature),
                    token.value, 
                    token.position
                )
                return dummy_token
        return Token(
            token.signature,
            token.value, 
            token.position
        )