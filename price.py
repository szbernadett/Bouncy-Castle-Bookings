
class Price():
    def __init__(self, id: int, value: str):
        self.__id=id
        self.__value=value

    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, id: int) -> None:
        self.__id=id

    @property
    def value(self) -> str:
        return self.__value
    
    @value.setter
    def value(self, value: str) -> None:
        self.__value=value

    def __str__(self) -> str:
        return self.__value
    
    def __repr__(self) -> str:
        return self.__value

