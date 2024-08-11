import time
from colorama import Fore

from src.debug import debug
from src.parse import nodes

from src.core import tokens
from src.core import memory
from src.core import luma_excepts
from src.core import luma_argmunets

from src.analize import loader




class Parser:
    def __init__(self) -> None:
        self.__tokens = []
        self.__nodes = []
        self.__pos = 0
        self.__run_time_memory = memory.Memory()
        self.__file = None
        self.__debug = False

    @property
    def debug(self) -> bool: return self.__debug

    @debug.setter
    def debug(self, value: bool):
        self.__debug = value


    @property
    def run_time_memory(self) -> memory.Memory:
        return self.__run_time_memory

    @property
    def file(self) -> loader.LumaFile:
        return self.__file
    
    @file.setter
    def file(self, value: loader.LumaFile):
        self.__file = value

    @property
    def nodes(self) -> list[nodes.Statements]:
        return self.__nodes

    @property
    def code_tokens(self) -> list[tokens.Token]:
        return self.__tokens
    
    @code_tokens.setter
    def code_tokens(self, tokens: list[tokens.Token]):
        self.__tokens = tokens

    def next_token(self):
        self.__pos += 1

    def before_token(self):
        self.__pos -= 1

    def get_token(self, offset: int = 0):
        return self.__tokens [self.__pos + offset]
    
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
    
    def match_token_signatures(self, signatures: list[tokens.TokenSignature]) -> bool:
        for signature in signatures:
            if self.is_token_signature(signature):
                self.next_token()
                return True
        return False
    
    def match_and_wait(self, signature: tokens.SignatureObject, offset: int = 0):
        if self.match_token_signature(signature.signature, offset):
            ...
        else:
            luma_excepts.call_exception_wait(self.__file, signature, self.get_token_position(-1))
        
    def is_token_and_wait(self, signature: tokens.SignatureObject, offset: int = 0):
        if self.is_token_signature(signature.signature, offset):
            ...
        else:
            luma_excepts.call_exception_wait(self.__file, signature, self.get_token_position(-1))
            
    def parse_statement(self):
        # variables declaration
        if self.is_token_signature(tokens.TokenSignature.KEYWORD_VAR) or self.is_token_signature(tokens.TokenSignature.KEYWORD_VAL):
            self.match_token_signatures([tokens.TokenSignature.KEYWORD_VAR, tokens.TokenSignature.KEYWORD_VAL])
            mutable = memory.MemoryObjectTypes.mutable if self.match_token_signature(tokens.TokenSignature.KEYWORD_MUT) else memory.MemoryObjectTypes.unmutable
            self.is_token_and_wait(tokens.SignatureObject(tokens.TokenSignature.WORD, 'variable name'))
            name = self.get_token_value()
            self.match_token_signature(tokens.TokenSignature.WORD)
            if self.is_token_signature(tokens.TokenSignature.OPERATOR_DOT_AND_COMMA):
                expression = None
                return nodes.Statements.NodeVariableSet(name, mutable, expression, self.__run_time_memory)
            else:
                self.match_and_wait(tokens.get_signature('='))
                expression = self.parse_expression()
                self.is_token_and_wait(tokens.get_signature(';'))
                return nodes.Statements.NodeVariableSet(name, mutable, expression, self.__run_time_memory)
            
        # out command
        if self.is_token_signature(tokens.TokenSignature.WORD) and self.get_token_value() == 'out':
            self.match_token_signature(tokens.TokenSignature.WORD)
            expressions = []
            i = 0
            while not self.is_token_signature(tokens.TokenSignature.OPERATOR_DOT_AND_COMMA):
                expr = self.parse_expression()
                expressions.append(expr)
                self.match_token_signature(tokens.TokenSignature.OPERATOR_COMMA)
                i += 1
                if i>100:
                    luma_excepts.BaseLumaException(self.__file, luma_excepts.LumaExceptionType.PARSER, f'Waited {Fore.YELLOW}"{tokens.get_signature(';').value}"{Fore.RESET} signature')(
                        tokens.TokenPosition(self.get_token_position(-1).line, self.get_token_position(-1).start + self.get_token_position(-1).lenght, 1)
                    )
                
            return nodes.Statements.NodeOut(expressions)
        
        # base variable chainge
        if self.is_token_signature(tokens.TokenSignature.WORD) and self.is_token_signature(tokens.TokenSignature.OPERATOR_EQUAL, 1):
            name = self.get_token_value()
            start_var_name_pos = self.get_token_position()
            self.match_token_signature(tokens.TokenSignature.WORD)
            end_var_name_pos = self.get_token_position()
            self.match_token_signature(tokens.TokenSignature.OPERATOR_EQUAL)
            if self.is_token_signature(tokens.TokenSignature.OPERATOR_DOT_AND_COMMA):
                luma_excepts.call_exception_wait(self.__file, tokens.SignatureObject(tokens.TokenSignature.WORD, 'expression'), self.get_token_position(-1))
            else:
                expression = self.parse_expression()
                self.is_token_and_wait(tokens.get_signature(';'))
                return nodes.Statements.NodeBaseVariableUpdate(name, expression, self.__run_time_memory, self.__file, tokens.TokenPosition(start_var_name_pos.line, start_var_name_pos.start, start_var_name_pos.lenght))

    def parse_expression(self):
        return self.parse_and()
    
    def parse_and(self):
        expression = self.parse_or()
        start_pos = self.get_token_position()
        while True:
            if self.match_token_signature(tokens.TokenSignature.OPERATOR_AND):
                expression = nodes.Expressions.NodeBinareCondition('&&', expression, self.parse_equals(), self.__file, start_pos)
                continue
            break
        return expression

    def parse_or(self):
        expression = self.parse_equals()
        start_pos = self.get_token_position()
        while True:
            if self.match_token_signature(tokens.TokenSignature.OPERATOR_OR):
                expression = nodes.Expressions.NodeBinareCondition('||', expression, self.parse_equals(), self.__file, start_pos)
                continue
            break
        return expression

    def parse_equals(self):
        expression = self.parse_conditions()
        start_pos = self.get_token_position()
        while True:
            if self.match_token_signature(tokens.TokenSignature.OPERATOR_NOT_EQUAL):
                expression = nodes.Expressions.NodeBinareCondition('!=', expression, self.parse_conditions(), self.__file, start_pos)
                continue
            if self.match_token_signature(tokens.TokenSignature.OPERATOR_EQUAL_EQUAL):
                expression = nodes.Expressions.NodeBinareCondition('==', expression, self.parse_conditions(), self.__file, start_pos)
                continue
            break
        return expression

    def parse_conditions(self):
        expression = self.parse_math_binare_addit()
        start_pos = self.get_token_position()
        while True:
            if self.match_token_signature(tokens.TokenSignature.OPERATOR_BIGGEST):
                expression = nodes.Expressions.NodeBinareCondition('>', expression, self.parse_math_binare_addit(), self.__file, start_pos)
                continue
            if self.match_token_signature(tokens.TokenSignature.OPERATOR_SMALLEST):
                expression = nodes.Expressions.NodeBinareCondition('<', expression, self.parse_math_binare_addit(), self.__file, start_pos)
                continue
            if self.match_token_signature(tokens.TokenSignature.OPERATOR_SMALLEST_EQUAL):
                expression = nodes.Expressions.NodeBinareCondition('<=', expression, self.parse_math_binare_addit(), self.__file, start_pos)
                continue
            if self.match_token_signature(tokens.TokenSignature.OPERATOR_BIGGEST_EQUAL):
                expression = nodes.Expressions.NodeBinareCondition('>=', expression, self.parse_math_binare_addit(), self.__file, start_pos)
                continue
            break
        return expression

    def parse_math_binare_addit(self):
        expression = self.parse_math_binare_multi()
        start_pos = self.get_token_position()
        while True:
            if self.match_token_signature(tokens.TokenSignature.OPERATOR_PLUS):
                expression = nodes.Expressions.NodeBinareOperation('+', expression, self.parse_math_binare_multi(), self.__file, start_pos)
                continue
            if self.match_token_signature(tokens.TokenSignature.OPERATOR_MINUS):
                expression = nodes.Expressions.NodeBinareOperation('-', expression, self.parse_math_binare_multi(), self.__file, start_pos)
                continue
            break
        return expression

    def parse_math_binare_multi(self):
        expression = self.parse_math_unary()
        start_pos = self.get_token_position()
        while True:
            if self.match_token_signature(tokens.TokenSignature.OPERATOR_DIV):
                expression = nodes.Expressions.NodeBinareOperation('/', expression, self.parse_math_unary(), self.__file, start_pos)
                continue
            if self.match_token_signature(tokens.TokenSignature.OPERATOR_MUL):
                expression = nodes.Expressions.NodeBinareOperation('*', expression, self.parse_math_unary(), self.__file, start_pos)
                continue
            if self.match_token_signature(tokens.TokenSignature.OPERATOR_PER):
                expression = nodes.Expressions.NodeBinareOperation('%', expression, self.parse_math_unary(), self.__file, start_pos)
                continue
            break
        return expression
    
    def parse_math_unary(self):
        
        if self.match_token_signature(tokens.TokenSignature.OPERATOR_MINUS):
            return nodes.Expressions.NodeUnareOperation('-', self.parse_basic(), self.__file, self.get_token_position())
        if self.match_token_signature(tokens.TokenSignature.OPERATOR_PLUS):
            return nodes.Expressions.NodeUnareOperation('+', self.parse_basic(), self.__file, self.get_token_position())
        return self.parse_basic()
    
    def parse_basic(self):
        if self.is_token_signature(tokens.TokenSignature.BRACKET_LEFT_STANDART):
            self.match_token_signature(tokens.TokenSignature.BRACKET_LEFT_STANDART)
            
            if self.is_token_signature(tokens.TokenSignature.BRACKET_RIGHT_STANDART):
                luma_excepts.call_exception_wait(self.__file, tokens.SignatureObject(None, 'expression'), self.get_token_position(-1))
            expr = self.parse_expression()
            self.match_and_wait(tokens.get_signature(')'))
            return expr

        if self.is_token_signature(tokens.TokenSignature.NUMBER):
            expr = nodes.Expressions.NodeNumberCreate(self.get_token_value(), self.__file, self.get_token_position())
            self.next_token()
            return expr
        
        if self.is_token_signatures([tokens.TokenSignature.TRUE, tokens.TokenSignature.FALSE]):
            expr = nodes.Expressions.NodeBoolCreate(self.get_token_value(), self.__file, self.get_token_position())
            self.next_token()
            return expr
        
        if self.is_token_signature(tokens.TokenSignature.STRING):
            expr = nodes.Expressions.NodeStringCreate(self.get_token_value(), self.__file, self.get_token_position())
            self.next_token()
            return expr
         
        if self.is_token_signature(tokens.TokenSignature.BRACKET_LEFT_RECT):
            self.match_token_signature(tokens.TokenSignature.BRACKET_LEFT_RECT)
            expressions = []
            while not self.is_token_signature(tokens.TokenSignature.BRACKET_RIGHT_RECT):
                expressions.append(self.parse_expression())
                if not self.is_token_signature(tokens.TokenSignature.BRACKET_RIGHT_RECT) and not self.is_token_signature(tokens.TokenSignature.OPERATOR_COMMA):
                    self.match_and_wait(tokens.get_signature(','))
                else:
                    self.match_token_signature(tokens.TokenSignature.OPERATOR_COMMA)     
            self.match_token_signature(tokens.TokenSignature.BRACKET_RIGHT_RECT)
            expr = nodes.Expressions.NodeListCreate(expressions, self.__file, self.get_token_position())
            return expr

        if self.is_token_signature(tokens.TokenSignature.OPERATOR_SNAKE):
            start_pos = self.get_token_position()
            self.match_token_signature(tokens.TokenSignature.OPERATOR_SNAKE)
            
            self.match_and_wait(tokens.get_signature('['))
            
            left_expr = self.parse_expression()
            self.match_and_wait(tokens.get_signature('->'))
            right_expr = self.parse_expression()

            step = None
            if self.is_token_signature(tokens.TokenSignature.OPERATOR_DOT_AND_DOT):
                self.match_token_signature(tokens.TokenSignature.OPERATOR_DOT_AND_DOT)
                step = self.parse_expression()
                
            self.match_and_wait(tokens.get_signature(']'))
            
            return nodes.Expressions.NodeDiapozonCreate(left_expr, right_expr, step, self.__file, start_pos, self.get_token_position())

        if self.is_token_signature(tokens.TokenSignature.KEYWORD_LAMBDA):
            self.match_token_signature(tokens.TokenSignature.KEYWORD_LAMBDA)
            arguments = self.parse_wait_arguments()
            
            
            self.match_and_wait(tokens.get_signature('{'))
            self.match_and_wait(tokens.get_signature('|>'))
            
            expression = self.parse_expression()
            self.match_and_wait(tokens.get_signature('}'))
            
            return nodes.Expressions.NodeLambdaCreate(self.__file, self.get_token_position(), arguments, expression)
            
        if self.is_token_signature(tokens.TokenSignature.WORD):
            if self.is_token_signature(tokens.TokenSignature.BRACKET_LEFT_STANDART, 1):
                name = self.get_token_value()
                pos =  self.get_token_position()
                self.match_token_signature(tokens.TokenSignature.WORD)
                start_pos = self.get_token_position()
                arguments = self.parse_these_arguments()
                end_pos = self.get_token_position()
                
                return nodes.Expressions.NodeCall(self.__file, pos, name, arguments, tokens.TokenPosition(start_pos.line, start_pos.start, end_pos.start-start_pos.start), self.__run_time_memory)
        
            else :
                expr = nodes.Expressions.NodeBaseVariableGet(self.get_token_value(), self.__run_time_memory, self.__file, self.get_token_position())
                self.next_token()
                return expr

    def parse_these_arguments(self):
        arguments = luma_argmunets.LumaTheseArguments()
        self.match_and_wait(tokens.get_signature('('))
        count = 0
        while not self.is_token_signature(tokens.TokenSignature.BRACKET_RIGHT_STANDART):
            expr = self.parse_expression()
           
            if not self.is_token_signature(tokens.TokenSignature.BRACKET_RIGHT_STANDART) and not self.is_token_signature(tokens.TokenSignature.OPERATOR_COMMA):
                luma_excepts.call_exception_wait(self.__file, tokens.get_signature(','), self.get_token_position(-1))
            self.match_token_signature(tokens.TokenSignature.OPERATOR_COMMA)
            arguments.add(
                luma_argmunets.LumaTheseArgument(expr)
            )
            count+=1
            if count>100:
                luma_excepts.call_exception_wait(self.__file, tokens.get_signature(')'), self.get_token_position(-1))
        
        self.match_token_signature(tokens.TokenSignature.BRACKET_RIGHT_STANDART)
        
        return arguments
            

    def parse_wait_arguments(self):
        start_pos = self.get_token_position()
        self.match_and_wait(tokens.get_signature('('))
        arguments = luma_argmunets.LumaArguments()
        count = 0
        while not self.is_token_signature(tokens.TokenSignature.BRACKET_RIGHT_STANDART):
            
            arg = self.parse_wait_argument()
            
            if self.is_token_signature(tokens.TokenSignature.OPERATOR_COMMA):
                self.match_token_signature(tokens.TokenSignature.OPERATOR_COMMA)
            else:
                if self.is_token_signature(tokens.TokenSignature.BRACKET_RIGHT_STANDART):
                    ...
                elif self.is_token_signature(tokens.TokenSignature.BRACKET_LEFT_CURLY):
                    
                    luma_excepts.call_warning_arguments_generate(self.__file, start_pos, self.get_token_position(), False)
                    luma_excepts.call_exception_wait(self.__file, tokens.get_signature(')'), self.get_token_position(-1))
                else:
                    
                    luma_excepts.call_warning_arguments_generate(self.__file, start_pos, self.get_token_position(), False)
                    luma_excepts.call_exception_wait(self.__file, tokens.get_signature(','), self.get_token_position(-1))
            arguments.add(arg)
            count += 1
            if count>100:
                
                luma_excepts.call_warning_arguments_generate(self.__file, start_pos, self.get_token_position(), False)
                luma_excepts.call_exception_wait(self.__file, tokens.get_signature(')'), self.get_token_position(-1))
        self.match_token_signature(tokens.TokenSignature.BRACKET_RIGHT_STANDART)
        
            
        return arguments

    def parse_wait_argument(self):
        arg_name = ''
        arg_types = []
        arg_standart_value = None

        
        arg_name = self.get_token_value()
        
        self.match_token_signature(tokens.TokenSignature.WORD)
        
        if self.is_token_signature(tokens.TokenSignature.OPERATOR_DOT_AND_DOT):
            self.match_token_signature(tokens.TokenSignature.OPERATOR_DOT_AND_DOT)
            if self.is_token_signature(tokens.TokenSignature.WORD):
                
                arg_types.append(self.get_token_value())
                self.match_token_signature(tokens.TokenSignature.WORD)
            elif self.is_token_signature(tokens.TokenSignature.BRACKET_LEFT_STANDART):
                self.match_token_signature(tokens.TokenSignature.BRACKET_LEFT_STANDART)
                count = 0
                while not self.is_token_signature(tokens.TokenSignature.BRACKET_RIGHT_STANDART):
                    count += 1
                    if count>100:
                        luma_excepts.call_exception_wait(self.__file, tokens.get_signature(']'), self.get_token_position(-1))
                    self.is_token_and_wait(tokens.SignatureObject(tokens.TokenSignature.WORD, 'type'))
                    arg_types.append(self.get_token_value())
                    self.match_token_signature(tokens.TokenSignature.WORD)
                self.match_and_wait(tokens.get_signature(']'))
        
        if self.is_token_signature(tokens.TokenSignature.OPERATOR_EQUAL):
            self.match_token_signature(tokens.TokenSignature.OPERATOR_EQUAL)
            arg_standart_value = self.parse_expression()
        
        return luma_argmunets.LumaArgument(arg_name, arg_types, arg_standart_value)

    def generate_ast(self):
        if self.debug:  print(f"Ast tree generate progress: {Fore.MAGENTA}0%{Fore.RESET}")
        while self.get_token_signature() != tokens.TokenSignature.EOF:
            self.__nodes.append(self.parse_statement())
            self.next_token()
            
            if self.debug:
                print(f"Ast tree generate progress: {Fore.MAGENTA}{int(round(self.__pos / len(self.__tokens), 2) * 100)}%{Fore.RESET}")
        if self.debug:  
            print(f"Ast tree generate progress: {Fore.MAGENTA}100%{Fore.RESET} {debug.DebugSignatures.YES}")
            print()
                
                