
import sys
import time
sys.path.extend('../')


from src.core import luma_exceptions
from src.core import luma_libs
from src.core import tokens

from src.runtime import expressions
from src.runtime import commands
from src.runtime import memory

from src.debugs import debug_parser, debug_compiler


class Parser:

    def __init__(self, debug: bool = False) -> None:
        self.__pos = 0
        self.__tokens = []
        self.__tokens_count = 0
        self.__file_name = None
        self.__saved_pos = None
        self.__commands = []
        self.__run_time_memory = memory.RunTimeMemory()
        self.__loaded_libs = []
        self.__debug = debug

    @property
    def commands(self):
        return self.__commands

    def load_tokens(self, tokens: list[tokens.Token], file_name: str):
        self.__tokens = tokens
        self.__tokens_count = len(self.__tokens)
        self.__file_name = file_name

    def next(self):
        self.__pos += 1

    def before(self):
        self.__pos -= 1

    def get_token(self, offset: int = 0):
        return self.__tokens[self.__pos + offset]
    
    def get_token_signature(self, offset: int = 0):
        return self.__tokens[self.__pos + offset].signature
    
    def get_token_value(self, offset: int = 0):
        return self.__tokens[self.__pos + offset].value
    
    def get_token_pos(self, offset: int = 0):
        return self.__tokens[self.__pos + offset].position
    
    def match(self, token_signature: tokens.TokenSignature) -> bool:
        if self.get_token_signature() == token_signature:
            self.next()
            return True
        else:
            return False
        
    def match_and_wait(self, token_signature: tokens.TokenSignature, wait_signature: str):
        if self.match(token_signature): ...
        else: luma_exceptions.WaitException(wait_signature, self.__file_name, self.get_token_pos()).LumaRaise()
        
    def is_token(self, token_signature: tokens.TokenSignature, offset: int = 0) -> bool:
        if self.get_token_signature(offset) == token_signature:
            return True
        else:
            return False
        
    def is_token_and_wait(self, token_signature: tokens.TokenSignature, wait_signature: str) -> bool:
        if self.get_token_signature() == token_signature:
            return True
        else:
            luma_exceptions.WaitException(wait_signature, self.__file_name, self.get_token_pos(-1)).LumaRaise()
        
    def parse_waited_arguments(self):
        arguments = []
        self.match_and_wait(tokens.TokenSignature.BRACKET_LEFT_STANDART, '(')
        while not self.is_token(tokens.TokenSignature.BRACKET_RIGHT_STANDART):
            if self.is_token(tokens.TokenSignature.WORD):
                arguments.append(self.get_token_value())
                self.match(tokens.TokenSignature.WORD)
                if self.is_token(tokens.TokenSignature.OPERATOR_COMMA):
                    self.match(tokens.TokenSignature.OPERATOR_COMMA)
                else:
                    luma_exceptions.WaitException(',', self.__file_name, self.get_token_pos())
            else:
                luma_exceptions.IncorrectDefinitionArgument(self.__file_name, self.get_token_pos(), self.get_token_value()).LumaRaise()
        self.match(tokens.TokenSignature.BRACKET_RIGHT_STANDART)
        return arguments

    def parse_waited_arguments_and_add_poses(self):
        arguments = []
        self.match_and_wait(tokens.TokenSignature.BRACKET_LEFT_STANDART, '(')
        while not self.is_token(tokens.TokenSignature.BRACKET_RIGHT_STANDART):
            if self.is_token(tokens.TokenSignature.WORD):
                arguments.append([self.get_token_value(), self.get_token_pos()])
                self.match(tokens.TokenSignature.WORD)
                if self.is_token(tokens.TokenSignature.OPERATOR_COMMA):
                    self.match(tokens.TokenSignature.OPERATOR_COMMA)
                else:
                    luma_exceptions.WaitException(',', self.__file_name, self.get_token_pos())
            else:
                luma_exceptions.IncorrectDefinitionArgument(self.__file_name, self.get_token_pos(), self.get_token_value()).LumaRaise()
        self.match(tokens.TokenSignature.BRACKET_RIGHT_STANDART)
        return arguments

    def parse_expression_arguments(self):
        arguments = []
        self.match_and_wait(tokens.TokenSignature.BRACKET_LEFT_STANDART, '(')
        while not self.is_token(tokens.TokenSignature.BRACKET_RIGHT_STANDART):
            arguments.append(self.parse_expression())
            if self.is_token(tokens.TokenSignature.OPERATOR_COMMA):
                self.match(tokens.TokenSignature.OPERATOR_COMMA)
            else:
                luma_exceptions.WaitException(',', self.__file_name, self.get_token_pos())
        self.match(tokens.TokenSignature.BRACKET_RIGHT_STANDART)
        return arguments

    def parse_commands_list(self):
        self.match_and_wait(tokens.TokenSignature.BRACKET_LEFT_CURLY, '{')
        commands = []
        while not self.is_token(tokens.TokenSignature.BRACKET_RIGHT_CURLY):
            commands.append(self.parse_commands())
            self.match_and_wait(tokens.TokenSignature.OPERATOR_DOT_AND_COMMA, ';')
            
        self.match(tokens.TokenSignature.BRACKET_RIGHT_CURLY)
        
        return commands
    
    def parse_commands_list_for_CommandsList(self):
        return commands.CommandCreateCommandsList(self.parse_commands_list())

    def parse_commands(self):
        command_start_pos = self.get_token_pos()
        if self.match(tokens.TokenSignature.KEYVORD_LET) or self.match(tokens.TokenSignature.KEYWORD_VAR):  
            return self.construct_command_BaseVariableSet(command_start_pos)
        if self.is_token(tokens.TokenSignature.WORD) and self.is_token(tokens.TokenSignature.OPERATOR_EQUAL, 1):
            return self.construct_command_BaseVariableChainge(command_start_pos)
        if self.is_token(tokens.TokenSignature.KEYWORD_DEL):
            return self.construct_command_CommandBaseVariableDelete(command_start_pos)
        if self.is_token(tokens.TokenSignature.KEYWORD_USING):
            return self.construct_command_CommandLoadFile(command_start_pos)
        if self.is_token(tokens.TokenSignature.WORD) and self.is_token(tokens.TokenSignature.BRACKET_LEFT_STANDART, 1):
            return self.construct_command_Call(command_start_pos)
        if self.is_token(tokens.TokenSignature.WORD) and self.is_token(tokens.TokenSignature.OPERATOR_DOT, 1):
            return self.construct_command_CallLib(command_start_pos)
        if self.is_token(tokens.TokenSignature.KEYVORD_FOR):
            return self.construct_command_For(command_start_pos)
            
        return self.parse_expression()
    
    def construct_command_For(self, command_start_pos):
        self.match(tokens.TokenSignature.KEYVORD_FOR)
        self.match_and_wait(tokens.TokenSignature.BRACKET_LEFT_STANDART, '(')
        variable_set_command = self.parse_commands()
        self.match_and_wait(tokens.TokenSignature.OPERATOR_DOT_AND_COMMA, ';')
        expression_condition = self.parse_expression()
        
        self.match_and_wait(tokens.TokenSignature.OPERATOR_DOT_AND_COMMA, ';')
        
        summ_command = self.parse_commands()
        
        self.match_and_wait(tokens.TokenSignature.OPERATOR_DOT_AND_COMMA, ';')
        self.match_and_wait(tokens.TokenSignature.BRACKET_RIGHT_STANDART, ')')
        
        executed_commands = self.parse_commands_list_for_CommandsList()
        self.is_token_and_wait(tokens.TokenSignature.OPERATOR_DOT_AND_COMMA, ';')
        return commands.CommandFor(variable_set_command, expression_condition, 
                summ_command, executed_commands, self.__file_name, command_start_pos)

    
    def construct_command_CallLib(self, command_start_pos):
        lib_name = self.get_token_value()
        self.match(tokens.TokenSignature.WORD)
        self.match(tokens.TokenSignature.OPERATOR_DOT)
        variable_name = self.get_token_value()
        self.match(tokens.TokenSignature.WORD)
        arguments_expressions = self.parse_expression_arguments()
        self.is_token_and_wait(tokens.TokenSignature.OPERATOR_DOT_AND_COMMA, ';')
        
        return commands.CommandCallLib(self.__run_time_memory, self.__file_name, command_start_pos, self.get_token_pos(), 
                                       variable_name, arguments_expressions, lib_name, self.__loaded_libs)
    
    def construct_command_Call(self, command_start_pos):
        variable_name = self.get_token_value()
        self.match(tokens.TokenSignature.WORD)
        arguments_expressions = self.parse_expression_arguments()
        self.is_token_and_wait(tokens.TokenSignature.OPERATOR_DOT_AND_COMMA, ';')
        return commands.CommandCall(self.__run_time_memory, self.__file_name, command_start_pos, self.get_token_pos(), variable_name, arguments_expressions)

    def construct_command_CommandLoadFile(self, command_start_pos):
        self.match(tokens.TokenSignature.KEYWORD_USING)
        
        self.is_token_and_wait(tokens.TokenSignature.STRING, 'loaded file directory')
        file_directory = self.get_token_value()
        self.match(tokens.TokenSignature.STRING)
        self.match_and_wait(tokens.TokenSignature.BRACKET_LEFT_STANDART, '(')
        self.is_token_and_wait(tokens.TokenSignature.WORD, 'loaded file extension (py, lm)')
        file_extension = self.get_token_value()
        self.match(tokens.TokenSignature.WORD)
        
        self.match_and_wait(tokens.TokenSignature.BRACKET_RIGHT_STANDART, ')')
        command_end_pos = self.get_token_pos()
        self.is_token_and_wait(tokens.TokenSignature.OPERATOR_DOT_AND_COMMA, ';')
        self.__loaded_libs.append(luma_libs.get_lib_name(file_directory))
        return commands.CommandLoadFile(self.__run_time_memory, file_directory, self.__file_name, command_start_pos, command_end_pos, file_extension)

    def construct_command_CommandBaseVariableDelete(self, command_start_pos):
        self.match(tokens.TokenSignature.KEYWORD_DEL)
        var_names = self.parse_waited_arguments_and_add_poses()
        self.is_token_and_wait(tokens.TokenSignature.OPERATOR_DOT_AND_COMMA, ';')
        return commands.CommandBaseVariableDelete(self.__run_time_memory, var_names, self.__file_name, command_start_pos)
    
    def construct_command_BaseVariableChainge(self, command_start_pos):
        variable_name = self.get_token_value()
        self.match(tokens.TokenSignature.WORD)
        self.match(tokens.TokenSignature.OPERATOR_EQUAL)
        variable_expression = self.parse_expression()
        self.is_token_and_wait(tokens.TokenSignature.OPERATOR_DOT_AND_COMMA, ';')
        command_end_pos = self.get_token_pos()
        return commands.CommandBaseVariableChainge(
            self.__run_time_memory, variable_name, variable_expression, self.__file_name,  command_start_pos, command_end_pos
        )
    
    def construct_command_BaseVariableSet(self, command_start_pos):
        variable_mutable = False
        if self.match(tokens.TokenSignature.KEYVORD_MUT): 
            variable_mutable = True
        variable_name = self.get_token_value()

        self.match_and_wait(tokens.TokenSignature.WORD, 'variable name')

        if self.match(tokens.TokenSignature.OPERATOR_DOT_AND_COMMA):
            command_end_pos = self.get_token_pos()
            self.before()
            return commands.CommandBaseVariableSet(
                self.__run_time_memory, variable_name, None, True, 
                file_name = self.__file_name, csp = command_start_pos, cep = command_end_pos
            )
        else:
            self.match_and_wait(tokens.TokenSignature.OPERATOR_EQUAL, '=')
            variable_expression = self.parse_expression()
            self.is_token_and_wait(tokens.TokenSignature.OPERATOR_DOT_AND_COMMA, ';')
            command_end_pos = self.get_token_pos()
            return commands.CommandBaseVariableSet(
                self.__run_time_memory, variable_name, variable_expression, variable_mutable, 
                file_name = self.__file_name, csp = command_start_pos, cep = command_end_pos
            )
    
    def parse_expression(self):
        return self.parse_and()
    
    def parse_and(self):
        parse_pos_start = self.get_token_pos(0)
        expression = self.parse_or()
        while True:
            if self.match(tokens.TokenSignature.OPERATOR_AND):
                expression = expressions.ExpressionConditionBinary('&&', self.__file_name, expression, self.parse_or(), parse_pos_start, self.get_token_pos())
                continue
            break
        return expression

    def parse_or(self):
        parse_pos_start = self.get_token_pos(0)
        expression = self.parse_equals()
        while True:
            if self.match(tokens.TokenSignature.OPERATOR_OR):
                expression = expressions.ExpressionConditionBinary('||', self.__file_name, expression, self.parse_equals(), parse_pos_start, self.get_token_pos())
                continue
            break
        return expression

    def parse_equals(self):
        parse_pos_start = self.get_token_pos(0)
        expression = self.parse_conditions()
        while True:
            if self.match(tokens.TokenSignature.OPERATOR_NOT_EQUAL):
                expression = expressions.ExpressionConditionBinary('!=', self.__file_name, expression, self.parse_conditions(), parse_pos_start, self.get_token_pos())
                continue
            if self.match(tokens.TokenSignature.OPERATOR_EQUAL_EQUAL):
                expression = expressions.ExpressionConditionBinary('==', self.__file_name, expression, self.parse_conditions(), parse_pos_start, self.get_token_pos())
                continue
            break
        return expression

    def parse_conditions(self):
        parse_pos_start = self.get_token_pos(0)
        expression = self.parse_math_binare_addit()
        while True:
            if self.match(tokens.TokenSignature.OPERATOR_BIGGEST):
                expression = expressions.ExpressionConditionBinary('>', self.__file_name, expression, self.parse_math_binare_addit(), parse_pos_start, self.get_token_pos())
                continue
            if self.match(tokens.TokenSignature.OPERATOR_SMALLEST):
                expression = expressions.ExpressionConditionBinary('<', self.__file_name, expression, self.parse_math_binare_addit(), parse_pos_start, self.get_token_pos())
                continue
            if self.match(tokens.TokenSignature.OPERATOR_SMALLEST_EQUAL):
                expression = expressions.ExpressionConditionBinary('<=', self.__file_name, expression, self.parse_math_binare_addit(), parse_pos_start, self.get_token_pos())
                continue
            if self.match(tokens.TokenSignature.OPERATOR_BIGGEST_EQUAL):
                expression = expressions.ExpressionConditionBinary('>=', self.__file_name, expression, self.parse_math_binare_addit(), parse_pos_start, self.get_token_pos())
                continue
            break
        return expression

    def parse_math_binare_addit(self):
        parse_pos_start = self.get_token_pos(0)
        expression = self.parse_math_binare_multi()
        while True:
            if self.match(tokens.TokenSignature.OPERATOR_PLUS):
                expression = expressions.ExpressionMathBinary('+', self.__file_name, expression, self.parse_math_binare_multi(), parse_pos_start, self.get_token_pos())
                continue
            if self.match(tokens.TokenSignature.OPERATOR_MINUS):
                expression = expressions.ExpressionMathBinary('-', self.__file_name, expression, self.parse_math_binare_multi(), parse_pos_start, self.get_token_pos())
                continue
            break
        return expression

    def parse_math_binare_multi(self):
        parse_pos_start = self.get_token_pos(0)
        expression = self.parse_math_unary()
        while True:
            if self.match(tokens.TokenSignature.OPERATOR_DIV):
                expression = expressions.ExpressionMathBinary('/', self.__file_name, expression, self.parse_math_unary(), parse_pos_start, self.get_token_pos())
                continue
            if self.match(tokens.TokenSignature.OPERATOR_MUL):
                expression = expressions.ExpressionMathBinary('*', self.__file_name, expression, self.parse_math_unary(), parse_pos_start, self.get_token_pos())
                continue
            break
        return expression
    
    def parse_math_unary(self):
        expression_start_pos = self.get_token_pos()
        if self.match(tokens.TokenSignature.OPERATOR_MINUS):
            return expressions.ExpressionMathUnary('-', self.__file_name, self.parse_basic(), expression_start_pos)
        if self.match(tokens.TokenSignature.OPERATOR_PLUS):
            return expressions.ExpressionMathUnary('+', self.__file_name, self.parse_basic(), expression_start_pos)
        return self.parse_basic()
    
    def parse_basic(self):
        if self.is_token(tokens.TokenSignature.NUMBER):
            expr = expressions.ExpressionNumber(self.__file_name, self.get_token_value(), self.get_token_pos())
            self.next()
            return expr
        
        if self.is_token(tokens.TokenSignature.STRING):
            expr = expressions.ExpressionString(self.__file_name, self.get_token_value(), self.get_token_pos())
            self.next()
            return expr
        
        if self.is_token(tokens.TokenSignature.TRUE) or self.is_token(tokens.TokenSignature.FALSE):
            expr = expressions.ExpressionBool(self.__file_name, self.get_token_value(), self.get_token_pos())
            self.next()
            return expr
        
        if self.is_token(tokens.TokenSignature.WORD) and self.is_token(tokens.TokenSignature.OPERATOR_DOT, 1):
            lib_name = self.get_token_value()
            self.match(tokens.TokenSignature.WORD)
            self.match(tokens.TokenSignature.OPERATOR_DOT)
            variable_name = self.get_token_value()
            self.match(tokens.TokenSignature.WORD)
            start_pos = self.get_token_pos()
            arguments_expressions = self.parse_expression_arguments()
            return expressions.ExpressionCallLib(self.__run_time_memory, self.__file_name, start_pos, self.get_token_pos(), variable_name, arguments_expressions, lib_name, self.__loaded_libs)
        
        if self.is_token(tokens.TokenSignature.WORD) and self.is_token(tokens.TokenSignature.BRACKET_LEFT_STANDART, 1):
            variable_name = self.get_token_value()
            self.match(tokens.TokenSignature.WORD)
            start_pos = self.get_token_pos()
            arguments_expressions = self.parse_expression_arguments()
            return expressions.ExpressionCall(self.__run_time_memory, self.__file_name, start_pos, self.get_token_pos(), variable_name, arguments_expressions)
        
        if self.is_token(tokens.TokenSignature.WORD):
            expr = expressions.ExpressionVariableGet(self.__run_time_memory, self.__file_name, self.get_token_value(), self.get_token_pos())
            self.next()
            return expr
        
        if self.is_token(tokens.TokenSignature.BRACKET_LEFT_STANDART):
            self.match(tokens.TokenSignature.BRACKET_LEFT_STANDART)
            expr = self.parse_expression()
            self.match(tokens.TokenSignature.BRACKET_RIGHT_STANDART)
            return expr
    
        if self.is_token(tokens.TokenSignature.KEYWORD_LAMBDA):
            self.match(tokens.TokenSignature.KEYWORD_LAMBDA)
            wait_argument_names = self.parse_waited_arguments()
            self.match_and_wait(tokens.TokenSignature.BRACKET_LEFT_CURLY, '{')
            self.match_and_wait(tokens.TokenSignature.KEYWORD_RETURN, '|>')
            expresion = self.parse_expression()
            self.match_and_wait(tokens.TokenSignature.BRACKET_RIGHT_CURLY, '}')
            return expressions.ExpressionLambdaObject(wait_argument_names, expresion)

        if self.is_token(tokens.TokenSignature.KEYWORD_FUN):
            
            self.match(tokens.TokenSignature.KEYWORD_FUN)
            wait_argument_names = self.parse_waited_arguments()
            code_block = self.parse_commands_list_for_CommandsList()
            return expressions.ExpressionFunObject(wait_argument_names, code_block, self.__file_name)

    def parse(self):
        while self.get_token_signature() != tokens.TokenSignature.EOF:
            self.__commands.append(self.parse_commands())
            self.next()

    def execute(self):
        for command in self.commands:
            command.exec()
            self.clear_cache()
            if self.__debug: self.debug_memory()
                  
    def debug_commands(self):
        debug_parser.debug_commands(self.__commands)

    def debug_memory(self):
        debug_compiler.debug_run_time_memory(self.__run_time_memory.get_memory())

    def clear_cache(self):
        self.__run_time_memory.ClearCache()
