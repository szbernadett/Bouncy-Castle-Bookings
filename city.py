
class City():
    def __init__(self, id: int, name: str):
        self.__id=id
        self.__name=name

    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, id: int):
        self.__id=id

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str):
        self.name=name

    def __str__(self):
        return self.__name
    
    def __repr__(self):
        return self.__name