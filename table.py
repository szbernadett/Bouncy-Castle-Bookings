from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from column import Primary

from column import Foreign

class Table():
    def __init__(self, name: str, primary_key: Primary, basic_columns: list, fkeys=[]):
        self.__name=name
        self.__primary_key=primary_key
        self.__basic_columns=basic_columns 
        self.__fkeys=fkeys

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        self.__name=name

    @property
    def basic_columns(self) -> list:
        return self.__basic_columns

    @basic_columns.setter
    def basic_columns(self, basic_columns: list) -> None:
        self.__basic_columns=basic_columns

    @property
    def primary_key(self) -> Primary:
        return self.__primary_key
    
    @primary_key.setter
    def primary_key(self, primary_key: Primary) -> None: 
        self.__primary_key=primary_key

    @property
    def fkeys(self) -> list:
        return self.__fkeys
    
    @fkeys.setter
    def fkeys(self, fkeys: list) -> None:
        self.__fkeys=fkeys

    def get_column_definitions(self) -> list:
        col_defs=[str(self.__primary_key)]+[str(c) for c in self.__basic_columns]
        if self.__fkeys:
            col_defs+=[str(f) for f in self.__fkeys]

        return col_defs
    
    
    def __str__(self):
        return self.__name

