# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ---------------------------------- IMPORTING LIBRARIES --------------------------------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# ------------------------------- System defined Packages -------------------------------
from flask import Flask, request, render_template
import os
import numpy as np
import pandas as pd

# -------------------------------- User defined Packages --------------------------------
from GlobalVariables.GlobalVariables import GlobalVariablesPath
from Data_Preprocessing.CleaningData import Cleaning
from Data_Preprocessing.EncodingFeatures import Encoding
from Data_Preprocessing.ScalingFeatures import Scaling
from Data_Preprocessing.BalancingData import Balancing
from Data_Models.Data_Models import Train_Pred_Submit_Model
from Data_Preprocessing.SelectingFeatures import FeatureSelection

app = Flask(__name__)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ................................................ HOMEPAGE ...............................................
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
@app.route("/", methods=['GET'])
def home():
    return render_template('home.html')

@app.route("/home_Backorder_Record", methods=['POST'])
def home_Backorder_Record():
    return render_template('home_Backorder_Record.html')

@app.route("/home_Backorder_File", methods=['POST'])
def home_Backorder_File():
    return render_template('home_Backorder_File.html')

@app.route("/home_Minbank_Record", methods=['POST'])
def home_Minbank_Record():
    return render_template('home_Minbank_Record.html')

@app.route("/home_Minbank_File", methods=['POST'])
def home_Minbank_File():
    return render_template('home_Minbank_File.html')
# ============================================================================================================


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ................................................ BACKORDER ...............................................
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# Backorder Record  ---------------------------------------------------------------------------------------
@app.route("/predict_Backorder_Record", methods=['POST'])
def predict_Backorder_Record():
    results = {}
    bo_features = ["national_inv", "lead_time", "in_transit_qty", "forecast_9_month", "sales_9_month", "perf_6_month_avg", "min_bank",
                   "pieces_past_due", "local_bo_qty", "deck_risk", "ppap_risk", "stop_auto_buy"]
    in_features = [[request.form[col] for col in bo_features]]
    X = pd.DataFrame(np.array(in_features), columns=bo_features)  # Creating Data Frame with input values
    data = Scaling().MinMaxScaling_backorder(X, "predicting")  # Features Scaling using MinMaxScaler
    Y_pred = Train_Pred_Submit_Model().backorderModelPrediction(data, "predicting")   # Predicting result

    if Y_pred[0] == 1:
        results["result"] = "Product falls under BACKORDER"
    else:
        results["result"] = "Product does not fall under BACKORDER"

    return render_template('results_Backorder_Record.html', data = X, results = results)
    # End : Validating Errors ====================================================

# Backorder File  ---------------------------------------------------------------------------------------
@app.route("/predict_Backorder_File", methods=['POST'])
def predict_Backorder_File():
    GVP = GlobalVariablesPath()

    results = {}
    file_path = request.form["file_path"]       # Get the file path given by user
    results["source_file_path"] = file_path
    file_name = os.path.basename(file_path).split(".")[0] + "_Submission.csv"  # Extracting Filename for submission

    data = pd.read_csv(file_path)       # Load Dataset
    Y_pred = backorderPrediction(data)  # Predicting result
    results["result"] = "Prediction is Successful"

    Train_Pred_Submit_Model().backorderModelSubmissions(Y_pred, file_name)  # Submitting the result into csv
    results["destination_file_path"] = GVP.filesPath["predictingFiles"] + file_name

    return render_template('results_Backorder_File.html', results=results)

# backorderTraining ----------------------------------------------------------------------------------------
@app.route("/backorderTraining", methods=['POST'])
def backorderTraining():
    GVP = GlobalVariablesPath()

    data = pd.read_csv(GVP.filesPath["trainingFile"])  # Loading Data
    data = Cleaning().cleanData(data)  # Data Cleaning
    data = FeatureSelection().selectedFeatures_for_backorder(data)  # Features Selection
    data = Encoding().convert_Cat_to_Num(data)  # Features Encoding
    data = Scaling().MinMaxScaling_backorder(data, "training")      # Features Scaling using MinMaxScaler
    data = Balancing().overSampling(data)  # Oversampling the data
    Train_Pred_Submit_Model().backorderModelTraining(data)  # Training the Model

    results = {}
    results["result"] = "Training is Successful"

    return render_template('results_Page.html', results=results)

