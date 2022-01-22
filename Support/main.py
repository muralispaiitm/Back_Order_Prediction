
# importing the necessary dependencies
import numpy as np 
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle

app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            national_inventory=float(request.form['national_inventory'])
            lead_time = float(request.form['lead_time'])
            in_transit_qty = float(request.form['in_transit_qty'])
            month_3_forcasted_value = float(request.form['month_3_forcasted_value'])
            prior_1_month_sales= float(request.form['prior_1_month_sales'])
            prior_9_month_sales = float(request.form['prior_9_month_sales'])

            filename = 'finalized_model.pickle'
            loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
            # predictions using the loaded model file
            prediction=loaded_model.predict(np.array([[national_inventory,lead_time,in_transit_qty,month_3_forcasted_value,prior_1_month_sales,prior_9_month_sales]]))
            def change (prediction):     #custom function to change the formate of result in Yes and No format
                if prediction == 1:
                    return 'Yes'
                else:
                    return 'No'
            # showing the prediction results in a UI
            return render_template('results.html',prediction=change(prediction))
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')



if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True) # running the app