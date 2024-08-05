from copy import copy
from src.core import luma_exceptions
from src.core import luma_values
from src.core import luma_types
from src.core import luma_lambdas
from src.core import luma_functions
from src.runtime import memory
from src.core import tokens


class ExpressionNumber:
    def __init__(self, file_name: str, value: str, pos: tokens.TokenPosition) -> None:
        self.__pos = pos
        self.__file_name = file_name
        if value.count('.') == 0:
            self.__value = luma_values.IntValue.Create(value)
        elif value.count('.') == 1:
            self.__value = luma_values.FloatValue.Create(value)
        else:
            luma_exceptions.NumberException(self.__file_name, self.__pos).LumaRaise()
        
    def eval(self):
        return self.__value
    
class ExpressionString:
    def __init__(self, file_name: str, value: str, pos: tokens.TokenPosition) -> None:
        self.__pos = pos
        self.__file_name = file_name
        self.__value = luma_values.StringValue.Create(value)

    def eval(self):
        return self.__value

class ExpressionBool:
    def __init__(self, file_name: str, value: str, pos: tokens.TokenPosition) -> None:
        self.__pos = pos
        self.__file_name = file_name
        self.__value = luma_values.BoolValue.Create(value)

    def eval(self):
        return self.__value
    
class ExpressionMathUnary:
    def __init__(self, operation: str, file_name: str, expression, pos: tokens.TokenPosition) -> None:
        self.__operation = operation
        self.__file_name = file_name
        self.__expression = expression
        self.__pos = pos

    def eval(self):
        
        value = self.__expression.eval()
        if self.__operation == '-':
            if luma_values.LumaTypeCheck(value, luma_types.LumaTypes.get('Int')):
                return luma_values.IntValue.Create(-value.value)
            elif luma_values.LumaTypeCheck(value, luma_types.LumaTypes.get('Int')):
                return luma_values.FloatValue.Create(-value.value)
            else:
                luma_exceptions.NotSupportedUnaryOperation(self.__file_name, self.__pos, self.__operation, value).LumaRaise()
        if self.__operation == '+':
            if luma_values.LumaTypeCheck(value, luma_types.LumaTypes.get('Int')):
                return luma_values.IntValue.Create(value.value)
            elif luma_values.LumaTypeCheck(value, luma_types.LumaTypes.get('Int')):
                return luma_values.FloatValue.Create(value.value)
            else:
                luma_exceptions.NotSupportedUnaryOperation(self.__file_name, self.__pos, self.__operation, value).LumaRaise()
        
class ExpressionMathBinary:
    def __init__(self, operation: str, file_name: str, expression_left, expression_right, start_pos: tokens.TokenPosition, this_pos: tokens.TokenPosition) -> None:
        self.__operation = operation
        self.__file_name = file_name
        self.__expression_left = expression_left
        self.__expression_right = expression_right
        self.__start_pos = start_pos
        self.__this_pos = this_pos

    def eval(self):
        
        value_left = self.__expression_left.eval()
        value_right = self.__expression_right.eval()

        if ((luma_values.LumaTypeCheck(value_left, luma_types.LumaTypes.get('Int')) or luma_values.LumaTypeCheck(value_left, luma_types.LumaTypes.get('Float'))) and
            (luma_values.LumaTypeCheck(value_right, luma_types.LumaTypes.get('Int')) or luma_values.LumaTypeCheck(value_right, luma_types.LumaTypes.get('Float')))):
            if self.__operation == '+':
                ret_value = value_left.value + value_right.value
                if luma_values.is_float(ret_value): return luma_values.FloatValue.Create(ret_value)
                if luma_values.is_int(ret_value): return luma_values.IntValue.Create(ret_value)
            if self.__operation == '-':
                ret_value = value_left.value - value_right.value
                if luma_values.is_float(ret_value): return luma_values.FloatValue.Create(ret_value)
                if luma_values.is_int(ret_value): return luma_values.IntValue.Create(ret_value)
            if self.__operation == '/':
                ret_value = value_left.value / value_right.value
                if luma_values.is_float(ret_value): return luma_values.FloatValue.Create(ret_value)
                if luma_values.is_int(ret_value): return luma_values.IntValue.Create(ret_value)
            if self.__operation == '*':
                ret_value = value_left.value * value_right.value
                if luma_values.is_float(ret_value): return luma_values.FloatValue.Create(ret_value)
                if luma_values.is_int(ret_value): return luma_values.IntValue.Create(ret_value)
            if self.__operation == '%':
                ret_value = value_left.value % value_right.value
                if luma_values.is_float(ret_value): return luma_values.FloatValue.Create(ret_value)
                if luma_values.is_int(ret_value): return luma_values.IntValue.Create(ret_value)
        elif (luma_values.LumaTypeCheck(value_left, luma_types.LumaTypes.get('String')) and luma_values.LumaTypeCheck(value_right, luma_types.LumaTypes.get('String'))):
            if self.__operation == '+':
                return luma_values.StringValue.Create(value_left.value + value_right.value)
            else:
                luma_exceptions.NotSupportedBinareOperation(self.__file_name, tokens.TokensLinePos(self.__start_pos, self.__this_pos), self.__operation, value_left, value_right).LumaRaise()
            
        elif luma_values.LumaTypeCheck(value_left, luma_types.LumaTypes.get('String')) and luma_values.LumaTypeCheck(value_right, luma_types.LumaTypes.get('Int')):
            if self.__operation == '*':
                return luma_values.StringValue.Create(value_left.value * value_right.value)
            else:
                luma_exceptions.NotSupportedBinareOperation(self.__file_name, tokens.TokensLinePos(self.__start_pos, self.__this_pos), self.__operation, value_left, value_right).LumaRaise()
            
        else:
            luma_exceptions.NotSupportedBinareOperation(self.__file_name, tokens.TokensLinePos(self.__start_pos, self.__this_pos), self.__operation, value_left, value_right).LumaRaise()

