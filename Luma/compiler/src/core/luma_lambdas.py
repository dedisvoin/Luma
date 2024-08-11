from copy import copy
from src.core import luma_argmunets

class LambdaType:
    Luma = 'Luma'
    Python = 'Python'

class LumaLambda:
    def __init__(self, expression, arguments) -> None:
        self.__expression = expression
        self.__arguments = arguments
        self.__call_type = LambdaType.Luma

    @property
    def type(self):
        return self.__call_type

    @property
    def arguments(self): 
        return self.__arguments
