
# ------------------------------- System defined Packages -------------------------------
# Import required libraries
from pymongo import MongoClient
import json
import pandas as pd
import os
import shutil
import glob
from datetime import datetime
import mysql.connector as Sql

# ------------------------------- User defined Packages -------------------------------
from GlobalVariables.GlobalVariables import GlobalVariablesPath


# Connection Name : BackorderDB
# HostName : 127.0.0.1
# User : root
# PWD : password

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ============================================= MONGO DB ==============================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class MongoDB:
    def __init__(self):
        # Importing MongoDB Variables paths
        self.GVP = GlobalVariablesPath()
        self.mdbVar = self.GVP.MdbVariables

        self.userId = self.mdbVar["userId"]
        self.pwd = self.mdbVar["pwd"]
        self.cluster = self.mdbVar["cluster"]
        self.DbURL = f"mongodb+srv://{self.userId}:{self.pwd}@{self.cluster}.heyil.mongodb.net/<dbname>?retryWrites=true&w=majority"

    # ======================= MongoDB Variables =======================
    # Need to modify

    # ======================= Data Base CONNECTING and CLOSING =======================
    def MDB_Connection_Open(self):
        client = MongoClient(self.DbURL)

        mydb = Sql.connect(host='localhost', user='root', password='admin', database='db1')
        cur = mydb.cursor()

        return client

    def MDB_Connection_Close(self, client):
        client.close()

    # ======================= Data Base =======================
    def List_Of_DB_Names(self, client):
        DB_Names = client.list_database_names()
        return DB_Names

    def Check_DB_Exists(self, client, DB_Name):
        if DB_Name in client.list_database_names():
            return True
        else:
            return False

    def Get_DataBase(self, client, DB_Name):
        if self.Check_DB_Exists(client, DB_Name):
            db = client[DB_Name]
            return db
        else:
            return False

    def Create_DataBase(self, client, DB_Name):
        if self.Check_DB_Exists(client, DB_Name):
            db = self.Get_DataBase(client, DB_Name)
            return db
        else:
            db = client[DB_Name]
            return db

    def Drop_DataBase(self, client, DB_Name):
        List_of_Collections = self.List_Of_Collections_From_DB(client, DB_Name)
        for collection in List_of_Collections:
            coll = self.Get_Collection(client, DB_Name, collection)
            coll.drop()

    # ======================= Collections =======================
    def List_Of_Collections_From_DB(self, client, DB_Name):
        if self.Check_DB_Exists(client, DB_Name):
            db = client[DB_Name]
            collectionNames = db.list_collection_names()
            return collectionNames
        else:
            return False

    def Check_Collection_Exists(self, client, DB_Name, CollectionName):
        db = self.Get_DataBase(client, DB_Name)
        if type(db) != type(False):
            if CollectionName in db.list_collection_names():
                return True
            else:
                return False
        else:
            return False

    def Insert_Collection(self, client, Local_JsonFilePath, DB_Name, Collection_Name):
        json_file = open(Local_JsonFilePath)
        FileCollection = json.load(json_file)

        if self.Check_Collection_Exists(client, DB_Name, Collection_Name):
            collection = self.Get_Collection(client, DB_Name, Collection_Name)
            collection.insert_one(FileCollection)

    def Drop_Collection(self, client, DB_Name, Collection_Name):
        collection = self.Get_Collection(client, DB_Name, Collection_Name)
        collection.drop()

    # ======================= Extract Records =======================
    def Get_Collection(self, client, DB_Name, Collection_Name):
        if (self.Check_DB_Exists(client, DB_Name)) & (self.Check_Collection_Exists(client, DB_Name, Collection_Name)):
            db = client[DB_Name]
            collection = db[Collection_Name]
            return collection
        else:
            return False

    def Get_Records_From_Collection_As_List(self, client, DB_Name, Collection_Name):
        collection = self.Get_Collection(client, DB_Name, Collection_Name)
        if type(collection) != type(False):
            Collection_In_List = list(collection.find())
            return Collection_In_List
        else:
            return False

    def Get_Records_From_Collection_As_DataFrame(self, client, DB_Name, Collection_Name):
        Collection_In_List = self.Get_Records_From_Collection_As_List(client, DB_Name, Collection_Name)
        if type(Collection_In_List) != type(False):
            Df = pd.DataFrame(Collection_In_List)
            return Df
        else:
            return False

    def Check_Record_Exists(self, client, DB_Name, Collection_Name, Record):
        collection = self.Get_Collection(client, DB_Name, Collection_Name)
        N_Records = collection.find(Record)
        if N_Records.count() > 0:
            return True
        else:
            return False

    # ======================= Insert Records =======================
    def Insert_Record(self, client, DB_Name, CollectionName, Record):
        collection = self.Get_Collection(client, DB_Name, CollectionName)
        collection.insert_one(Record)

    def Insert_Records_From_Df_Into_Collection(self, client, DB_Name, CollectionName, Df):
        if "_id" in Df.columns.to_list():
            Df = Df.drop(columns=["_id"], axis=1)
        records = json.loads(Df.T.to_json()).values()

        collection = self.Get_Collection(client, DB_Name, CollectionName)

        N_Inserted_Records = 0
        N_Uninserted_Records = 0
        for record in records:
            if self.Check_Record_Exists(client, DB_Name, CollectionName, record):
                N_Uninserted_Records += 1
            else:
                collection.insert_one(record)
                N_Inserted_Records += 1
        return {"Inserted_Records": N_Inserted_Records, "Uninserted_Records": N_Uninserted_Records}