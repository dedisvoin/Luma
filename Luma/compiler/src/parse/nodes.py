from colorama import Fore
from src.core import memory
from src.core import luma_types
from src.core import luma_values
from src.core import luma_excepts
from src.core import luma_lambdas
from src.core import luma_argmunets
from src.core import out_features
from src.core import tokens

class BaseExpression:
    def __init__(self, file, pos) -> None:
        self.file = file
        self.pos = pos

    def eval(self):
        ...

class Statements:

    class NodeVariableSet:
        def __init__(self, var_name: str, var_mutable: memory.MemoryObjectTypes, var_expression, memory: memory.Memory ) -> None:
            self.__name = var_name
            self.__mutable = var_mutable
            self.__expression = var_expression
            self.__memory = memory

        def exec(self):
            if self.__expression is not None:
                self.__memory.write(self.__name, self.__expression.eval(), self.__mutable)
            else:
                self.__memory.write(self.__name, None, self.__mutable)
    
    class NodeBaseVariableUpdate:
        def __init__(self, var_name: str, var_expression, memory: memory.Memory, file, pos_name) -> None:
            self.__name = var_name
            self.__expression = var_expression
            self.__memory = memory
            self.__file = file
            self.__pos_name = pos_name
        
        def exec(self):
            self.value = self.__expression.eval()
            if self.__memory.is_mutable(self.__name):
                self.__memory.write(self.__name, self.value, memory.MemoryObjectTypes.mutable)
            else:
                luma_excepts.call_exeception_base_variable_not_mutable(self.__file, self.__name, self.__pos_name)

    class NodeOut:
        def __init__(self, vars_expressions) -> None:
            self.__vars_expressions = vars_expressions

        def exec(self):
            values = [expr.eval() for expr in self.__vars_expressions]
            new_values = out_features.LumaListToOutList(values)
            print(*new_values)

