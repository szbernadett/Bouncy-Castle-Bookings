
class Colour():
    def __init__(self, id: int, name: str):
        self.__id=id
        self.__name=name

    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, id: int) -> None:
        self.__id=id

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str) -> None:
        self.__name=name

    def __str__(self) -> str:
        return self.__name
    
    def __repr__(self) -> str:
        return self.__name
  