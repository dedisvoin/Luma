from src.core import luma_types
from src.core import luma_values

from typing import Optional

class LumaArgument:
    def __init__(self, name: str, wait_types: list[luma_types.LumaType], standart_value: Optional[luma_values.LumaValue] = None) -> 'LumaArgument':
        self.__name = name
        self.__wait_types = wait_types
        self.__standart_value = standart_value

    @property
    def name(self) -> str: return self.__name

    @property
    def wait_types(self) -> list[luma_types.LumaType]: return self.__wait_types

    @property
    def standart_value(self) -> Optional[luma_values.LumaValue]: return self.__standart_value

class LumaArguments:
    def __init__(self) -> None:
        self.__arguments: list[LumaArgument] = []
        self.__count = 0

    @property
    def arguments(self):
        return self.__arguments

    @property
    def count(self) -> int: return self.__count

    def add(self, arg: LumaArgument):
        self.__arguments.append(arg)
        self.__count += 1

    def get_argument_with_name(self, name: str) -> Optional[LumaArgument]:
        for arg in self.__arguments:
            if arg.name == name: return arg
        return None
    
    def get_argument_with_index(self, index: int) -> Optional[LumaArgument]:
        return self.__arguments[index]
    
    def get_name_with_index(self, index: int) -> str:
        return self.get_argument_with_index(index).name
    
    

class LumaTheseArgument:
    def __init__(self, expresion) -> None:
        self.__expression = expresion

    @property
    def expression(self): return self.__expression

class LumaTheseArguments:
    def __init__(self) -> None:
        self.__arguments: list[LumaTheseArgument] = []
        self.__count = 0

    @property
    def count(self) -> int: return self.__count

    def add(self, arg: LumaTheseArgument):
        self.__arguments.append(arg)
        self.__count += 1

    def get_argument_with_index(self, index) -> Optional[LumaTheseArgument]:
        return self.__arguments[index]
    
def cheack_count(wait_args: LumaArguments, these_args: LumaTheseArguments):
    if wait_args.count >= these_args.count:
        return True
    return False