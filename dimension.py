
class Dimension():
    def __init__(self, id: int, values: str):
        self.__id=id
        self.__values=values

    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, id: int) -> None:
        self.__id=id

    @property
    def values(self) -> str:
        return self.__values
    
    @values.setter
    def dimension(self, values: str) -> None:
        self.__values=values

    def __str__(self) -> str:
        return self.__values
    
    def __repr__(self) -> str:
        return self.__values