# backorderPredicting ----------------------------------------------------------------------------------------
@app.route("/backorderPrediction", methods=['POST'])
def backorderPrediction(data):
    GVP = GlobalVariablesPath()

    data = Cleaning().cleanData(data)                                          # Data Cleaning
    data = FeatureSelection().selectedFeatures_for_backorder(data)  # Features Selection
    data = Encoding().convert_Cat_to_Num(data)                                # Features Encoding
    data = Scaling().MinMaxScaling_backorder(data, "predicting")                        # Features Scaling using MinMaxScaler
    Y_pred = Train_Pred_Submit_Model().backorderModelPrediction(data, "predicting")   # Predicting result
    return Y_pred


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ................................................ MINBANK .................................................
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# Minbank Record ---------------------------------------------------------------------------------------
@app.route("/predict_Minbank_Record", methods=['POST'])
def predict_Minbank_Record():
    results = {}
    mb_features = ["national_inv", "lead_time", "in_transit_qty", "forecast_6_month", 'sales_3_month', "perf_6_month_avg", 'pieces_past_due', 'local_bo_qty',
                   'deck_risk', 'ppap_risk', 'stop_auto_buy', 'oe_constraint', 'potential_issue', 'rev_stop']
    in_features = [[request.form[col] for col in mb_features]]
    X = pd.DataFrame(np.array(in_features), columns=mb_features)  # Creating Data Frame with input values

    data = Scaling().MinMaxScaling_minbank(X, "predicting")  # Features Scaling using MinMaxScaler
    Y_pred = Train_Pred_Submit_Model().minbankModelPrediction(data, "predicting")  # Predicting result

    results["result"] = "Minimum required storage for the given product in Minbank is  " + str(Y_pred[0])

    return render_template('results_Minbank_Record.html', data = X, results = results)

# Minbank File  ---------------------------------------------------------------------------------------
@app.route("/predict_Minbank_File", methods=['POST'])
def predict_Minbank_File():
    GVP = GlobalVariablesPath()

    results = {}
    file_path = request.form["file_path"]
    results["source_file_path"] = file_path     # Storing Source file path
    file_name = os.path.basename(file_path).split(".")[0] + "_Submission.csv"

    data = pd.read_csv(file_path)
    Y_pred = minbankPrediction(data) # Predicting result
    results["result"] = "Prediction is Successful"

    Train_Pred_Submit_Model().minbankModelSubmissions(Y_pred, file_name)  # Submitting the result into csv
    results["destination_file_path"] = GVP.filesPath["predictingFiles"] + file_name

    return render_template('results_Minbank_File.html', results=results)

# minbankTraining ----------------------------------------------------------------------------------------
@app.route("/minbankTraining", methods=['POST'])
def minbankTraining():
    GVP = GlobalVariablesPath()

    data = pd.read_csv(GVP.filesPath["trainingFile"])   # Loading Data
    data = Cleaning().cleanData(data)                     # Data Cleaning
    data = FeatureSelection().selectedFeatures_for_minbank(data)  # Features Selection
    data = Encoding().convert_Cat_to_Num(data)            # Features Encoding
    data = Scaling().MinMaxScaling_minbank(data, "training")      # Features Scaling using MinMaxScaler
    Train_Pred_Submit_Model().minbankModelTraining(data)         # Training the Model
    results = {}
    results["result"] = "Training is Successful"

    return render_template('results_Page.html', results=results)


# minbankPredicting ----------------------------------------------------------------------------------------
@app.route("/minbankPrediction", methods=['POST'])
def minbankPrediction(data):
    GVP = GlobalVariablesPath()

    data = Cleaning().cleanData(data)                                         # Data Cleaning
    data = FeatureSelection().selectedFeatures_for_minbank(data)              # Features Selection
    data = Encoding().convert_Cat_to_Num(data)                                # Features Encoding
    data = Scaling().MinMaxScaling_minbank(data, "predicting")                        # Features Scaling using MinMaxScaler
    Y_pred = Train_Pred_Submit_Model().minbankModelPrediction(data, "predicting")   # Predicting result

    return Y_pred

if __name__ == "__main__":
    app.run(debug=True, port=8765)





# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ----------------------------------------------------- NOT NEEDED -----------------------------------------------------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
@app.route("/home_Training", methods=['GET'])
def home_Training():
    results = {}
    errors = {}
    errors["trainingError"] = ""

    try:
        results = backorderTraining()
    except:
        errors["trainingError"] += "Error while training the Model\n"
        return render_template('results_ErrorsPage.html', errors=errors, results=results)
    return render_template('home_Training.html')

@app.route("/home_Predictions", methods=['GET'])
def home_Predictions():
    return render_template('home_Predictions.html')

# Template after home page to run 'backorder | minbank'  ---------------------------------------------------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
@app.route("/runTemplate", methods=['POST'])
def runTemplate():
    errors = {}
    errors["inputErrors"] = ""

    # Extracting the input values given by user --------------------------------------
    input_type = request.form['input_type']
    if input_type == "":
        errors["inputErrors"] += "Choose Prediction Type\n"
        return render_template('results_ErrorsPage.html', errors=errors)
    try:
        recordVal = request.form['record']
    except:
        recordVal = ""
    try:
        fileVal = request.form['file']
    except:
        fileVal = ""


    # Validating the input values given by user --------------------------------------
    if ((recordVal == "") & (fileVal == "")) | ((recordVal == "yes") & (fileVal == "yes")):
        errors["inputErrors"] += "Choose only either 'Record' or 'File'\n"
        return render_template('results_ErrorsPage.html', errors=errors)

    if recordVal == "yes":
        if input_type == "backorder":
            return render_template('home_Backorder_Record.html')
        elif input_type == "minbank":
            return render_template('home_Minbank_Record.html')
    elif fileVal == "yes":
        if input_type == "backorder":
            return render_template('home_Backorder_File.html')
        elif input_type == "minbank":
            return render_template('home_Minbank_File.html')