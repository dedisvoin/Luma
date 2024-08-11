![logo](https://github.com/user-attachments/assets/b4e9a51f-a58e-4fc1-b308-26103aa10dcb)

# Как устроен язык программирования Luma?
##### в этой документации вы узнаете как работает конвеер который из обычного текста собирает работающию программу.

#### всего я выделил столько этапов построения.

- синтаксический анализ
- - разбиение кода на составляющие языка, их мы будем называть токенами. к ним относятся различные символы, последовательности символов, целые слова и словестные конструкции.
- - устанока каждому токену своего идентификатора для дальнейшего опознания.
- построение абстрактного синтаксического дерева. (compilation)
- - генерация нод
- - создание класса памяти для run time
- - разбиение токенов на группы по опредеоенным правилам синтаксиса нашего языка.
- - парсинг данных токенов посредством рекурсивного спуска (об этом мы поговорим в дальнейшем).
- - добавление ветвей в единый механизм запуска


- проверка на наличие ошибок в ветвях дерева на стадии парсинга.
- запуск главной ветви программы. (execution)
- - проверка ветви на наличие ошибок на стадии исполнения.
- - ичполнение данной ветви.
  
















# Стадия 1.0 - синтаксический анализ
#### для данной стадии нам понадобится два файла:

`loader.py` - в нем хранится код загрузчика 
`tokenizer.py` - тут находится сам класс токенизатора

##### разберем эти файлы по подробнее.
```py
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
   
```

для того чтобы было удобно в дальнейшем работать с файлами нашего языка мы будем представлять их отдельным классом.
```py
class LumaFile:
    def __init__(self, code: str, code_file: str, code_lenght: str) -> None:
        self.code = code
        self.code_file = code_file
        self.code_lenght = code_lenght
        self.code_to_lines = self.code.split('\n')
```
##### он будет принимать 3 атрибута
`code` - код в его строковом представлении
`code_file` - полный путь к файлу кода
`code_lenght` - длина кодовой строки

##### при инициализации мы добавим еще одино поле `code_to_lines` в котором будем хрнаить наш код построчно разбитый символом `/n` для дальнейшего пользования (поиска индекса данной строки).

##### для самой же загрузки файла добавим отдельную функцию `LoadLumaFile` принимающую лишь один аргумент `file_name` - путь к файлу.
##### для начала нам протребуется проверить расширение нашего файла. если оно не соответствует расширению нашего языка то выбрасываем соответствующую ошибку хранящуюся в файле `src.debug.loader`. мы импортируем его с именем `debug_loader`.

при успешном соответствии выбрасываем сообщение об успехе.
далее открываем наш файл в режиме чтения и считываеи оттуда данные построчно
потом соединям их обратно в одну строку символом `/n`. И узнаем длину этой строки.
в конце просто собираем все данные в обьект и возвращаем.

```py
if file_name.split('.')[-1] == 'lm':
    debug_loader.debug_file_load_succes.out_funct = lambda file_name: print(f'File {Fore.YELLOW}{file_name}{Fore.RESET}.')
    debug_loader.debug_file_load_succes(file_name)
else:
    debug_loader.debug_file_load_error.out_funct = lambda file_name: print(f'File {Fore.YELLOW}{file_name}{Fore.RESET} extension is not {Fore.YELLOW}".lm"{Fore.RESET}')
    debug_loader.debug_file_load_error(file_name)

__code = ''.join(open(file_name, 'r').readlines()) + '\n'   # считываем стоки заодно соединяя их
__code_lenght = len(__code)                                 # узнаем длину всей последовательности

return LumaFile(__code, file_name, __code_lenght)           # в конце не забываем возвратить обьект файла нашего языка
```
на этом функционал данного файла оканчивается. Он содержит лишь код загрусчика.

# Стадия 1.1 - разбиение кода на стоставные языка

##### тут нам понадобится создать еще один файл `tokenizer.py` в нем мы пропишем всю логику 1 этапа.
##### для начала создадим папку ядра `core` куда будем складывать все основные файлы кода нашего языка.
##### и первым файлом который мы туда добавим будет файл `lexems.py` где пропишем все символы которые будут использоваться в нашем языке.
он будет выглядеть так:
```py
# Alphabetic characters (lowercase and uppercase)
CHARS = 'abcdefghigklmnopqrstuvwxyz' + 'abcdefghigklmnopqrstuvwxyz'.upper()

# Numeric characters
NUMBERS = '1234567890'

# Special symbols and operators
SYMVOLS = '~-+*/=|<>%$#@!&,;.:'

math_operations = '+-*/=%'

# Underscore character
THUNDER = '_'

# Bracket characters
BRACKETS = '{}[]()'

# Dot character
DOT = '.'

# Quote characters for string literals
MARKS = ['"', "'"]
```

вроде-бы ничего сложного да. мы просто обьеденим символы в особые группы для дальнейшего удобного пользования ими.

##### теперь там-же в ядре создадим еще один файл `tokens.py` где опишем класс токена и все что с ним связано.

для начала создадим дата класс где будем хранить сигнатуры сигнатуры токенов
```py
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
```
##### первые 8 типов сигнатур (`NUMBER`,`WORD`,`STRING`,`OPERATOR`,`BRACKET`,`EOF`,`TRUE`,`FALSE`) - они появляются после первой стадии токенизации. теперь по подробнее разберем эти сигнатуры.
- `NUMBER` - сигнатура числа (`0`, `12`, `0.12324` и тд)
- `WORD` - сигнатура любой символьной комбинации (`hello`, `var`, `number_one`, и тд)
- `STRING` - сигнатура строки (`'Hello, world!'`, `'i am 18 years old'`, и тд)
- `OPERATOR` - сигнатура операторов (`=`, `==`, `+`, `-`, `->`, `<-`, `:`, `,`, и тд)
- `BRACKET` - сигнатура всех видов скобок (`(`, `{`, `[`, и их пары)
- `EOF` - сигнатура окончания файла (необходима для корректной работы парсера) (добавляется в конец всех сигнатур)
- `TRUE`, `FALSE` - сигнатура неизменяемых булевых значений (`true`, `false`)

##### далее мы опишем класс обьекта сигнатуры.
##### он будет принимать два аргумента:
`signature` - сама сигнатура с которой будет представлятся полученное значение
`value` - само значение обьекта с указанной сигнатурой
##### ну и добавим еще методы для доступа к данным приватным полям
```py
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
    def signature(self) -> str:             # метод доступа
        """Get the token signature."""
        return self.__signature

    @property
    def value(self) -> str:                 # метод доступа
        """Get the token value."""
        return self.__value
```

##### и в отдельном массиве опишем сигнатуры для каждого обьекта языка

```py
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
```
эти сигнатуры будут использоваться в дальнейшем для построения абстрактного синтаксического дерева (ast).

не забудем добваить метод для получения сигнатуры по его строковому значению.
```py
def get_signature(string: str):
    for signature in SIGNATURES:
        if signature.value == string:
            return signature            # возвратит нам обьект сигнатуры
```

##### для удобного поиска ошибок в коде мы должны знать на какой позиции (индекс строки, поизиция в строке) находимся в данный момент или же на каком токене. для этого опишем особый класс.
##### он будет принимать и хранить 3 атрибута:
`line` - строка в которой находится данный токен
`start` - позиция первого символа данного токена в данной строке
`lenght` - длина токена в символах
```py
class TokenPosition:
    """
    Represents the position of a token in the source code.
    """
    def __init__(self, line: int, start: int, lenght: int) -> 'TokenPosition':
        """
        Initialize a TokenPosition.

        Args:
            line (int): The line number (1-indexed).
            start (int): The starting position of the token.
            lenght (int): The length of the token.
        """
        self.__line = line
        self.__start = start
        self.__lenght = lenght
```
не забудем добавить методы для доступа
```py
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

```
и еще опишем тандер функцию `__str__` чтобе при выводе позиции она печаталась в понятном формате
```py
    def __str__(self) -> str:
        """
        Return a string representation of the token position.

        Returns:
            str: A formatted string with line and position information.
        """
        return f'(line {Fore.MAGENTA}{self.line + 1}{Fore.RESET} : pos {Fore.MAGENTA}{self.start}{Fore.RESET} : lenght {Fore.MAGENTA}{self.lenght}{Fore.RESET})'
```
##### на этом класс `TokenPosition` оканчивается, все понятно и просто.

##### но как нам найти позицию между двумя токенами? эту проблему решим так-же отдельным классом:
```py
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
```
##### думаю тот обьяснять ничего не нужно.

##### и наконец давайте опишем класс самого токена, ну тут тоже все интуитивно понятно.
`signature` - сигнатура токена
`value` - значение токена
`position` - позиция токена в нашем коде

```py
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
```
##### на этом мы закончим с файлом `tokens.py` и перейдем обратно к реализации самого токенизатора.

##### для начала в файле `tokenizer.py` импортируем все нобходимые классы и методы
```py
import sys
sys.path.extend('../') # добавим данный путь в глобальную облость видимости

from copy import copy

from src.core import tokens     # |
from src.core import lexems     # | - импортируем все ранее написанные файлы
from src.analize import loader  # |
```

опишем сам класс токенизатора и его конструктор
```py
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
```
`self.__pos = 0` - позиция токенизатора относительно начала файла
`self.__this_line = 0` - строка в которой находится токенизатор
`self.__this_pos = 0` - позиция токенизатора относительно начала строки
`self.__tokens: list[tokens.Token] = []` - массив токенов первого порядка
`self.__standart_tokens: list[tokens.Token] = []` - массив токенов второго порядка
`self.__file = None` - поле для хранения обьекта файла (в начале оно пустое)

> все эти поля приватные так-как малейшее вмешательство в данный класс может привести к сбою его работы

добавим несколько вспомогательный методов
```py
    @property
    def basic_tokens(self) -> list[tokens.Token]: # дает доступ к токенам первого порядка
        """
        Get the list of basic tokens.

        Returns:
            list[tokens.Token]: The list of basic tokens.
        """
        return self.__tokens
    
    @property
    def standert_tokens(self) -> list[tokens.Token]: # дает доступ к токенам второго порядка
        """
        Get the list of standard tokens.

        Returns:
            list[tokens.Token]: The list of standard tokens.
        """
        return self.__standart_tokens

    @property
    def file(self) -> str: # дает доступ к обьекту файла кода
        """
        Get the name of the file being tokenized.

        Returns:
            str: The name of the file.
        """
        return self.__file
    
    @file.setter
    def file(self, value: loader.LumaFile): # устанаваливает обьект файла кода
        """
        Set the name of the file being tokenized.

        Args:
            value (str): The name of the file.
        """
        self.__file = value

    def reinit(self): # переинициализирует позицию токенизатора
        """
        Reinitialize the Tokenizer, clearing the code and resetting the position.
        """
        self.__pos = 0
```

для перемещения токенизатора вперед по коду добавим данный метод
```py
    def next_sym(self):
        """
        Move to the next symbol in the code.
        """
        self.__this_pos += 1 
        if self.get_sym() == '\n':
            self.__this_line += 1
            self.__this_pos = 0
        self.__pos += 1
```
при его вызове виртуальная позиция токенизатора будет перемещаться на 1 символ вперед. если при передвижении он найдет символ `/n` то это будет означать что он перешел на другую строку при этом мы увеличим `self.__this_line` на 1 и обнулим позицию в данной строке `self.__this_pos = 0`

также добавим метод для возвражения на прежний символ
```py
    def before_sym(self):
        """
        Move to the previous symbol in the code.
        """
        self.__pos -= 1
        self.__this_pos -=1
```
ну тут ничего сложного.

добавим метод для получени символа по его позиции в коде
```py
    def get_sym(self, offset: int = 0) -> str:
        """
        Get the symbol at the current position plus an optional offset.

        Args:
            offset (int, optional): The offset from the current position. Defaults to 0.

        Returns:
            str: The symbol at the specified position.
        """
        return self.__file.code[self.__pos + offset]
```
> заметьте, параметр `offset` добваляет смещение для вертуальной позиции для того чтобы узнать какие символы окружают (слева и справа) наш токенизатор.
>
теперь самые важные методы, методы проверки на принадлежность тем или иным лексемам

```py
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
```
> методы `is_comment_basic_start`, `is_comment_multiline_start` необходимы для дольнейшей токенизации комментариев.

### теперь пойдут сами методы токенизации, это самое веселое.

---

#### - метод токеницации слова (или-же словосочетания с использованием символа `_`)
```py
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
```
мы просто добавляем символы в буфер пока они принадлежать либо лексемам `char` `number` `_`
> лексема `number` может быть использована в этом методе токенизации если только буфер уже чем то заполнен.

в конце формируем токен и добавляем его в массив токенов первого порядка.

---

#### - метод токеницации числа
```py
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
```
тут так-же как и при токенизации слова, только в буфер добавляются только лексемы `number` и `.`

в конце формируем токен и добавляем его в массив токенов первого порядка.

---

#### - метод токеницации теста
```py
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
```
тут так-же как и при токенизации слова, толко символы начнут добавляться в буфер только после нахождения символа `'` или `"` и перестанут добавляться так-же при их нахождении уже во второй раз.

в конце формируем токен и добавляем его в массив токенов первого порядка.

---

#### - метод токеницации различных операторов
```py
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
```
тут так-же как и при токенизации слова или числа, но добавляются лишь символы соответствующие лексеме `operator`.

в конце формируем токен и добавляем его в массив токенов первого порядка.

---

#### - метод токеницации различных скобок
```py
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
```
так как скобка это одиночный символ мы можем просто сразу создать обьект токена, призвоить ему данную скобку в качестве значения, и добавить его в массив токенов первого порядка предварительно указав сигнатуру `BRACKET`

---

#### - метод токеницации различных типов комментариев
```py
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
```
ну тут обьяснять думаю не обязательно.

---


##### далее мы просто запускаем цыкл и вызываем эти методы по очереди, предварительно очистив наш массив первичных токенов `self.__tokens.clear()`
```py
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
```

---

#### вот небольшой тестовый код на нашем языке:
```kt
var name = 10;
val age = [1, 2, 3] + 'Hello';
```


при вызове функции `tokenize`, предварительно загрузив данный код, мы получим список первичных токенов. если его красиво вывести он будет выглядеть так.

```
                       значение токена   |                                  позиция в коде   |                                        сигнатура
-----------------------------------------------------------------------------------------------------------------------------------------------
 token:                            var   |   pos:              (line 1 : pos 0 : lenght 3)   |   name:                                     WORD
 token:                           name   |   pos:              (line 1 : pos 4 : lenght 4)   |   name:                                     WORD
 token:                              =   |   pos:              (line 1 : pos 9 : lenght 1)   |   name:                                 OPERATOR
 token:                             10   |   pos:             (line 1 : pos 11 : lenght 2)   |   name:                                   NUMBER
 token:                              ;   |   pos:             (line 1 : pos 13 : lenght 1)   |   name:                                 OPERATOR
 token:                            val   |   pos:              (line 2 : pos 0 : lenght 3)   |   name:                                     WORD
 token:                            age   |   pos:              (line 2 : pos 4 : lenght 3)   |   name:                                     WORD
 token:                              =   |   pos:              (line 2 : pos 8 : lenght 1)   |   name:                                 OPERATOR
 token:                              [   |   pos:             (line 2 : pos 10 : lenght 1)   |   name:                                  BRACKET
 token:                              1   |   pos:             (line 2 : pos 11 : lenght 1)   |   name:                                   NUMBER
 token:                              ,   |   pos:             (line 2 : pos 12 : lenght 1)   |   name:                                 OPERATOR
 token:                              2   |   pos:             (line 2 : pos 14 : lenght 1)   |   name:                                   NUMBER
 token:                              ,   |   pos:             (line 2 : pos 15 : lenght 1)   |   name:                                 OPERATOR
 token:                              3   |   pos:             (line 2 : pos 17 : lenght 1)   |   name:                                   NUMBER
 token:                              ]   |   pos:             (line 2 : pos 18 : lenght 1)   |   name:                                  BRACKET
 token:                              +   |   pos:             (line 2 : pos 20 : lenght 1)   |   name:                                 OPERATOR
 token:                          Hello   |   pos:             (line 2 : pos 23 : lenght 5)   |   name:                                   STRING
 token:                              ;   |   pos:             (line 2 : pos 29 : lenght 1)   |   name:                                 OPERATOR
```

на этом этап 1.1 заканчивается.

# Стадия 1.2 - установка идентификаторов

#### установка идентификаторов превратит токены первого порядка в токены второго порядка. что позволит парсеру лучше понимать суть кода.

данная стадия самая простая, ведь нам нужно лишь соотнести токены первого порядка сигнатурам токенов второго порядка.
для этого в класс `Tokenizer` добавим следующую функцию.

```py
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
```
название функции говорит само за себя. оно само переконыеритрует токены первого порядка в токены второго порядка. в конце добавив тот самый токен с сигнатурой `EOF`.

тепер после конвертации наши токены будут выглядеть так:
```
                       значение токена   |                                  позиция в коде   |                                        сигнатура
-----------------------------------------------------------------------------------------------------------------------------------------------
 token:                            var   |   pos:              (line 1 : pos 0 : lenght 3)   |   name:                                      VAR
 token:                           name   |   pos:              (line 1 : pos 4 : lenght 4)   |   name:                                     WORD
 token:                              =   |   pos:              (line 1 : pos 9 : lenght 1)   |   name:                                    EQUAL
 token:                             10   |   pos:             (line 1 : pos 11 : lenght 2)   |   name:                                   NUMBER
 token:                              ;   |   pos:             (line 1 : pos 13 : lenght 1)   |   name:                            DOT_AND_COMMA
 token:                            val   |   pos:              (line 2 : pos 0 : lenght 3)   |   name:                                      VAL
 token:                            age   |   pos:              (line 2 : pos 4 : lenght 3)   |   name:                                     WORD
 token:                              =   |   pos:              (line 2 : pos 8 : lenght 1)   |   name:                                    EQUAL
 token:                              [   |   pos:             (line 2 : pos 10 : lenght 1)   |   name:                        BRACKET_LEFT_RECT
 token:                              1   |   pos:             (line 2 : pos 11 : lenght 1)   |   name:                                   NUMBER
 token:                              ,   |   pos:             (line 2 : pos 12 : lenght 1)   |   name:                                    COMMA
 token:                              2   |   pos:             (line 2 : pos 14 : lenght 1)   |   name:                                   NUMBER
 token:                              ,   |   pos:             (line 2 : pos 15 : lenght 1)   |   name:                                    COMMA
 token:                              3   |   pos:             (line 2 : pos 17 : lenght 1)   |   name:                                   NUMBER
 token:                              ]   |   pos:             (line 2 : pos 18 : lenght 1)   |   name:                       BRACKET_RIGHT_RECT
 token:                              +   |   pos:             (line 2 : pos 20 : lenght 1)   |   name:                                     PLUS
 token:                          Hello   |   pos:             (line 2 : pos 23 : lenght 5)   |   name:                                   STRING
 token:                              ;   |   pos:             (line 2 : pos 29 : lenght 1)   |   name:                            DOT_AND_COMMA
 token:                            eof   |   pos:           (line -1 : pos -1 : lenght -1)   |   name:                                      EOF
```
заметьте сами значения токенов не поменялись, поменялись лишь их сигнатуры, ну и так же добавился токен конца файла `EOF` с его специфической позицией.

> такая позиция нужна токену `EOF` чтобы мы могли легко найти его среди остальных токенов.

на этом стадия синтаксического анализа заканчивается (самое простое позади).

# Стадия 2.0 - построение абстрактного синтаксического дерева или же компиляция
для того чтобы исполнить наш код его сначала необходимо скомпилировать, то-есть превратить в набор команд которые после мы передадим исполнителю.

# Стадия 2.1 - генерация нод
самая главная нода - корневая нода (по аналогии с деревом). от нее исодят остальные ноды.
чтобы запустить любой код достаточно лишь вызвать корневую ноду и все остальные ноды сами рекурсивно будут вызываться.
##### пример разбиения на ноды:

```
                                                                        var age = 10 - 20 * 5;
                                                                        ^^^^^^^^^ ^^^^^^^^^^^
                                                                            /          \
1) тут бы разбиваем на две ноды   --------------------------------   var age     =   10 - 20 * 5
                                                                                     ^^   ^^^^^^  
                                                                                     /        \
2) тут еще две ноды   ----------------------------------------------------------   10    -    20 * 5
                                                                                              ^^   ^
                                                                                            /       \
3) тут еще две   ----------------------------------------------------------------------   20    *     5

```                
чем ниже выше поднимаются ветви, тем сильнее их приоритет выполнения возрастает ( тут схема перевернута ).
> у нод нет единого класса, так-как функционал каждой ноды уникален ( одна складывает значения двух других нод, другая записывает значения в память, другая читает и тд). поэтому каждую ноду необходимо писать самостоятельно.   
>   
всего ноды делятся на два вида, `statements nodes` - (ноды состояния), `expressions nodes` - (ноды выражений).
'ноды состояния' - можно вызвать (выполняют какую либо команду)
'ноды выражений' - можно вычислить (вызвать и получить какой-то результат)

##### напирмер:

```

эта нода состояния, она может обращаться к памяти и      а эта нода выражения ее можно вычислить и 
      записывать в нее какое либо значение                     и получить результат
                                       |                        |
                                    ~~~~~~~               ~~~~~~~~~~~
                                    var age       =       10 - 20 * 5
                                                          ^^   ^^^^^^
                                                        /          \
                                                       10          20 * 5 - эта тоже нода выражения
                                                        \
                                                         даже просто число является нодой выражения,
                                                    так-как ее тоже можно вычислить и получить результат.
                                                               в данном случаем результат 10
```

---

#### перейдем к написанию самого кода

создадим папку `parse` а в нем файл `nodes.py`.

в нем мы будем хранить два класса: 
- класс нод выражений
- класс нод состояний
  
```py
class Statements:
    ...

class Expressions:
    ...
```

и еще добавим базовый класс выражения, от которого потом будем наследовать все остальные ноды выражений

```py
class BaseExpression:
    def __init__(self, file, pos) -> None:
        self.file = file
        self.pos = pos

    def eval(self):
        ...
```
пока для родителя выражений нужен лишь файл кода и позиция данного выражения в коде, но наследования мы будем добавлять дополнительные атрибуты.
> метод `eval` будет возвращать результат ноды

добавим несколько нод но их функционал напишем позже.

---

#### Нода записи значения в память ( инициальзация переменной )
```py
class Statements:

    ...

    class NodeVariableSet:
        def __init__(self, var_name: str, var_mutable: memory.MemoryObjectTypes, var_expression, memory: memory.Memory ) -> None:
            self.__name = var_name
            self.__mutable = var_mutable
            self.__expression = var_expression
            self.__memory = memory

        def exec(self):
            ...
            # тут будет функционал записи обьекта в виртуальную память
    
    ...

```
`var_name` - назмание переменной (ее идентификатор в памяти)
`var_mutable` - будет ли наша переменная изменяемой
`var_expression` - нода выражения которую необходимо будет вычислить
`memory` - обьект виртуальной памяти куда будет помещена переменная

---
#### Нода вывода значения в консоль
```py
class Statements:

    ...

    class NodeOut:
        def __init__(self, vars_expressions: list) -> None:
            self.__vars_expressions = vars_expressions

        def exec(self):
            ...
            # тут будет функционал вывода
    
    ...

```
`vars_expressions` - массив выражений которые необходимо вычислить и вывести в консоль

---
#### Нода создания числа, является вершинной нодой
> вершинаая нода - нода на которой рекурсивный спуск останавливается (конечная, неделимая ветвь для парсера)
```py
class Expressions:

    ...

    class NodeNumberCreate(BaseExpression):
            def __init__(self, value: str, file, pos) -> None:
                super().__init__(file, pos)
                py_number = luma_types.GetPyNumberForString(value)
                if isinstance(py_number, int):
                    self.__value = luma_values.L_Int.set_value(py_number)
                elif isinstance(py_number, float):
                    self.__value = luma_values.L_Float.set_value(py_number)

            def eval(self):         # метод вычисления - значит она является нодой выражения
                return self.__value

    ...
    
```
тот что написано в конструкторе этой ноды будет обьяснено далее, но кратко - тут мы при помощи метода `GetPyNumberForString` из строки извлекаем число и узнавая тип этого числа конвертируем его в нужное значение нашего языка с базовым типом.

пока на этом остановимся и перейдем к самому парсеру.
в папке `parse` создадим файл `parser.py` и добавми в него следующий код.

```py
from colorama import Fore

from src.debug import debug                 # тут мы импортируем файл содержащий инструкции для дебага его про него поговорим далее
from src.parse import nodes                 # импортируем файл с нодами

from src.core import tokens                 # импортируем функции ядра
from src.core import memory
from src.core import luma_excepts
from src.core import luma_argmunets

from src.analize import loader              # код из анализатора нам тоже понадобится


class Parser:
    def __init__(self) -> None:
        self.__tokens = []
        self.__nodes = []
        self.__pos = 0
        self.__run_time_memory = memory.Memory()
        self.__file = None
        self.__debug = False

    @property
    def debug(self) -> bool: return self.__debug # доступ к полю debug

    @debug.setter
    def debug(self, value: bool): # установка поля debug
        self.__debug = value

    @property
    def run_time_memory(self) -> memory.Memory: # доступ к памяти времени выполнения
        return self.__run_time_memory

    @property
    def file(self) -> loader.LumaFile: # доступ к файлу кода
        return self.__file
    
    @file.setter
    def file(self, value: loader.LumaFile): # установка поля файла
        self.__file = value

    @property
    def nodes(self) -> list[nodes.Statements]: # доступ к нодам
        return self.__nodes

    @property
    def code_tokens(self) -> list[tokens.Token]: # доступ к токенам
        return self.__tokens
    
    @code_tokens.setter
    def code_tokens(self, tokens: list[tokens.Token]): # установка поля токенов
        self.__tokens = tokens

    def next_token(self): # переместиться на следующий токен
        self.__pos += 1

    def before_token(self): # переместиться на предыдущий токен
        self.__pos -= 1

    def get_token(self, offset: int = 0): # плучить токен 
        return self.__tokens [self.__pos + offset]
    
    def get_token_signature(self, offset: int = 0) -> tokens.TokenSignature: # получить сигнатуру токена
        return self.get_token(offset).signature
    
    def get_token_value(self, offset: int = 0) -> str: # получить значение токена
        return self.get_token(offset).value
    
    def get_token_position(self, offset: int = 0) -> tokens.TokenPosition: # получить позицию токена
        return self.get_token(offset).position
```

класс `Parser` содержит следующие приватные поля:
- `self.__tokens = []` - массив в котором будут храниться токены второго порядка
- `self.__nodes = []` - массив куда будут помещаться сгенерированные ноды
- `self.__pos = 0` - позиция парсера
- `self.__run_time_memory = memory.Memory()` - обьект виртуальной памяти времени выполнения
- `self.__file = None` - файл кода
- `self.__debug = False` - будет ли выводиться отладочная информация

добавим еще пару методов

---

##### метод проверки токена на совпадение с указанной сигнатурой
`signature` - сигнатура с которой будем сравнивать токен
```py
    def is_token_signature(self, signature: tokens.TokenSignature, offset: int = 0) -> bool:
        return self.get_token_signature(offset) == signature
```

---

##### метод проверки токена на совпадение со списком сигнатур
`signatures` - список сигнатур с которыми будет сравниваться токен
```py
    def is_token_signatures(self, signatures: list[tokens.TokenSignature], offset: int = 0) -> bool:
        for signature in signatures:
            if self.is_token_signature(signature, offset):
                return True
        return False
```

---

##### метод перехода на следующий токен если этот токен соответствует указзанной сигнатуре
`signature` - сигнатура с которой будем сравнивать токен
```py
    def match_token_signature(self, signature: tokens.TokenSignature, offset: int = 0):
        if self.is_token_signature(signature, offset):
            self.next_token()
            return True
        return False
```

---

##### метод перехода на следующий токен если этот токен соответствует хотя-бы одной сигнатуре из списка
`signatures` - список сигнатур с которыми будет сравниваться токен
```py
    def match_token_signatures(self, signatures: list[tokens.TokenSignature]) -> bool:
        for signature in signatures:
            if self.is_token_signature(signature):
                self.next_token()
                return True
        return False
```
