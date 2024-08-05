from copy import copy
from colorama import Fore

class TokenSignature:
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
    OPERATOR_COMMA = 'COMMA'
    OPERATOR_DOT = 'DOT'
    OPERATOR_SMALLEST = 'SMALLEST'
    OPERATOR_BIGGEST = 'BIGGEST'
    OPERATOR_SMALLEST_EQUAL = 'SMALLEST_EQUAL'
    OPERATOR_BIGGEST_EQUAL = 'BIGGEST_EQUAL'
    OPERATOR_PER = 'PER'
    OPERATOR_STRELA_RIGHT = 'STRELA_RIGHT'

    OPERATOR_EQUAL_EQUAL = 'EQUAL_EQUAL'
    OPERATOR_NOT_EQUAL = 'NOT_EQUAL'
    OPERATOR_AND = 'AND'
    OPERATOR_OR = 'OR'


    # keywords
    KEYWORD_VAR = 'VAR'
    KEYVORD_LET = 'LET'
    KEYVORD_MUT = 'MUT'
    KEYVORD_IF = 'IF'
    KEYVORD_ELSE = 'ELSE'
    KEYVORD_FOR = 'FOR'
    KEYWORD_WHILE = 'WHILE'
    KEYWORD_FUN = 'FUN'
    KEYVORD_IN = 'IN'
    KEYWORD_RETURN = 'RETURN'
    KEYWORD_LAMBDA = 'LAMBDA'
    KEYWORD_DEL = 'DEL'
    KEYWORD_USING = 'USING'
    KEYWORD_TRY = 'TRY'
    KEYWORD_CATCH = 'CATCH'
    
class SignatureObject:
    def __init__(self, signature: TokenSignature, value: str) -> None:
        self.__signature = signature
        self.__value = value

    @property
    def signature(self) -> str: return self.__signature

    @property
    def value(self) -> str: return self.__value


SIGNATURES = [
    SignatureObject(TokenSignature.KEYVORD_LET, 'let'),
    SignatureObject(TokenSignature.KEYWORD_VAR, 'var'),
    SignatureObject(TokenSignature.KEYVORD_MUT, 'mut'),
    SignatureObject(TokenSignature.KEYVORD_IF, 'if'),
    SignatureObject(TokenSignature.KEYVORD_ELSE, 'else'),
    SignatureObject(TokenSignature.KEYVORD_FOR, 'for'),
    SignatureObject(TokenSignature.KEYWORD_WHILE, 'while'),
    SignatureObject(TokenSignature.KEYWORD_FUN, 'fun'),
    SignatureObject(TokenSignature.KEYVORD_IN, 'in'),
    SignatureObject(TokenSignature.KEYWORD_DEL, 'del'),
    SignatureObject(TokenSignature.KEYWORD_LAMBDA, 'lambda'),
    SignatureObject(TokenSignature.KEYWORD_RETURN, '|>'),
    SignatureObject(TokenSignature.KEYWORD_USING, 'using'),
    SignatureObject(TokenSignature.KEYWORD_TRY, 'try'),
    SignatureObject(TokenSignature.KEYWORD_CATCH, 'catch'),

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
    

    SignatureObject(TokenSignature.BRACKET_LEFT_STANDART, '('),
    SignatureObject(TokenSignature.BRACKET_RIGHT_STANDART, ')'),
    SignatureObject(TokenSignature.BRACKET_LEFT_RECT, '['),
    SignatureObject(TokenSignature.BRACKET_RIGHT_RECT, ']'),
    SignatureObject(TokenSignature.BRACKET_LEFT_CURLY, '{'),
    SignatureObject(TokenSignature.BRACKET_RIGHT_CURLY, '}'),
]


class TokenPosition:
    def __init__(self, line: int, start: int, lenght: int) -> 'TokenPosition':
        self.__line = line + 1
        self.__start = start
        self.__lenght = lenght

    @property
    def line(self) -> int: return self.__line

    @property
    def start(self) -> int: return self.__start

    @property
    def lenght(self) -> int: return self.__lenght

    def __str__(self) -> str:
        return f'(line {Fore.MAGENTA}{self.line}{Fore.RESET} : pos {Fore.MAGENTA}{self.start+self.lenght}{Fore.RESET})'
    
def TokensLinePos(token_pos_start: TokenPosition, token_pos_end: TokenPosition):
    return TokenPosition(token_pos_start.line - 1, token_pos_start.start, token_pos_end.start - token_pos_start.start - token_pos_end.lenght)



class Token:
    def __init__(self, signature: TokenSignature, value: str, position: TokenPosition) -> 'Token':
        self.__signature = signature
        self.__value = value
        self.__position = position

    @property
    def signature(self) -> str: return self.__signature

    @property
    def value(self) -> str:  return self.__value

    @property
    def position(self) -> TokenPosition: return self.__position



def signature_convert(token: Token):
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