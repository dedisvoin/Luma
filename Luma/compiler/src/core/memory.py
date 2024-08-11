
from copy import copy
import random
from typing import Any


class MemoryObjectTypes:
    mutable = 'mutable'
    unmutable = 'unmutable'


class MemoryObject:
    def __init__(self, name: str, mutable_type: MemoryObjectTypes = MemoryObjectTypes.mutable, value = None) -> None:
        self.__value = value
        self.__name = name
        self.__mutable_type = mutable_type
        self.__inited = False if self.__value is None else True
        self.__id = None

    @property
    def id(self) -> int | None:
        return self.__id
    
    @id.setter
    def id(self, value):
        self.__id = id
        
    @property
    def inited(self) -> bool:
        return self.__inited

    @property
    def name(self) -> str : return self.__name

    @property
    def value(self) : return self.__value

    @property
    def mutable_type(self) -> str : return self.__mutable_type

    @property
    def mutable(self) -> bool : return True if self.__mutable_type == MemoryObjectTypes.mutable else False

class Memory:
    def __init__(self) -> None:
        self.__rom: list[MemoryObject] = []
        self.__buffer_rom: list[MemoryObject] = []
        self.__id = random.randint(0, 99999999999999)

    def id(self) -> int:
        return self.__id

    def get(self):
        return self.__rom
    
    
    def get_rom(self) -> list[MemoryObject]:
        #!NOT BE USE THIS YOU CODE
        return self.__rom
    
    def merge(self, memory: 'Memory'):
        self.__rom += memory.get_rom()

    def __get_object_to_name__(self, name: str) -> MemoryObject | None:
        for obj in self.__rom:
            if obj.name == name:
                return obj
        return None


    def is_exist(self, name: str):
        for obj in self.__rom:
            if obj.name == name: return True
        return False
    

    def is_mutable(self, name: str):
        for obj in self.__rom:
            if obj.name == name: return obj.mutable
        return None


    def delete(self, name: str):
        for obj in self.__rom:
            if obj.name == name: 
                self.__rom.remove(obj)
                break

    def write_to_buffer(self):
        self.__buffer_rom.clear()
        for obj in self.__rom:
            self.__buffer_rom.append(copy(obj))

    def read_to_buffer(self):
        self.__rom.clear()
        for obj in self.__buffer_rom:
            self.__buffer_rom.append(copy(obj))

    def write(self, name: str, value: Any, mutable_type: MemoryObjectTypes):
        if self.is_exist(name):
            self.delete(name)
        
        mo = MemoryObject(name, mutable_type, value)
        mo.id = self.__id
        self.__rom.append(mo)

    def read(self, name: str) -> MemoryObject:
        return self.__get_object_to_name__(name)


    




