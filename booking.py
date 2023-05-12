from bouncycastle import BouncyCastle
from customer import Customer
from address import Address

class Booking():        
    def __init__(self, 
                 id: int,
                 date: str, 
                 customer: Customer, 
                 bouncy_castle: BouncyCastle,
                 delivery_address: Address):
        
        self.__id=id
        self.__date=date
        self.__customer=customer
        self.__bouncy_castle=bouncy_castle
        self.__delivery_address=delivery_address
        

    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, id: int) -> None:
        self.__id=id

    @property
    def date(self) -> str:
        return self.__date
    
    @date.setter
    def date(self, date: str) -> None:
        self.__date=date

    @property
    def customer(self) -> Customer:
        return self.__customer
    
    @customer.setter
    def customer(self, customer: Customer) -> None:
        self.__customer=customer

    @property
    def bouncy_castle(self) -> BouncyCastle:
        return self.__bouncy_castle
    
    @bouncy_castle.setter
    def bouncy_castle(self, bouncy_castle: BouncyCastle) -> None:
        self.__bouncy_castle=bouncy_castle

    @property
    def delivery_address(self) -> Address:
        return self.__delivery_address

    @delivery_address.setter
    def delivery_address(self, delivery_address: Address) -> None:
        self.__delivery_address=delivery_address

    def __str__(self) -> str:
        return f"{self.__id} {self.__date} {self.__bouncy_castle.name} {self.customer}"
    
    def __repr__(self) -> str:
        return f"{self.__id} {self.__date} {self.__bouncy_castle.name} {self.customer}"


    