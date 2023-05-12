from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from table import Table
from db_constants import Constraint
from abc import ABC
from db_constants import DataType

class Column(ABC):
    def __init__(self, name: str, data_type: DataType, constraints=[]):
        self._name=name
        self._data_type=data_type.value
        constraints=[c for c in constraints]
        self._constraints=" ".join(constraints)

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: str) -> None:
        self._name=name

    @property
    def data_type(self) -> str:
        return self._data_type
    
    @data_type.setter
    def data_type(self, data_type: DataType) -> None:
        self._data_type=data_type.value

    @property
    def constraints(self) -> str:
        return self._constraints
    
    @constraints.setter
    def constraints(self, constraints: list) -> None:
        constraints=[c for c in constraints]
        self._constraints=" ".join(constraints)

    def __str__(self) -> str:
         base=f"{self._name} {self._data_type}"
         return base if not self._constraints else f"{base} {self._constraints}"

    
    def __repr__(self) -> str:
        base=f"{self._name} {self._data_type}"
        return base if not self._constraints else f"{base} {self._constraints}"
    
class Primary(Column):
    def __init__(self, name: str, data_type: DataType, auto_increment=True, constraints=[]):
        super().__init__(name, data_type, constraints)
        self._auto_increment=auto_increment
        self._default_constraint=Constraint.PKEY.value


    @property
    def auto_increment(self) -> bool:
        return self._auto_increment
    
    @auto_increment.setter
    def auto_increment(self, auto_increment: bool) -> None:
        self._auto_increment=auto_increment

    @property
    def default_constraint(self) -> str:
        return self._default_constraint
     
    def get_pkey_statement(self) -> str:
        if self._auto_increment:
            return f"{self._default_constraint}({self._name} {Constraint.INCR})"
        else:
            return f"{self._default_constraint}({self._name})"
           

    
class Foreign(Column):
    def __init__(self, name: str, data_type: DataType, fkey_table: Table, constraints=[], fkey_constraints=[]): 
        super().__init__(name, data_type, constraints)
        self._fkey_table=fkey_table
        fkey_constraints=[f for f in fkey_constraints]
        self._fkey_constraints=" ".join(fkey_constraints)
        self._default_constraint=Constraint.FKEY.value


    @property
    def fkey_constraints(self) -> str:
        return self._fkey_constraints
    
    @fkey_constraints.setter
    def fkey_constraints(self, fkey_constraints: list) -> None:
        fkey_constraints=[f for f in fkey_constraints]
        self._fkey_constraints=" ".join(fkey_constraints)

    def get_fkey_statement(self) -> str:
        stmt= f"{self._default_constraint}({self._name}) REFERENCES {self._fkey_table.name}({self._fkey_table.primary_key.name})"
        if self._fkey_constraints:
           stmt+=f" {self._fkey_constraints}"

        return stmt
      
    

class BasicColumn(Column):
    def __init__(self, name: str, data_type: DataType, constraints=[]):
       super().__init__(name, data_type, constraints)
 

    