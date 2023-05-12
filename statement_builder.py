from table import Table
from column import *
import logconfig

logger=logconfig.config_logger(__name__, "logs/statements.log")

def select_all_stmt(table: Table, clause=""):
   query=f"SELECT * FROM {table.name}" 
   if clause:
      query += f" {clause}"

   query += ";"

   return query

def select_cols_stmt(table: Table, columns: list, clause=""):
   col_names=[c.name for c in columns]

   query="SELECT "+", ".join(col_names) + f" FROM {table.name}"
   
   if clause:
         query += f" {clause}"

   query += ";"

   return query

def create_table_stmt(table: Table):
   statement= f"CREATE TABLE IF NOT EXISTS {table.name} (\n " + ",\n ".join(table.get_column_definitions()) + f",\n {table.primary_key.get_pkey_statement()}"
   if table.fkeys:
      fkey_statements=[f.get_fkey_statement() for f in table.fkeys]
      statement +=",\n "+",\n ".join(fkey_statements)
   statement +="\n );"
   logger.info(statement)

   return statement

def insert_stmt(table: Table):
   col_num=len(table.basic_columns)
   vals=["?"] * col_num
   statement="INSERT INTO " + table.name + " VALUES " + "(" +", ".join(vals)+");"
   logger.info(statement)

   return statement

def insert_or_update_stmt(table: Table):
   cols=list(filter(lambda x: not isinstance(x, Primary), table.basic_columns))
   col_num=len(table.basic_columns)
   vals=["?"] * col_num
   upd=[c.name + " = ?" for c in cols]

   statement=f"INSERT INTO {table.name} VALUES (" +", ".join(vals)+f""")
 ON CONFLICT({table.primary_key.name}) DO UPDATE
 SET\n """+",\n ".join(upd) +";"

   logger.info(statement)

   return statement

def update_stmt(table: Table):
      cols=list(filter(lambda x: not isinstance(x, Primary), table.basic_columns))
      upd=[c.name + " = ?" for c in cols]

      statement=f"UPDATE {table.name} SET "+", ".join(upd) +f" WHERE {table.primary_key.name} = ?;"
      logger.info(statement)

      return statement


def delete_stmt(table: Table, cols: list):

   statement=f"DELETE FROM {table.name} WHERE {cols[0].name} = ?"

   if len(cols) > 1:
      for c in cols[1:]:
         statement += f" AND {c.name} = ? "
      
      statement=statement[:-1]

   statement += ";"
   logger.info(statement)

   return statement