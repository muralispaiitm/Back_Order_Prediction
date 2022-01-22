# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ---------------------------------- IMPORTING LIBRARIES --------------------------------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# 1 PREPROCESSING DATA
# 1.1 CleaningData
# 1.2 Imputing Missing data
# 1.2.1 NullRows
# 1.2.2 NullColumns
# 1.2.3 SyntaxErrors
# 1.3 Converting Features
# 1.4 Feature Selection
# 1.5 Feature Scaling
# 1.6 Balance Data
# 2 Training Model
# 3 Prediction
# 4 Visualization


# ------------------------------- System defined Packages -------------------------------
from flask import Flask, request,render_template
import os
import json
from datetime import datetime
import joblib
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import KNNImputer


# -------------------------------- User defined Packages --------------------------------

app = Flask(__name__)

# Home Page ------------------------------------------------------------------------------------------------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
@app.route("/", methods=['GET'])
def home():
    pass
    return render_template('index.html')

# Training the Raw Batch Files -----------------------------------------------------------------------------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
@app.route("/train", methods=['GET'])
def trainRouteClient():
    BOP_train = pd.read_csv("/dataset/Training_BOP.csv")


    # 1 PREPROCESSING DATA
    categorical_features = ['potential_issue', 'deck_risk', 'oe_constraint', 'ppap_risk', 'stop_auto_buy', 'rev_stop',
                            'went_on_backorder']
    numerical_features = ['national_inv', 'lead_time', 'in_transit_qty', 'forecast_3_month', 'forecast_6_month',
                          'forecast_9_month', 'sales_1_month', 'sales_3_month', 'sales_6_month', 'sales_9_month',
                          'min_bank', 'pieces_past_due', 'perf_6_month_avg', 'perf_12_month_avg', 'local_bo_qty']

    # 1.1 CleaningData
    # ------------------------------------------------------------------
    BOP_train.drop(['sku'], axis=1, inplace=True)
    # 1.2 Imputing Missing data
    # 1.2.1 NullRows
    # ------------------------------------------------------------------
    nullIndices = BOP_train.index[(BOP_train.isnull().sum(axis=1)) / len(BOP_train.columns) > 0.8]
    BOP_train.drop(nullIndices, inplace=True)

    # 1.2.2 NullColumns
    # ------------------------------------------------------------------
    lead_time_mean = np.round(BOP_train["lead_time"].mean())
    lead_time_null_index = BOP_train[BOP_train["lead_time"].isnull()].index
    BOP_train.loc[lead_time_null_index, "lead_time"] = lead_time_mean

    # 1.2.3 SyntaxErrors
    # ------------------------------------------------------------------
    # Imputing NULL values of 'national_inv'
    national_inv_mean = np.round(BOP_train[BOP_train["national_inv"] != -99]["national_inv"].mean())
    national_inv_99_index = BOP_train[BOP_train["national_inv"] == -99].index
    BOP_train.loc[national_inv_99_index, "national_inv"] = national_inv_mean

    # Imputing NULL values of 'perf_6_month_avg'
    perf_6_month_avg_mean = np.round(BOP_train[BOP_train["perf_6_month_avg"] > 0]["perf_6_month_avg"].mean())
    perf_6_month_avg_99_index = BOP_train[BOP_train["perf_6_month_avg"] < 0]["perf_6_month_avg"].index
    BOP_train.loc[perf_6_month_avg_99_index, "perf_6_month_avg"] = perf_6_month_avg_mean

    # Imputing NULL values of 'perf_12_month_avg'
    perf_12_month_avg_mean = np.round(BOP_train[BOP_train["perf_12_month_avg"] > 0]["perf_12_month_avg"].mean())
    perf_12_month_avg_99_index = BOP_train[BOP_train["perf_12_month_avg"] < 0]["perf_12_month_avg"].index
    BOP_train.loc[perf_12_month_avg_99_index, "perf_12_month_avg"] = perf_12_month_avg_mean

    # 1.3 Converting Features
    # ------------------------------------------------------------------
    # Converting Categorical to Numerical
    for feature in categorical_features:
        BOP_train[feature] = BOP_train[feature].map({'No': 0, 'Yes': 1})

    # 1.4 Feature Selection
    selectedFeatuers = ['stop_auto_buy', 'lead_time', 'deck_risk', 'perf_6_month_avg', 'ppap_risk', 'national_inv',
                        'forecast_9_month', 'sales_9_month', 'local_bo_qty', 'pieces_past_due', 'min_bank',
                        'in_transit_qty']
    targetFeature = "went_on_backorder"
    BOP_train = BOP_train[selectedFeatuers + [targetFeature]]

    # 1.5 Feature Scaling
    # ------------------------------------------------------------------
    X = BOP_train.drop("went_on_backorder", axis=1)
    Y = BOP_train["went_on_backorder"]

    from sklearn.preprocessing import MinMaxScaler
    MMS = MinMaxScaler()
    MMS.fit(X)
    X_array = MMS.transform(X)
    X_scale = pd.DataFrame(X_array, columns=X.columns)
    X_scale.head()

    BOP_train = pd.concat([X_scale, Y], axis=1)

    # 1.6 Balance Data
    # ------------------------------------------------------------------

    # 2 Training Model
    # ------------------------------------------------------------------

    # 3 Prediction
    # ------------------------------------------------------------------

    # 4 Visualization
    # ------------------------------------------------------------------


    pass

# Predicting the Raw Batch Files -----------------------------------------------------------------------------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
@app.route("/predict", methods=['GET'])
def predictRouteClient():

    # 1 PREPROCESSING DATA
    # 1.1 CleaningData
    # 1.2 Imputing Missing data
    # 1.2.1 NullRows
    # 1.2.2 NullColumns
    # 1.2.3 SyntaxErrors
    # 1.3 Converting Features
    # 1.4 Feature Selection
    # 1.5 Feature Scaling
    # 3 Prediction
    # 4 Visualization

    pass

if __name__ == "__main__":
    app.run(debug=True, port=8765)