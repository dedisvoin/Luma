import sys
from typing import Any
sys.path.extend('../')

from src.runtime import memory
from src.core import luma_values
from src.core import luma_exceptions
from src.core import tokens
from src.core import luma_types
from src.core import luma_libs
from src.runtime import memory


class CommandBaseVariableSet:
    def __init__(self, memory: memory.RunTimeMemory, 
                 var_name: str, var_expression: Any | None = None, 
                 var_mutable: bool = False, 
                 dummy_value: luma_values.LumaDummyValues = luma_values.LumaDummyValues.ZERO,
                 file_name: str = '',
                 csp: tokens.TokenPosition = None,
                 cep: tokens.TokenPosition = None) -> None:
        self.__var_name = var_name
        self.__expression = var_expression
        self.__mutable = var_mutable
        self.__dummy_value = dummy_value
        self.__memory = memory
        self.__file_name = file_name
        self.__csp = csp
        self.__cep = cep

    def exec(self):
        if self.__expression is not None:
            self.__value = self.__expression.eval()
            
            value_type = memory.MemoryObjectTypes.VARIABLE
            if self.__value.type == luma_types.LumaTypes.get('Lambda'):
                value_type = memory.MemoryObjectTypes.LAMBDA
            if self.__value.type == luma_types.LumaTypes.get('Function'):
                value_type = memory.MemoryObjectTypes.FUNCTION

            writeable_object = memory.MemoryObject(
                self.__var_name, 
                self.__value, 
                self.__mutable, 
                value_type
            )
            
        else:
            writeable_object = memory.MemoryObject(
                self.__var_name, 
                self.__dummy_value,
                self.__mutable,
                memory.MemoryObjectTypes.VARIABLE
            )
        
        if self.__memory.ContainWithNameObject(self.__var_name):
            self.__memory.DeleteObjectWithoutType(self.__var_name)
            
        self.__memory.WriteObject(
            writeable_object
        )

class CommandBaseVariableChainge:
    def __init__(self, memory: memory.RunTimeMemory,
                 var_name: str, var_expression: Any = None,
                 file_name: str = '',
                 csp: tokens.TokenPosition = None,
                 cep: tokens.TokenPosition = None) -> None:
        self.__var_name = var_name
        self.__expression = var_expression
        self.__memory = memory
        self.__file_name = file_name
        self.__csp = csp
        self.__cep = cep

    def exec(self):
        if self.__expression is not None:
            self.__value = self.__expression.eval()
            value_type = memory.MemoryObjectTypes.VARIABLE
            if self.__value.type == luma_types.LumaTypes.get('Lambda'):
                value_type = memory.MemoryObjectTypes.LAMBDA

            writeable_object = memory.MemoryObject(
                self.__var_name, 
                self.__value,
                True,
                value_type
            )
            if self.__memory.ContainWithNameObject(self.__var_name):
                if self.__memory.GetObjectWithoutType(self.__var_name).mutable:
                    self.__memory.DeleteObjectWithoutType(self.__var_name)
                    self.__memory.WriteObject(
                        writeable_object
                    )
                else:
                    luma_exceptions.VariableChainge(self.__file_name, tokens.TokensLinePos(self.__csp, self.__cep), self.__var_name).LumaRaise()
            else:
                luma_exceptions.VariableNotFound(self.__file_name, tokens.TokensLinePos(self.__csp, self.__cep), self.__var_name).LumaRaise()

class CommandBaseVariableDelete:
    def __init__(self, memory: memory.RunTimeMemory,
                 var_names: list[str], file_name: str = '', pos: tokens.TokenPosition = None) -> None:
        self.__memory = memory
        self.__var_names = var_names
        self.__file_name = file_name
        self.__pos = pos

    def exec(self):
        for var in self.__var_names:
            
            if self.__memory.ContainWithNameObject(var[0]):
                self.__memory.DeleteObjectWithoutType(var[0])
            else:
                luma_exceptions.VariableNotFound(self.__file_name, var[1], var[0]).LumaRaise()

class CommandLoadFile:
    def __init__(self, memory: memory.RunTimeMemory,
                 file_path: str, file_name: str = '', pos: tokens.TokenPosition = None, end_pos: tokens.TokenPosition = None, file_extension: str = '') -> None:
        self.__memory = memory
        self.__file_path = file_path
        self.__file_name = file_name
        self.__pos = pos
        self.__end_pos = end_pos
        self.__file_extension = file_extension


    def exec(self):
        lib = luma_libs.load_python_file(self.__file_path + '.' + self.__file_extension)
        lib_functions = lib.fs
        for func in lib_functions.functions:
            self.__memory.WriteObject(
                memory.MemoryObject(
                    luma_libs.get_lib_name(self.__file_path)+func.name,
                    luma_values.FunctionValue.Create(func),
                    True, 
                    memory.MemoryObjectTypes.FUNCTION
                )
            )