class ExpressionConditionBinary:
    def __init__(self, operation: str, file_name: str, expression_left, expression_right, start_pos: tokens.TokenPosition, this_pos: tokens.TokenPosition) -> None:
        self.__operation = operation
        self.__file_name = file_name
        self.__expression_left = expression_left
        self.__expression_right = expression_right
        self.__start_pos = start_pos
        self.__this_pos = this_pos

    def eval(self):
        
        value_left = self.__expression_left.eval()
        value_right = self.__expression_right.eval()
 
        
        if ((luma_values.LumaTypeCheck(value_left, luma_types.LumaTypes.get('Int')) or luma_values.LumaTypeCheck(value_left, luma_types.LumaTypes.get('Float'))) and
            (luma_values.LumaTypeCheck(value_right, luma_types.LumaTypes.get('Int')) or luma_values.LumaTypeCheck(value_right, luma_types.LumaTypes.get('Float')))):
            if self.__operation == '<':
                ret_value = value_left.value < value_right.value
                return luma_values.BoolValue.Create(ret_value)
            if self.__operation == '>':
                ret_value = value_left.value > value_right.value
                return luma_values.BoolValue.Create(ret_value)
            if self.__operation == '>=':
                ret_value = value_left.value >= value_right.value
                return luma_values.BoolValue.Create(ret_value)
            if self.__operation == '<=':
                ret_value = value_left.value <= value_right.value
                return luma_values.BoolValue.Create(ret_value)
            if self.__operation == '!=':
                ret_value = value_left.value != value_right.value
                return luma_values.BoolValue.Create(ret_value)
            if self.__operation == '==':
                ret_value = value_left.value == value_right.value
                return luma_values.BoolValue.Create(ret_value)
                


        elif (luma_values.LumaTypeCheck(value_left, luma_types.LumaTypes.get('Bool')) and luma_values.LumaTypeCheck(value_right, luma_types.LumaTypes.get('Bool'))):
            if self.__operation == '==':
                return luma_values.BoolValue.Create(value_left.value == value_right.value)
            elif self.__operation == '!=':
                return luma_values.BoolValue.Create(value_left.value == value_right.value)
            elif self.__operation == '||':
                return luma_values.BoolValue.Create(value_left.value or value_right.value)
            elif self.__operation == '&&':
                return luma_values.BoolValue.Create(value_left.value and value_right.value)
            else:
                luma_exceptions.NotSupportedBinareOperation(self.__file_name, tokens.TokensLinePos(self.__start_pos, self.__this_pos), self.__operation, value_left, value_right).LumaRaise()

        elif (luma_values.LumaTypeCheck(value_left, luma_types.LumaTypes.get('String')) and luma_values.LumaTypeCheck(value_right, luma_types.LumaTypes.get('String'))):
            if self.__operation == '==':
                return luma_values.BoolValue.Create(value_left.value == value_right.value)
            elif self.__operation == '!=':
                return luma_values.BoolValue.Create(value_left.value == value_right.value)
            else:
                luma_exceptions.NotSupportedBinareOperation(self.__file_name, tokens.TokensLinePos(self.__start_pos, self.__this_pos), self.__operation, value_left, value_right).LumaRaise()
            
        
            
        else:
            luma_exceptions.NotSupportedBinareOperation(self.__file_name, tokens.TokensLinePos(self.__start_pos, self.__this_pos), self.__operation, value_left, value_right).LumaRaise()

