# ------------------------------- User defined Packages -------------------------------
from GlobalVariables.GlobalVariables import GlobalVariablesPath


class FeatureSelection:
    def __init__(self):
        self.GVP = GlobalVariablesPath()

    def selectedFeatures_for_backorder(self, data):
        SelectedFeatures_for_backorder = self.GVP.SelectedFeatures_for_backorder.copy()

        if "went_on_backorder" not in data.columns:
            SelectedFeatures_for_backorder.remove("went_on_backorder")

        data = data[SelectedFeatures_for_backorder]
        return data

    def selectedFeatures_for_minbank(self, data):
        SelectedFeatures_for_minbank = self.GVP.SelectedFeatures_for_minbank.copy()

        if "min_bank" not in data.columns:
            SelectedFeatures_for_minbank.remove("min_bank")

        data = data[SelectedFeatures_for_minbank]
        return data