class Expressions:
    class NodeNumberCreate(BaseExpression):
        def __init__(self, value: str, file, pos) -> None:
            super().__init__(file, pos)
            py_number = luma_types.GetPyNumberForString(value)
            if isinstance(py_number, int):
                self.__value = luma_values.L_Int.set_value(py_number)
            elif isinstance(py_number, float):
                self.__value = luma_values.L_Float.set_value(py_number)

        def eval(self):
            return self.__value
        
    class NodeBoolCreate(BaseExpression):
        def __init__(self, value: str, file, pos) -> None:
            super().__init__(file, pos)
            self.__value = luma_values.L_True.copy_value() if value == 'true' else luma_values.L_False.copy_value() 

        def eval(self):
            return self.__value
        
    class NodeStringCreate(BaseExpression):
        def __init__(self, value: str, file, pos) -> None:
            super().__init__(file, pos)
            self.__value = luma_values.L_String.set_value(value)

        def eval(self):
            return self.__value
    
    class NodeListCreate(BaseExpression):
        def __init__(self, expressions, file, pos) -> None:
            super().__init__(file, pos)
            self.__expressions = expressions
            
        def eval(self):
            values = [expr.eval() for expr in self.__expressions]
            return luma_values.L_List.set_value(values)

    class NodeDiapozonCreate(BaseExpression):
        def __init__(self, start_expression, end_expression, step, file, start_pos, end_pos) -> None:
            super().__init__(file, tokens.TokenPosition(start_pos.line, start_pos.start, end_pos.start - start_pos.start))
            self.__start_value = start_expression
            self.__end_value = end_expression
            self.__step = step

        def eval(self):
            start_value = self.__start_value.eval()
            end_value = self.__end_value.eval()
            step = luma_values.LumaValue(1) if self.__step is None else self.__step.eval()
            if luma_types.LumaTypeCheck(start_value, luma_types.BaseLumaTypes.L_Int) and luma_types.LumaTypeCheck(end_value, luma_types.BaseLumaTypes.L_Int) and luma_types.LumaTypeCheck(step, luma_types.BaseLumaTypes.L_Int):
                
                diapozon = list(range(start_value.get_value(), end_value.get_value() + step.get_value(), step.get_value()))
                diapozon = [luma_values.LumaValue(value) for value in diapozon]
            elif luma_types.LumaTypeCheck(start_value, luma_types.BaseLumaTypes.L_Char) and luma_types.LumaTypeCheck(end_value, luma_types.BaseLumaTypes.L_Char) and luma_types.LumaTypeCheck(step, luma_types.BaseLumaTypes.L_Int):
                diapozon = list(range(ord(start_value.get_value()), ord(end_value.get_value()) + step.get_value(), step.get_value()))
                diapozon = list(map(lambda x: luma_values.LumaValue(chr(x)), diapozon))
            else:
                luma_excepts.call_exception_diapozon_generate_fail(self.file, self.pos, start_value.get_type(), end_value.get_type(), step.get_type())



            return luma_values.L_List.set_value(diapozon)

    class NodeUnareOperation(BaseExpression):
        def __init__(self, operation: str, expression, file, pos) -> None:
            super().__init__(file, pos)
            self.__operation = operation
            self.__expression = expression

            self.__number_suported_types = [
                luma_types.BaseLumaTypes.L_Int,
                luma_types.BaseLumaTypes.L_Float,
            ]
        
        def eval(self):
            value = self.__expression.eval()
            if luma_types.LumaTypesCheck(value, self.__number_suported_types):
                if self.__operation == '+':
                    value = +value.get_value() 
                    return luma_values.LumaValue.create(value)
                elif self.__operation == '-':
                    value = -value.get_value() 
                    return luma_values.LumaValue.create(value)
                
    class NodeBinareOperation(BaseExpression):
        def __init__(self, operation: str, left_expression, right_expression, file, pos) -> None:
            super().__init__(file, pos)
            self.__operation = operation
            self.__left_expression = left_expression
            self.__right_expression = right_expression

            self.__number_suported_types = [
                luma_types.BaseLumaTypes.L_Int,
                luma_types.BaseLumaTypes.L_Float,
            ]
            self.__number_and_number_suported_operations = {
                '+': lambda v1, v2: v1 + v2,
                '-': lambda v1, v2: v1 - v2,
                '*': lambda v1, v2: v1 * v2,
                '/': lambda v1, v2: v1 / v2,
                '%': lambda v1, v2: v1 % v2
            }

            self.__string_and_string_suported_operatios = {
                '+': lambda v1, v2: v1 + v2
            }

            self.__string_and_number_suported_operations = {
                '*': lambda v1, v2: v1 * v2
            }

            self.__char_and_number_suported_operations = {
                '*': lambda v1, v2: v1 * v2
            }

            self.__list_and_list_suported_operations = {
                '+': lambda v1, v2: v1 + v2
            }

        def eval(self):
            value_left = self.__left_expression.eval()
            value_right = self.__right_expression.eval()
            if luma_types.LumaTypesCheck(value_left, self.__number_suported_types) and luma_types.LumaTypesCheck(value_right, self.__number_suported_types):
                try:
                    value = self.__number_and_number_suported_operations[self.__operation](value_left.get_value(), value_right.get_value())
                    return luma_values.LumaValue.create(value)
                except: luma_excepts.call_exception_not_suport_operation(self.file, self.__operation, value_left, value_right, self.pos)

            elif luma_types.LumaTypeCheck(value_left, luma_types.BaseLumaTypes.L_String) and luma_types.LumaTypeCheck(value_right, luma_types.BaseLumaTypes.L_String):
                try:
                    value = self.__string_and_string_suported_operatios[self.__operation](value_left.get_value(), value_right.get_value())
                    return luma_values.LumaValue.create(value)
                except: luma_excepts.call_exception_not_suport_operation(self.file, self.__operation, value_left, value_right, self.pos)
            elif luma_types.LumaTypeCheck(value_left, luma_types.BaseLumaTypes.L_String) and luma_types.LumaTypeCheck(value_right, luma_types.BaseLumaTypes.L_Int):
                try:
                    value = self.__string_and_number_suported_operations[self.__operation](value_left.get_value(), value_right.get_value())
                    return luma_values.LumaValue.create(value)
                except: luma_excepts.call_exception_not_suport_operation(self.file, self.__operation, value_left, value_right, self.pos)
            elif luma_types.LumaTypeCheck(value_left, luma_types.BaseLumaTypes.L_Char) and luma_types.LumaTypeCheck(value_right, luma_types.BaseLumaTypes.L_Int):
                try:
                    value = self.__char_and_number_suported_operations[self.__operation](value_left.get_value(), value_right.get_value())
                    return luma_values.LumaValue.create(value)
                except: luma_excepts.call_exception_not_suport_operation(self.file, self.__operation, value_left, value_right, self.pos)
            elif luma_types.LumaTypeCheck(value_left, luma_types.BaseLumaTypes.L_List) and luma_types.LumaTypeCheck(value_right, luma_types.BaseLumaTypes.L_List):
                try:
                    value = self.__list_and_list_suported_operations[self.__operation](value_left.get_value(), value_right.get_value())
                    return luma_values.LumaValue.create(value, luma_types.BaseLumaTypes.L_List)
                except: luma_excepts.call_exception_not_suport_operation(self.file, self.__operation, value_left, value_right, self.pos)
            else:
                luma_excepts.call_exception_not_suport_operation(self.file, self.__operation, value_left, value_right, self.pos)
                
    class NodeBinareCondition(BaseExpression):
        def __init__(self, operation: str, left_expression, right_expression, file, pos) -> None:
            super().__init__(file, pos)
            self.__operation = operation
            self.__left_expression = left_expression
            self.__right_expression = right_expression

            self.__bool_and_bool_suported_operations = {
                '&&': lambda v1, v2: v1 and v2,
                '||': lambda v1, v2: v1 or v2,
                '==': lambda v1, v2: v1 == v2,
                '!=': lambda v1, v2: v1 != v2,
            }

            self.__number_and_number_suported_operations = {
                '==': lambda v1, v2: v1 == v2,
                '!=': lambda v1, v2: v1 != v2,
                '>': lambda v1, v2: v1 > v2,
                '<': lambda v1, v2: v1 < v2,
                '>=': lambda v1, v2: v1 >= v2,
                '<=': lambda v1, v2: v1 <= v2,
            }

            self.__any_and_any_suported_operations = {
                '==': lambda v1, v2: v1 == v2,
                '!=': lambda v1, v2: v1 != v2,
            }

        def eval(self):
            
            value_left = self.__left_expression.eval()
            value_right = self.__right_expression.eval()

            if luma_types.LumaTypeCheck(value_left, luma_types.BaseLumaTypes.L_Bool) and luma_types.LumaTypeCheck(value_right, luma_types.BaseLumaTypes.L_Bool):
                try:
                    value = self.__bool_and_bool_suported_operations[self.__operation](value_left.get_value(), value_right.get_value())
                    return luma_values.LumaValue.create(value)
                except: luma_excepts.call_exception_not_suport_operation(self.file, self.__operation, value_left, value_right, self.pos)
                
            elif luma_types.LumaTypesCheck(value_left, [luma_types.BaseLumaTypes.L_Int, luma_types.BaseLumaTypes.L_Float]) and luma_types.LumaTypesCheck(value_right, [luma_types.BaseLumaTypes.L_Int, luma_types.BaseLumaTypes.L_Float]):
                try:
                    value = self.__number_and_number_suported_operations[self.__operation](value_left.get_value(), value_right.get_value())
                    return luma_values.LumaValue.create(value)
                except: luma_excepts.call_exception_not_suport_operation(self.file, self.__operation, value_left, value_right, self.pos)
            else:
                try:
                    value = self.__any_and_any_suported_operations[self.__operation](value_left.get_value(), value_right.get_value())
                    return luma_values.LumaValue.create(value)
                except: luma_excepts.call_exception_not_suport_operation(self.file, self.__operation, value_left, value_right, self.pos)

            luma_excepts.call_exception_not_suport_operation(self.file, self.__operation, value_left, value_right, self.pos)
            
    class NodeBaseVariableGet(BaseExpression):
        def __init__(self, var_name: str, memory: memory.Memory, file, pos) -> None:
            super().__init__(file, pos)  
            self.__var_name = var_name
            self.__memory = memory

        def eval(self):
            if self.__memory.is_exist(self.__var_name):
                return self.__memory.read(self.__var_name).value
            else:
                luma_excepts.call_exception_base_vaiable_not_found(self.file, self.__var_name, self.pos)

    class NodeLambdaCreate(BaseExpression):
        def __init__(self, file, pos, arguments: luma_argmunets.LumaArguments, expression: BaseExpression) -> None:
            super().__init__(file, pos)
            self.__arguments = arguments
            self.__expression = expression

        def eval(self):
            return luma_values.L_Lambda.set_value( luma_lambdas.LumaLambda(self.__expression, self.__arguments))
        
    class NodeCall(BaseExpression):
        def __init__(self, file, pos, name: str, arguments: luma_argmunets.LumaTheseArguments, args_pos, memory: memory.Memory) -> None:
            super().__init__(file, pos)
            self.__these_arguments = arguments
            self.__name = name
            self.__memory = memory
            self.__args_pos = args_pos
        
        def eval(self):
            if not self.__memory.is_exist(self.__name):
                luma_excepts.call_exception_base_vaiable_not_found(self.file, self.__name, self.pos)

            inner_memory = memory.Memory()

            memory_object = self.__memory.read(self.__name)
            if memory_object.value.get_type() == luma_types.BaseLumaTypes.L_Lambda:
                
                lambda_object = memory_object.value.get_value()
                wait_arguments: luma_argmunets.LumaArguments = lambda_object.arguments
                if luma_argmunets.cheack_count(wait_arguments, self.__these_arguments):
                    
                    # set argument values in inner memory
                    for arg in wait_arguments.arguments:
                        if arg.standart_value is not None:
                            inner_memory.write(arg.name, arg.standart_value, memory.MemoryObjectTypes.mutable)
                    

                else:
                    luma_excepts.call_warning_args_count(self.file, self.__args_pos)
                    luma_excepts.call_exceprion_callable_error_argument_count(self.file, self.pos, self.__name, wait_arguments.count, self.__these_arguments.count)
            else:
                luma_excepts.call_warning_variable_is_not_callable(self.file, self.pos, self.__name, memory_object.value)
            
            