
from mysql import connector
import pandas as pd

from GlobalVariables.GlobalVariables import GlobalVariablesPath

class MySQL_DB:
    def __init__(self):
        self.GVP = GlobalVariablesPath()

    # Connecting to MySQL --------------------------------------------
    def connect_to_MySQL(self):
        MySQL = connector.connect(host= self.GVP.MySQL_Variables["host"],
                                  user=self.GVP.MySQL_Variables["user"],
                                  password=self.GVP.MySQL_Variables["pwd"]
                                  )
        SQL_Cursor = MySQL.cursor()
        return MySQL, SQL_Cursor

    # Connecting to database ------------------------------------------
    def connect_to_database(self, DB_Name):
        MyDB = connector.connect(host= self.GVP.MySQL_Variables["host"],
                                 user=self.GVP.MySQL_Variables["user"],
                                 password=self.GVP.MySQL_Variables["pwd"],
                                 database=DB_Name
                                 )
        DB_Cursor = MyDB.cursor()
        return MyDB, DB_Cursor

    # Returns list of database names available in MySQL
    def list_of_databases(self):
        MySQL, SQL_Cursor = self.connect_to_MySQL()
        SQL_Cursor.execute("SHOW DATABASES")
        dataBaseNames = [x[0] for x in SQL_Cursor]
        MySQL.close()
        return dataBaseNames

    # Returns list of table names available in database
    def list_of_tables_in_DB(self, DB_Name):
        MyDB, DB_Cursor = self.connect_to_database(DB_Name)
        DB_Cursor.execute("SHOW TABLES")
        tableNames = [x[0] for x in DB_Cursor]
        MyDB.close()
        return tableNames

    def create_DB(self, DB_Name):
        MySQL, SQL_Cursor = self.connect_to_MySQL()
        if DB_Name not in self.list_of_databases():
            query = "CREATE DATABASE " + DB_Name
            SQL_Cursor.execute(query)
            print(f"Database '{DB_Name}' is created successfully")
        else:
            print(f"Database '{DB_Name}' already exists")
        MySQL.close()

    def drop_DB(self, DB_Name):
        MySQL, SQL_Cursor = self.connect_to_MySQL()
        if DB_Name in self.list_of_databases():
            query = "DROP DATABASE " + DB_Name
            SQL_Cursor.execute(query)
            print(f"Database '{DB_Name}' is dropped successfully")
        else:
            print(f"Database '{DB_Name}' doesn't exist")
        MySQL.close()

    def create_table_in_DB(self, DB_Name, Table_Name, Columns):
        MyDB, DB_Cursor = self.connect_to_database(DB_Name)
        # Creating the table if table doesn't present in database
        if DB_Name not in self.list_of_tables_in_DB(DB_Name):
            query = "CREATE TABLE " + Table_Name + " " + Columns
            DB_Cursor.execute(query)
            print(f"Table '{Table_Name}' is created successfully in the database '{DB_Name}'")

        # Dropping the table and agian creating if table presents in database
        else:
            print(f"Table '{Table_Name} already exists in the database '{DB_Name}'")
            self.drop_table_in_DB(DB_Name, Table_Name)
            self.create_table_in_DB(DB_Name, Table_Name, Columns)
        MyDB.close()

    def drop_table_in_DB(self, DB_Name, Table_Name):
        MyDB, DB_Cursor = self.connect_to_database(DB_Name)
        if Table_Name in self.list_of_tables_in_DB(DB_Name):
            query = "DROP TABLE " + Table_Name
            DB_Cursor.execute(query)
            print(f"Table '{Table_Name}' is dropped successfully from the database '{DB_Name}'")
        else:
            print(f"Table '{Table_Name} doesn't exist in the database '{DB_Name}'")
        MyDB.close()

    def create_table_as_dataframe(self, df, DB_Name, Table_Name):
        data = pd.DataFrame(df.dtypes).T
        Columns = "("
        for col in data.columns:
            val = data.loc[0, col]
            if val == "datetime64[ns]":
                dType = "datetime"
            elif val == "int64":
                dType = "int(64)"
            elif val == "float64":
                dType = "float(64)"
            elif val == "object":
                dType = "varchar(255)"
            Columns = Columns + col + " " + dType + ", "
        Columns = Columns[0:-2] + ")"
        self.create_table_in_DB(DB_Name, Table_Name, Columns)

    def load_data_from_dataframe_to_table(self, df, DB_Name, Table_Name):
        self.create_table_as_dataframe(df, DB_Name, Table_Name)  # Creating table in DB

        # --------------------------------- Extracting column names as tuples
        columnNames = tuple(df.columns)

        # --------------------------------- Creating values type for insert values
        string = "("
        for i in range(len(tuple(df.columns))):
            string = string + "%s, "
        string = string[0:-2] + ")"


        # --------------------------------- Extracting values as tuples
        arrayValues = df.values
        records_to_insert = [tuple(arrayValues[i]) for i in range(len(arrayValues))]

        # --------------------------------- SQL Query
        SQL_Query = "INSERT INTO customers " + columnNames + " VALUES " + string
        # --------------------------------- Connecting to database
        MyDB, DB_Cursor = self.connect_to_database(DB_Name)
        # --------------------------------- Inserting Records into SQL table
        try:
            DB_Cursor.executemany(SQL_Query, records_to_insert)
            MyDB.commit()  # If no errors, permanently insert all the records into table
        except:
            MyDB.rollback()  # If any error exists, remove all inserted records from table
        MyDB.close()

