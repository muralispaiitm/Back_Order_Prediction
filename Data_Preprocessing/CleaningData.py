
# ------------------------------- System defined Packages -------------------------------
import pandas as pd
import numpy as np

# ------------------------------- User defined Packages -------------------------------
from GlobalVariables.GlobalVariables import GlobalVariablesPath

class Cleaning:
    def __init__(self):
        self.GVP = GlobalVariablesPath()

    def cleanData(self, data):
        # Run removeRowsCols(),imputeMissingData()
        data = self.removeRowsCols(data)
        data = self.imputeSyntaxErrors(data)
        data = self.imputeMissingData(data)
        return data

    def removeRowsCols(self, data):
        # 1.1.1 Removing unnecessary Rows and Columns (NullRows, NUllColumns)

        # DROP ROWS
        nullIndices = data.index[(data.isnull().sum(axis=1)) / len(data.columns) > 0.7]
        data.drop(nullIndices, inplace=True)  # Droping the rows which have percentage of null values more than 70%.

        # DROP COLUMNS
        nullColumns = data.columns[data.isnull().sum() / len(data) > 0.7]
        data.drop(nullColumns, axis=1, inplace=True)   # Droping the columns which have percentage of null values more than 70%.

        # Drop 'sku' columns
        if 'sku' in data.columns:
            # Storing Unique Id in Temporary folder
            data[["sku"]].to_csv(self.GVP.filesPath["Temp"] + "submission.csv", index=False)
            data.drop('sku', axis=1, inplace=True)

        return data

    def imputeSyntaxErrors(self, data):
        # Imputing Syntax Errors
        syntaxVal = self.GVP.syntaxErrorVal  # Accessing syntax error value form the GlobalVariables class
        syntaxErrorColumns = data.columns[data.isin([syntaxVal]).sum() > 0]
        for col in syntaxErrorColumns:
            syntaxIndex = data[data[col] == syntaxVal].index
            data.loc[syntaxIndex, col] = np.nan
        return data

    def imputeMissingData(self, data):
        # Imputing Null values
        nullColumns = data.columns[data.isnull().sum() > 0]
        for col in nullColumns:
            meanVal = np.round(data[col].mean())
            nullIndex = data[data[col].isnull()].index
            data.loc[nullIndex, col] = meanVal
        return data