class CommandCall:
    def __init__(self, 
                    this_memory: memory.RunTimeMemory,
                    file_name: str, 
                    start_pos:tokens.TokenPosition, 
                    pos: tokens.TokenPosition,  
                    variable_name: str, 
                    arguments_expression: list) -> None:
        self.__var_name = variable_name
        self.__arguments_expression = arguments_expression
        self.__memory = this_memory
        self.__file_name = file_name
        self.__pos = pos
        self.__start_pos = start_pos

    def exec(self):  
        if self.__memory.ConatinsWithNameAndType(self.__var_name, memory.MemoryObjectTypes.FUNCTION):
            function_object = self.__memory.GetObject(self.__var_name, memory.MemoryObjectTypes.FUNCTION)
            if len(self.__arguments_expression) != len(function_object.value.value.waited_value_names) and not function_object.value.value.args_count_ignore:
                luma_exceptions.ArgumentCountError(self.__file_name, tokens.TokensLinePos(self.__start_pos, self.__pos), self.__var_name, len(self.__arguments_expression), len(function_object.value.value.waited_value_names)).LumaRaise()
            else:
                if not function_object.value.value.args_count_ignore:
                    self.__memory.BufferizeMemory()
                    for i in range(len(self.__arguments_expression)):
                        value = self.__arguments_expression[i].eval()
                        type = luma_values.get_memory_type(value)
                        self.__memory.WriteObject(
                            memory.MemoryObject(function_object.value.value.waited_value_names[i], value, False, type, True))
                    if function_object.value.value.FUNCTION_TYPE == 'Python':
                        function_object.value.value.callable_object(self.__memory.GetObjectsWithNames(function_object.value.value.waited_value_names))
                    elif function_object.value.value.FUNCTION_TYPE == 'Luma':
                        function_object.value.value.callable_object.exec()
                else:
                    self.__memory.BufferizeMemory()
                    new_names = []
                    for i in range(len(self.__arguments_expression)):
                        
                        value = self.__arguments_expression[i].eval()
                        type = luma_values.get_memory_type(value)
                        self.__memory.WriteObject(
                            memory.MemoryObject(function_object.value.value.waited_value_names[0]+'**'+str(i), value, False, type, True))
                        new_names.append(function_object.value.value.waited_value_names[0]+'**'+str(i))
                    
                    function_object.value.value.callable_object(self.__memory.GetObjectsWithNames(new_names))
        else:   
            luma_exceptions.VariableNotFound(self.__file_name, self.__pos, self.__var_name).LumaRaise()

class CommandCallLib:
    def __init__(self, 
                    this_memory: memory.RunTimeMemory,
                    file_name: str, 
                    start_pos:tokens.TokenPosition, 
                    pos: tokens.TokenPosition,  
                    variable_name: str, 
                    arguments_expression: list,
                    lib_name: str,
                    all_libs: list[str]) -> None:
        self.__var_name = variable_name
        self.__arguments_expression = arguments_expression
        self.__memory = this_memory
        self.__file_name = file_name
        self.__pos = pos
        self.__start_pos = start_pos
        self.__lib_name = lib_name
        self.__all_libs = all_libs


    def exec(self):  
        
        if self.__lib_name+'.' not in self.__all_libs:
            luma_exceptions.FileNotFound(self.__file_name, self.__pos, self.__lib_name).LumaRaise()

        if self.__memory.ConatinsWithNameAndType(self.__lib_name+'.'+self.__var_name, memory.MemoryObjectTypes.FUNCTION):
            function_object = self.__memory.GetObject(self.__lib_name+'.'+self.__var_name, memory.MemoryObjectTypes.FUNCTION)
            if len(self.__arguments_expression) != len(function_object.value.value.waited_value_names) and not function_object.value.value.args_count_ignore:
                luma_exceptions.ArgumentCountError(self.__file_name, tokens.TokensLinePos(self.__start_pos, self.__pos), self.__lib_name+'.'+self.__var_name, len(self.__arguments_expression), len(function_object.value.value.waited_value_names)).LumaRaise()
            else:
                if not function_object.value.value.args_count_ignore:
                    self.__memory.BufferizeMemory()
                    for i in range(len(self.__arguments_expression)):
                        value = self.__arguments_expression[i].eval()
                        type = luma_values.get_memory_type(value)
                        self.__memory.WriteObject(
                            memory.MemoryObject(function_object.value.value.waited_value_names[i], value, False, type, True))
                    function_object.value.value.callable_object(self.__memory.GetObjectsWithNames(function_object.value.value.waited_value_names))
                else:
                    self.__memory.BufferizeMemory()
                    new_names = []
                    for i in range(len(self.__arguments_expression)):
                        
                        value = self.__arguments_expression[i].eval()
                        type = luma_values.get_memory_type(value)
                        self.__memory.WriteObject(
                            memory.MemoryObject(function_object.value.value.waited_value_names[0]+'**'+str(i), value, False, type, True))
                        new_names.append(function_object.value.value.waited_value_names[0]+'**'+str(i))
                    
                    function_object.value.value.callable_object(self.__memory.GetObjectsWithNames(new_names))
        else:   
            luma_exceptions.VariableNotFound(self.__file_name, self.__pos, self.__lib_name+'.'+self.__var_name).LumaRaise()

class CommandCreateCommandsList:
    def __init__(self, commands: list) -> None:
        self.__commands = commands

    def exec(self):
        for command in self.__commands:
            
            command.exec()
            

class CommandFor:
    def __init__(self, var_set_command, condition, sum_command, executed_commands, file_name, pos) -> None:
        self.__var_set_command = var_set_command
        self.__condition = condition
        self.__sum_command = sum_command
        self.__executed_commands = executed_commands
        self.__file_name = file_name
        self.__pos = pos
    
    def exec(self):
        self.__var_set_command.exec()
        while self.__condition.eval().value == True:
            self.__executed_commands.exec()
            self.__sum_command.exec()
