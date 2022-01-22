
# ------------------------------- System defined Packages -------------------------------
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import joblib

# ------------------------------- User defined Packages -------------------------------
from GlobalVariables.GlobalVariables import GlobalVariablesPath

class Scaling:
    def __init__(self):
        self.GVP = GlobalVariablesPath()

    # Method 1 ------------------------------------------------------------------------------------------
    def MinMaxScaling_backorder(self, data, validate):
        if "went_on_backorder" in data.columns:
            X = data.drop("went_on_backorder", axis=1)
            Y = data["went_on_backorder"]
        else:
            X = data.copy()

        if validate == "training":
            MMS = MinMaxScaler()
            MMS.fit(X)
            joblib.dump(MMS, self.GVP.filesPath["PickleFiles"] + "MinMaxScaling_backorder.pkl")
        else:
            MMS = joblib.load(self.GVP.filesPath["PickleFiles"] + "MinMaxScaling_backorder.pkl")

        X_array = MMS.transform(X)
        X_scale = pd.DataFrame(X_array, columns=X.columns)

        if "went_on_backorder" in data.columns:
            data = pd.concat([X_scale, Y], axis=1)
        else:
            data = X_scale

        return data

    def MinMaxScaling_minbank(self, data, validate):
        if "min_bank" in data.columns:
            X = data.drop("min_bank", axis=1)
            Y = data["min_bank"]
        else:
            X = data.copy()

        if validate == "training":
            MMS = MinMaxScaler()
            MMS.fit(X)
            joblib.dump(MMS, self.GVP.filesPath["PickleFiles"] + "MinMaxScaling_minbank.pkl")
        else:
            MMS = joblib.load(self.GVP.filesPath["PickleFiles"] + "MinMaxScaling_minbank.pkl")

        X_array = MMS.transform(X)
        X_scale = pd.DataFrame(X_array, columns=X.columns)
        if "min_bank" in data.columns:
            data = pd.concat([X_scale, Y], axis=1)
        else:
            data = X_scale

        return data
