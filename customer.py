from address import Address

class Customer():
    def __init__(self,
                 id: int,
                 first_name: str, 
                 last_name: str,
                 phone_num: str, 
                 email: str, 
                 address: Address):
        
        self.__id=id
        self.__first_name=first_name
        self.__last_name=last_name
        self.__phone_num=phone_num
        self.__email=email
        self.__address=address

    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, id: int) -> None:
        self.__id=id

    @property
    def first_name(self) -> str:
        return self.__first_name
    
    @first_name.setter
    def first_name(self, first_name: str) -> None:
        self.__first_name=first_name

    @property
    def last_name(self) -> str:
        return self.__last_name
    
    @last_name.setter
    def last_name(self, last_name: str) -> None:
        self.__last_name=last_name

    @property
    def phone_num(self) -> str:
        return self.__phone_num
    
    @phone_num.setter
    def phone_num(self, phone_num: str) -> None:
        self.__phone_num=phone_num

    @property
    def email(self) -> str:
        return self.__email
    
    @email.setter
    def email(self, email: str) -> None:
        self.__email=email

    @property
    def address(self) -> Address:
        return self.__address
    
    @address.setter
    def address(self, address: Address):
        self.__address=address

    def __str__(self) -> str:
        return f"{self.__first_name} {self.__last_name}"
    
    def __repr__(self) -> str:
        return f"{self.__first_name} {self.__last_name}"
