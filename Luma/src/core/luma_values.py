from copy import copy
from typing import Any
from src.core import luma_types
from src.runtime import memory

class ValueConstruct:
    def __init__(self, type: luma_types.LumaType) -> None:
        self.__type = type
        self.__value = None
        self.__init_function = None

    def set_construct_function(self, funct: callable):
        self.__init_function = funct

    def Create(self, value: str | Any):
        self.__value = self.__init_function(value)
        return copy(self)

    @property
    def value(self) -> any: return self.__value

    @property
    def type(self) -> luma_types.LumaType: return self.__type


IntValue = ValueConstruct(luma_types.LumaTypes.get('Int'))
def IntValueConstruct(value):
    return int(value)
IntValue.set_construct_function(IntValueConstruct)

FloatValue = ValueConstruct(luma_types.LumaTypes.get('Float'))
def FloatValueConstruct(value):
    value = str(value)
    if value.count('.') == 1:
        return float(value)
FloatValue.set_construct_function(FloatValueConstruct)

StringValue = ValueConstruct(luma_types.LumaTypes.get('String'))
def StringValueConstruct(value):
    return str(value)
StringValue.set_construct_function(StringValueConstruct)

BoolValue = ValueConstruct(luma_types.LumaTypes.get('Bool'))
def BoolValueConstruct(value):
    if value == 'true': return True
    if value == 'false': return False
    if value == True: return True
    if value == False: return False

BoolValue.set_construct_function(BoolValueConstruct)

LambdaValue = ValueConstruct(luma_types.LumaTypes.get('Lambda'))
LambdaValue.set_construct_function(lambda obj: obj)

FunctionValue = ValueConstruct(luma_types.LumaTypes.get('Function'))
FunctionValue.set_construct_function(lambda obj: obj)


def LumaTypeCheck(value: ValueConstruct, type: luma_types.LumaTypes):
    if value.type == type:
        return True
    return False

def is_float(number):
    if str(number).count('.') == 1:
        return True
    return False

def is_int(number):
    if str(number).count('.') == 0:
        return True
    return False

def get_memory_type(value: ValueConstruct):
    if value.type.name != luma_types.LumaTypes.get('Lambda').name:
        return memory.MemoryObjectTypes.VARIABLE
    return memory.MemoryObjectTypes.LAMBDA



class LumaDummyValues:
    ZERO = IntValue.Create(0)
    ONE = IntValue.Create(1)
