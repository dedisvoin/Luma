
from copy import copy


class MemoryObjectTypes:
    VARIABLE = 'VARIABLE'
    LAMBDA = 'LAMBDA'
    FUNCTION = 'FUNCTION'


class MemoryObject:
    def __init__(self, name: str, value: any, mutable: bool, type: MemoryObjectTypes, cached = False) -> None:
        self.__name = name
        self.__value = value
        self.__type = type
        self.__mutable = mutable
        self.__cached = cached
        self.__cache_clear_depth = 3

    @property
    def cached(self) -> bool: return self.__cached

    @property
    def value(self) -> any: return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def type(self) -> str: return self.__type

    @property
    def name(self) -> any: return self.__name

    @property
    def mutable(self) -> bool: return self.__mutable

    


class RunTimeMemory:
    def __init__(self) -> None:
        self.__memory = []
        self.__buffer_memory = []
        self.__cache_clear_depth = 3

    @property
    def cache_clear_depth(self) -> int: return self.__cache_clear_depth

    @cache_clear_depth.setter
    def cache_clear_depth(self, value: int):
        self.__cache_clear_depth = value

    def GetObjectsWithNames(self, names: list[str]) -> list[MemoryObject]:
        objects = []
        for obj in self.__memory:
            if obj.name in names:
                objects.append(obj)
        return objects
    
    def ClearCache(self):
        for _ in range(self.__cache_clear_depth):
            for obj in self.__memory:
                if obj.cached:
                    del self.__memory[self.__memory.index(obj)]
                

    def GetObject(self, name: str, type: MemoryObjectTypes) -> MemoryObject:
        for obj in self.__memory:
            if obj.name == name and obj.type == type:
                return obj
        return None
    
    def GetObjectWithoutType(self, name: str) -> MemoryObject:
        for obj in self.__memory:
            if obj.name == name:
                return obj
        return None
    
    def BufferizeMemory(self):
        self.__buffer_memory = []
        for obj in self.__memory:
            self.__buffer_memory.append(copy(obj))

    def UnBufferizeMemory(self):
        self.__memory = []
        for obj in self.__buffer_memory:
            self.__memory.append(copy(obj))
        #print('Unbuferize', len(self.__memory))

    def get_memory(self) -> list[MemoryObject]: return self.__memory

    def ReadObject(self, name: str) -> MemoryObject:
        for obj in self.__memory:
            if obj.name == name: return obj
        return None

    def WriteObject(self, memory_object: MemoryObject):
        if self.ContainsObject(memory_object):
            self.UpdateObject(memory_object)
        else:
            self.__memory.append(memory_object)

    def DeleteObject(self, name: str, type: MemoryObjectTypes):
        for obj in self.__memory:
            if obj.name == name and obj.type == type:
                self.__memory.remove(obj)
                break
    
    def DeleteObjectWithoutType(self, name: str):
        for obj in self.__memory:
            if obj.name == name:
                self.__memory.remove(obj)
                break

    def UpdateObject(self, memory_object: MemoryObject):
        for obj in self.__memory:
            if obj.name == memory_object.name and obj.type == memory_object.type:
                obj.value = memory_object.value

    def ContainsObject(self, memory_object: MemoryObject):
        for obj in self.__memory:
            if obj.name == memory_object.name and obj.type == memory_object.type:
                return True
        else:
            return False
        
    def ConatinsWithNameAndType(self, name: str, type: MemoryObjectTypes):
        for obj in self.__memory:
            if obj.name == name and obj.type == type:
                return True
        else:
            return False
    
    def ContainWithNameObject(self, name: str):
        for obj in self.__memory:
            if obj.name == name: return True
        return False
    
