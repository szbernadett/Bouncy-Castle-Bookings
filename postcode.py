from city import City

class Postcode():
    def __init__(self,
                 id: int,
                 postcode: str, 
                 city: City):
        
        self.__id=id
        self.__postcode=postcode
        self.__city=city

    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, id: int):
        self.__id=id

    @property
    def postcode(self) -> str:
        return self.__postcode

    @postcode.setter
    def postcode(self, postcode: str):
        self.__postcode=postcode

    @property
    def city(self) -> City:
        return self.__city
    
    @city.setter
    def city(self, city: City):
        self.__city=city

    def __str__(self) -> str:
        return self.__postcode
    
    def __repr__(self) -> str:
        return self.__postcode

