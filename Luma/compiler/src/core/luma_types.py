from typing import Any


def string_to_id(string: str) -> int:
    nums_and_chars_ = list(enumerate('abcdefghijklmnopqrstuvwxyz'+'abcdefghijklmnopqrstuvwxyz'.upper()))
    converted_string = ''
    for sym in string:
        for num in nums_and_chars_:
            if sym == num[1]:
                converted_string += str(num[0])
    return int(converted_string)

class LumaType:
    def __init__(self, name: str, id: int | None = None) -> None:
        self.__name = name
        self.__id = string_to_id(self.__name) if id is None else id
        
    @property
    def id(self) -> int : return self.__id

    @property
    def name(self) -> str : return self.__name


class BaseLumaTypes:
    L_String = LumaType('String')
    L_Int = LumaType('Int')
    L_Float = LumaType('Float')
    L_Bool = LumaType('Bool')
    L_Char = LumaType('Char')
    L_Function = LumaType('Function')
    L_Lambda = LumaType('Lambda')
    L_List = LumaType('List')

def GetBaseLumaType(python_value: Any) -> BaseLumaTypes: 
    if isinstance(python_value, str):
        if python_value == 'true':          return BaseLumaTypes.L_Bool
        if python_value == 'false':          return BaseLumaTypes.L_Bool
        if len(python_value) > 1:           return BaseLumaTypes.L_String
        else:                               return BaseLumaTypes.L_Char
    if isinstance(python_value, bool):      return BaseLumaTypes.L_Bool
    if isinstance(python_value, int):       return BaseLumaTypes.L_Int
    if isinstance(python_value, float):     return BaseLumaTypes.L_Float


def GetPyNumberForString(string: str) -> Any:
    if string.count('.') == 0:
        return int(string)
    elif string.count('.') == 1:
        return float(string)
    else:
        raise Exception('Invalid number')
    
def LumaTypeCheck(value, type) -> bool:
    if value.get_type() == type:
        return True
    else:
        return False
    
def LumaTypesCheck(value, types) -> bool:
    if value.get_type() in types:
        return True
    else:
        return False