class ExpressionVariableGet:
    def __init__(self, memory: memory.RunTimeMemory, file_name: str, var_name: str, pos: tokens.TokenPosition) -> None:
        self.__file_name = file_name
        self.__var_name = var_name
        self.__memory = memory
        self.__pos = pos

    def eval(self):

        if self.__memory.ContainWithNameObject(self.__var_name):
            try:
                return copy(self.__memory.GetObject(self.__var_name, memory.MemoryObjectTypes.LAMBDA).value)
            except:
                try:
                    return copy(self.__memory.GetObject(self.__var_name, memory.MemoryObjectTypes.VARIABLE).value)
                except:
                    return copy(self.__memory.GetObject(self.__var_name, memory.MemoryObjectTypes.FUNCTION).value)
        else:
            luma_exceptions.VariableNotFound(self.__file_name, self.__pos, self.__var_name).LumaRaise()
        
class ExpressionLambdaObject:
    def __init__(self, arguments: list[str], expression) -> None:
        self.__arguments = arguments
        self.__expression = expression

    def eval(self):
        return luma_values.LambdaValue.Create(luma_lambdas.LambdaConstruct(self.__arguments, self.__expression))
    
class ExpressionFunObject:
    def __init__(self, arguments: list[str], expression, file_name: str, returned = False) -> None:
        self.__arguments = arguments
        self.__expression = expression
        self.__file_name = file_name
        self.__returned = returned

    def eval(self):
        return luma_values.FunctionValue.Create(
            luma_functions.LumaFunction.ConstructLumaFunction(
                self.__expression, None, self.__returned, self.__file_name, self.__arguments
            )
        )

class ExpressionCall:
    def __init__(self, this_memory: memory.RunTimeMemory, file_name: str, start_pos:tokens.TokenPosition, pos: tokens.TokenPosition,  variable_name: str, arguments_expression: list) -> None:
        self.__var_name = variable_name
        self.__arguments_expression = arguments_expression
        self.__memory = this_memory
        self.__file_name = file_name
        self.__pos = pos
        self.__start_pos = start_pos
        

    def eval(self):
        
        if self.__memory.ConatinsWithNameAndType(self.__var_name, memory.MemoryObjectTypes.LAMBDA):
            lambda_object = self.__memory.GetObject(self.__var_name, memory.MemoryObjectTypes.LAMBDA)
            if len(self.__arguments_expression) != len(lambda_object.value.value.waited_value_names):
                luma_exceptions.ArgumentCountError(self.__file_name, tokens.TokensLinePos(self.__start_pos, self.__pos), self.__var_name, len(self.__arguments_expression), len(lambda_object.value.value.waited_value_names)).LumaRaise()
            else:
                
                self.__memory.BufferizeMemory()
                
                for i in range(len(self.__arguments_expression)):
                    value = self.__arguments_expression[i].eval()
                    type = luma_values.get_memory_type(value)
                    self.__memory.WriteObject(
                        memory.MemoryObject(lambda_object.value.value.waited_value_names[i], value, False, type, True))
                res_value = lambda_object.value.value.expression.eval()
                
                self.__memory.UnBufferizeMemory()
                return res_value
            
        elif self.__memory.ConatinsWithNameAndType(self.__var_name, memory.MemoryObjectTypes.FUNCTION):
            function_object = self.__memory.GetObject(self.__var_name, memory.MemoryObjectTypes.FUNCTION)
            if len(self.__arguments_expression) != len(function_object.value.value.waited_value_names):
                luma_exceptions.ArgumentCountError(self.__file_name, tokens.TokensLinePos(self.__start_pos, self.__pos), self.__var_name, len(self.__arguments_expression), len(function_object.value.value.waited_value_names)).LumaRaise()
            else:
                self.__memory.BufferizeMemory()
                for i in range(len(self.__arguments_expression)):
                    value = self.__arguments_expression[i].eval()
                    type = luma_values.get_memory_type(value)
                    self.__memory.WriteObject(
                        memory.MemoryObject(function_object.value.value.waited_value_names[i], value, False, type, True))
                
                
                    
                if function_object.value.value.returned or function_object.value.value.callable_object.is_returned():
                            
                        
                    try:
                        function_object.value.value.callable_object.exec()
                    except luma_exceptions.Return as ret:
                                
                        res_value = ret.expression.eval()
                        return res_value
                else:
                    luma_exceptions.ErrorFunNotReturn(self.__file_name, self.__pos, self.__var_name).LumaRaise()
                
        else:
            luma_exceptions.VariableNotFound(self.__file_name, self.__pos, self.__var_name).LumaRaise()

