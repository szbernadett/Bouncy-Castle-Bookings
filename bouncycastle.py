from dimension import Dimension
from colour import Colour
from price import Price

class BouncyCastle():
    def __init__(self, 
                 id: int,
                 name: str, 
                 dimension: Dimension, 
                 colour: Colour, 
                 price: Price):
        
        self.__id=id
        self.__name=name
        self.__dimension=dimension
        self.__colour=colour
        self.__price=price

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

    @property
    def dimension(self) -> Dimension:
        return self.__dimension
    
    @dimension.setter
    def dimension(self, dimension: Dimension) -> None:
        self.__dimension=dimension

    @property
    def colour(self) -> Colour:
        return self.__colour
    
    @colour.setter
    def colour(self, colour: Colour) -> None:
        self.__colour=colour

    @property
    def price(self) -> Price:
        return self.__price
    
    @price.setter
    def price(self, price: Price) -> None:
        self.__price=price

    def __str__(self) -> str:
        return self.__name
    
    def __repr__(self) -> str:
        return self.__name


        