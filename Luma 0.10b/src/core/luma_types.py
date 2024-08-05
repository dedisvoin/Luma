

class LumaType:
    def __init__(self, name: str) -> None:
        self.__name = name

    @property
    def name(self) -> str: return self.__name

class LTS:
    def __init__(self) -> None:
        self.lumatypes = {}

    def get(self, name: str): return self.lumatypes[name]


    def __call__(self, lt: LumaType): 
        self.lumatypes[lt.name] = lt





LumaTypes = LTS()
LumaTypes(LumaType('String'))
LumaTypes(LumaType('Int'))
LumaTypes(LumaType('Float'))
LumaTypes(LumaType('Bool'))
LumaTypes(LumaType('Lambda'))
LumaTypes(LumaType('Function'))


def LumaTypeCheck(value, types: LumaType | list[LumaType]) -> bool:
    if value.value.type.name in [t.name for t in types]: return True
    return False