
# ------------------------------- System defined Packages -------------------------------
import pandas as pd
import numpy as np

from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

import joblib

# ------------------------------- User defined Packages -------------------------------
from GlobalVariables.GlobalVariables import GlobalVariablesPath

class Train_Pred_Submit_Model:
    def __init__(self):
        self.GVP = GlobalVariablesPath()

    def backorderModelReport(self, Y, Y_pred_prob, Y_pred, validate):
        # Classification Reports using Confusion Matrix ----------------------------------------------------------------
        roc_auc = roc_auc_score(Y, Y_pred_prob[:, 1])

        cm = confusion_matrix(Y, Y_pred)
        TP = cm[0, 0]
        TN = cm[1, 1]
        FP = cm[0, 1]
        FN = cm[1, 0]
        accuracy = (TP + TN) / float(TP + TN + FP + FN)
        error = (FP + FN) / float(TP + TN + FP + FN)
        precision = TP / float(TP + FP)
        recall = TP / float(TP + FN)
        specificity = TN / (TN + FP)
        TPR = TP / float(TP + FN)
        FPR = FP / float(FP + TN)

        # Loading 'XGBC_Model_Report.csv' file -------------------------------------------------------------------------
        XGBC_Model_Report = pd.read_csv(self.GVP.filesPath["dataSet"] + "XGBC_Model_Report.csv")

        # Storing classification reports in a csv file -----------------------------------------------------------------
        XGBC_Model_Report.loc[validate, :] = [validate, roc_auc, TP, TN, FP, FN, accuracy, error, precision, recall,
                                              specificity, TPR, FPR]
        XGBC_Model_Report.to_csv(self.GVP.filesPath["dataSet"] + "XGBC_Model_Report.csv", index=False)

    def backorderModelPrediction(self, data, validate):
        if "went_on_backorder" in data.columns:
            X = data.drop("went_on_backorder", axis=1)
            Y = data["went_on_backorder"]
        else:
            X = data.copy()

        # Predictions --------------------------------------------------------------------------------------------------
        model = joblib.load(self.GVP.filesPath["PickleFiles"] + "XGBClassifier.pkl")
        Y_pred_prob = model.predict_proba(X)
        Y_pred = model.predict(X)

        # Model Report Summary -----------------------------------------------------------------------------------------
        if "went_on_backorder" in data.columns:
            self.backorderModelReport(Y, Y_pred_prob, Y_pred, validate)

        return Y_pred

    def backorderModelTraining(self, data):
        X = data.drop('went_on_backorder', axis=1)
        Y = data['went_on_backorder']

        model = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
                              colsample_bynode=1, colsample_bytree=0.7, gamma=0.0,
                              importance_type='gain', interaction_constraints='',
                              learning_rate=0.1, max_delta_step=0, max_depth=10,
                              min_child_weight=3,
                              n_estimators=100, n_jobs=0, num_parallel_tree=1,
                              objective='binary:logistic', random_state=50, reg_alpha=1.2,
                              reg_lambda=1.6, scale_pos_weight=1.0, subsample=0.9,
                              tree_method='exact', validate_parameters=1, verbosity=0)

        # Training Model ===========================================================
        model.fit(X, Y)

        # Storing Model as a pickle ================================================
        joblib.dump(model, self.GVP.filesPath["PickleFiles" ] + "XGBClassifier.pkl")

        # Creating a Data Frame to store Classification reports ====================
        XGBC_Model_Report = pd.DataFrame(columns=["data", "roc_auc", "TP", "TN", "FP", "FN", "accuracy", "error", "precision", "recall", "specificity", "TPR", "FPR"])
        XGBC_Model_Report.to_csv(self.GVP.filesPath["dataSet" ] +"XGBC_Model_Report.csv", index=False)

        # Getting predictions and storing in a DataFrame ===========================
        Y_pred_prob = model.predict_proba(X)
        Y_pred = model.predict(X)
        self.backorderModelReport(Y, Y_pred_prob, Y_pred, "training")

    def backorderModelSubmissions(self, Y_pred, file_name):
        submission = pd.read_csv(self.GVP.filesPath["Temp"] + "submission.csv")
        submission["BO_Prediction"] = Y_pred
        submission.to_csv(self.GVP.filesPath["predictingFiles"] + file_name, index=False)

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Min Bank ========================================================================================================================
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def minbankModelReport(self, Y, Y_pred, validate):

        # Regression report
        R2_score = r2_score(Y, Y_pred)
        MAE = mean_absolute_error(Y, Y_pred)
        MSE = mean_squared_error(Y, Y_pred)
        RMSE = np.sqrt(MSE)

        # Loading 'LinearRegression_Model_Report.csv' file -------------------------------------------------------------------------
        LinearRegression_Model_Report = pd.read_csv(self.GVP.filesPath["dataSet"] + "LinearRegression_Model_Report.csv")

        # Storing Regression reports in a csv file -----------------------------------------------------------------
        LinearRegression_Model_Report.loc[validate, :] = [validate, R2_score, MAE, MSE, RMSE]
        LinearRegression_Model_Report.to_csv(self.GVP.filesPath["dataSet"] + "LinearRegression_Model_Report.csv", index=False)

    def minbankModelPrediction(self, data, validate):
        if "min_bank" in data.columns:
            X = data.drop('min_bank', axis=1)
            Y = data['min_bank']
        else:
            X = data.copy()

        # Predictions ==============================================================
        model = joblib.load(self.GVP.filesPath["PickleFiles"] + "LinearRegression_Model.pkl")
        Y_pred = model.predict(X)

        # Model Report Summary -----------------------------------------------------------------------------------------
        if "min_bank" in data.columns:
            self.minbankModelReport(Y, Y_pred, validate)

        return np.round(Y_pred)

    def minbankModelTraining(self, data):
        X = data.drop('min_bank', axis=1)
        Y = data['min_bank']

        model = LinearRegression()
        # Training Model ===========================================================
        model.fit(X, Y)

        # Storing Model as a pickle ================================================
        joblib.dump(model, self.GVP.filesPath["PickleFiles"] + "LinearRegression_Model.pkl")

        # Creating a Data Frame to store Classification reports ====================
        LinearRegression_Model_Report = pd.DataFrame(columns=["data", "R2_score", "MAE", "MSE", "RMSE"])
        LinearRegression_Model_Report.to_csv(self.GVP.filesPath["dataSet"] + "LinearRegression_Model_Report.csv", index=False)

        # Predicting result
        Y_pred = model.predict(X)
        self.minbankModelReport(Y, Y_pred, "training")

    def minbankModelSubmissions(self, Y_pred, file_name):
        submission = pd.read_csv(self.GVP.filesPath["Temp"] + "submission.csv")
        submission["MB_Prediction"] = Y_pred
        submission.to_csv(self.GVP.filesPath["predictingFiles"] + file_name, index=False)

