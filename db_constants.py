from enum import Enum

class Constraint(str, Enum):
    PKEY="PRIMARY KEY"
    FKEY="FOREIGN KEY"
    U="UNIQUE"
    NN="NOT NULL"
    INCR="AUTOINCREMENT"
    INCR_M="AUTO_INCREMENT"
    DEF0="DEFAULT 0"
    DEL_CASC="ON DELETE CASCADE"
    DEL_DEF="ON DELETE SET DEFAULT"


class DataType(str, Enum):
    INT="INTEGER"
    TXT="TEXT"
    REAL="REAL"
    BOOL="BOOLEAN"

class DBCommand(str, Enum):
    INS="INSERT"
    DEL="DELETE"
    UPD="UPDATE"
    




