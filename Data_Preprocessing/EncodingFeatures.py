
# ------------------------------- System defined Packages -------------------------------


# ------------------------------- User defined Packages -------------------------------
from GlobalVariables.GlobalVariables import GlobalVariablesPath

class Encoding:
    def __init__(self):
        self.GVP = GlobalVariablesPath()

    def convert_Cat_to_Num(self, data):
        # Converting Categorical to Numerical
        categoricalFeatures = self.GVP.CategoricalFeatures.copy()

        for feature in self.GVP.CategoricalFeatures:
            if feature not in data.columns:
                categoricalFeatures.remove(feature)

        for feature in categoricalFeatures:
            data[feature] = data[feature].map({'No': 0, 'Yes': 1})
        return data