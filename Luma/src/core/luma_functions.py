from typing import Callable
from src.core import luma_types
import inspect

class LumaFunction:
    def __init__(self, name: str | None = None, file_name: str = '', 
                 waited_args: list[str] = [], waited_args_count: int = 0, 
                 returned: bool = False, args_count_ignore: bool = False,
                 types: list[luma_types.LumaType] | None = None) -> 'LumaFunction':
        self.__name = name
        self.__file_name = file_name
        self.__waited_args = waited_args
        self.__waited_args_count = waited_args_count
        self.__returned = returned
        self.__call_function = None
        self.__args_count_ignore = args_count_ignore
        self.__types = types

        self.FUNCTION_TYPE = None

    @property
    def types(self) -> list[luma_types.LumaType]: return self.__types

    def set_python_function(self, function: Callable):
        self.__call_function = function

    def set_luma_statements(self, statements):
        self.__call_function = statements

    @property
    def args_count_ignore(self) -> bool: return self.__args_count_ignore

    @property
    def callable_object(self) -> Callable:
        return self.__call_function
    
    @property
    def name(self) -> str: return self.__name

    @property
    def returned(self) -> bool: return self.__returned

    @property
    def waited_value_names(self) -> int: return self.__waited_args

    @classmethod
    def ConstructPythonFunction(self, function: Callable, 
                                name: str | None = None, returned: bool = False, 
                                args_count_ignore: bool = False, types: list[luma_types.LumaType] = []) -> 'LumaFunction':
        code = function.__code__
        
        lf_file_name = code.co_filename
        if name is not None:
            lf_name = name
        else:
            lf_name = code.co_name
        lf_returned = returned
        lf_waited_args = list(inspect.signature(function).parameters.keys())
        lf_args_count = len(lf_waited_args)
        lf = LumaFunction(
            lf_name,
            lf_file_name,
            lf_waited_args,
            lf_args_count,
            lf_returned,
            args_count_ignore,
            types
        )
        lf.set_python_function(function)
        lf.FUNCTION_TYPE = 'Python'
        return lf

    @classmethod
    def ConstructLumaFunction(self, function_statements, name, returned: bool = False, file_name: str = '', waited_args: list = []):
        lf = LumaFunction(
            name,
            file_name,
            waited_args,
            len(waited_args),
            returned,
            False, None
        )
        lf.set_luma_statements(function_statements)
        lf.FUNCTION_TYPE = 'Luma'
        return lf


class LumaFunctionsSaver:
    def __init__(self) -> None:
        self.functions = []

    def add(self, luma_function: LumaFunction):
        self.functions.append(luma_function)


def LumaFun(function_saver: LumaFunctionsSaver, name: str | None = None, 
            returned: bool = False,
            args_count_ignore: bool = False,
            types: list[luma_types.LumaType] = []) -> Callable:
    def wrapper(funct: Callable):
        function_saver.add(
            LumaFunction.ConstructPythonFunction(funct, name, returned, args_count_ignore, types)
        )
        
    return wrapper