class ExpressionCallLib:
    def __init__(self, this_memory: memory.RunTimeMemory, file_name: str, start_pos: tokens.TokenPosition, pos: tokens.TokenPosition,  variable_name: str, arguments_expression: list, lib_name: str,
                    all_libs: list[str]) -> None:
        self.__var_name = variable_name
        self.__arguments_expression = arguments_expression
        self.__memory = this_memory
        self.__file_name = file_name
        self.__pos = pos
        self.__start_pos = start_pos
        self.__lib_name = lib_name
        self.__all_libs = all_libs

    def eval(self):
        if self.__lib_name+'.' not in self.__all_libs:
            luma_exceptions.FileNotFound(self.__file_name, self.__pos, self.__lib_name).LumaRaise()
        
        if self.__memory.ConatinsWithNameAndType(self.__lib_name+'.'+self.__var_name, memory.MemoryObjectTypes.LAMBDA):
            lambda_object = self.__memory.GetObject(self.__lib_name+'.'+self.__var_name, memory.MemoryObjectTypes.LAMBDA)
            if len(self.__arguments_expression) != len(lambda_object.value.value.waited_value_names):
                luma_exceptions.ArgumentCountError(self.__file_name, tokens.TokensLinePos(self.__start_pos, self.__pos), self.__lib_name+'.'+self.__var_name, len(self.__arguments_expression), len(lambda_object.value.value.waited_value_names)).LumaRaise()
            else:
                
                self.__memory.BufferizeMemory()
                
                for i in range(len(self.__arguments_expression)):
                    value = self.__arguments_expression[i].eval()
                    type = luma_values.get_memory_type(value)
                    self.__memory.WriteObject(
                        memory.MemoryObject(lambda_object.value.value.waited_value_names[i], value, False, type, True))
                res_value = lambda_object.value.value.expression.eval()
                
                self.__memory.UnBufferizeMemory()
                return res_value
            
        elif self.__memory.ConatinsWithNameAndType(self.__lib_name+'.'+self.__var_name, memory.MemoryObjectTypes.FUNCTION):
            function_object = self.__memory.GetObject(self.__lib_name+'.'+self.__var_name, memory.MemoryObjectTypes.FUNCTION)
            if len(self.__arguments_expression) != len(function_object.value.value.waited_value_names):
                luma_exceptions.ArgumentCountError(self.__file_name, tokens.TokensLinePos(self.__start_pos, self.__pos), self.__lib_name+'.'+self.__var_name, len(self.__arguments_expression), len(function_object.value.value.waited_value_names)).LumaRaise()
            else:
                self.__memory.BufferizeMemory()
                for i in range(len(self.__arguments_expression)):
                    
                    value = self.__arguments_expression[i].eval()
                    
                    type = luma_values.get_memory_type(value)
                    self.__memory.WriteObject(
                        memory.MemoryObject(function_object.value.value.waited_value_names[i], value, False, type, True))
                
                if function_object.value.value.types is not None:
                    
                    for i in range(len(function_object.value.value.types)):
                        
                        if luma_types.LumaTypeCheck(self.__memory.GetObjectWithoutType(function_object.value.value.waited_value_names[i]), function_object.value.value.types[i]):
                            ...
                        else: 
                            luma_exceptions.ErrorTypedArg(self.__file_name, tokens.TokensLinePos(self.__start_pos, self.__pos), 
                                                          function_object, 
                                                          self.__memory.GetObjectWithoutType(function_object.value.value.waited_value_names[i]), i).LumaRaise()
                if function_object.value.value.returned:
                    res_value = function_object.value.value.callable_object(*self.__memory.GetObjectsWithNames(function_object.value.value.waited_value_names))
                    return res_value
        else:
            luma_exceptions.VariableNotFound(self.__file_name, self.__pos, self.__var_name).LumaRaise()
