

from copy import copy
from typing import Any
from src.core import luma_types

class LumaValue:
    def __init__(self, value: Any, type: luma_types.LumaType | None = None) -> None:
        self.__value = value
        self.__type = luma_types.GetBaseLumaType(value) if type is None else type
        self.__out_function = None
        

    def set_out_function(self, func: callable):
        self.__out_function = func

    def get_value(self) -> Any:
        return self.__value
    
    def set_value(self, value):
        self.__value = value
        #self.__v_type = luma_types.GetBaseLumaType(value) if type is None else type
    
        return copy(self)
    
    def get_out_value(self) -> Any:
        if self.__out_function is None:
            return self.__value
        else:
            return self.__out_function(self.__value)
    
    def get_type(self):
        return self.__type

    @classmethod
    def create(self, value: Any, type: luma_types.LumaType | None = None) -> 'LumaValue':
        return LumaValue(value, type)
    
    def copy_value(self):
        return copy(self)
    

L_True = LumaValue.create(True)
L_False = LumaValue.create(False)
L_Int = LumaValue.create(0, luma_types.BaseLumaTypes.L_Int)
L_Float = LumaValue.create(0.0, luma_types.BaseLumaTypes.L_Float)
L_String = LumaValue.create('', luma_types.BaseLumaTypes.L_String)
L_Char = LumaValue.create('', luma_types.BaseLumaTypes.L_Char)
L_List = LumaValue.create('', luma_types.BaseLumaTypes.L_List)
L_Lambda = LumaValue.create(None, luma_types.BaseLumaTypes.L_Lambda)
L_Lambda.set_out_function(lambda value: value.__name__)