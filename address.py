from postcode import Postcode
from city import City

class Address():
    def __init__(self, 
                 id: int,
                 address_line_1: str, 
                 address_line_2: str, 
                 postcode: Postcode):
        
        self.__id=id
        self.__address_line_1=address_line_1
        self.__address_line_2=address_line_2
        self.__postcode=postcode

    @property
    def id(self) -> str:
        return self.__id
    
    @id.setter
    def id(self, id: int) -> None:
        self.__id=id

    @property
    def address_line_1(self) -> str:
        return self.__address_line_1
    
    @address_line_1.setter
    def address_line_1(self, address_line_1: str) -> None:
        self.__address_line_1=address_line_1

    @property
    def address_line_2(self) -> str:
        return self.__address_line_2
    
    @address_line_2.setter
    def address_line_2(self, address_line_2: str) -> None:
        self.__address_line_2=address_line_2

    @property
    def postcode(self) -> Postcode:
        return self.__postcode
    
    @postcode.setter
    def postcode(self, postcode: Postcode) -> None:
        self.__postcode=postcode

    def __str__(self) -> str:
        return f"{self.__address_line_1} {self.__postcode.postcode}"
    
    def __repr__(self) -> str:
        return f"{self.__address_line_1} {self.__postcode.postcode}"