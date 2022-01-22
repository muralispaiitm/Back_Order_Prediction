
# ------------------------------- System defined Packages -------------------------------
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import NearMiss
import pandas as pd

# ------------------------------- User defined Packages -------------------------------

class Balancing:
    def __init__(self):
        pass

    def overSampling(self, data):
        X = data.drop("went_on_backorder", axis=1)
        Y = data["went_on_backorder"]

        X_overSample, Y_overSample = SMOTE(random_state=12).fit_resample(X, Y)
        data = pd.concat([X_overSample, Y_overSample], axis=1)
        return data
