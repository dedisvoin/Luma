from src.runtime import memory

class LambdaConstruct:
    def __init__(self, waited_value_names: list[str], expression) -> None:
        self.__waited_value_names = waited_value_names
        self.__expression = expression

    @property
    def waited_value_names(self) -> list[str]: return self.__waited_value_names

    @property
    def expression(self): return self.__expression