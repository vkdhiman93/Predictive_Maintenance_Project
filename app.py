# importing the necessary dependencies
from flask import Flask, render_template, request, redirect
from flask_cors import cross_origin
# from training_val_linkage import Main_trainingDataValidation
import pandas as pd
import training_file as train
import prediction_file as pred
from Data_Ingestion import data_loader
from application_logging.logging import LoggerApp
import os
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)  # initializing a flask app

@app.route('/')
def index():
    return render_template('public/index.html')

@app.route('/about')
def about():
    return """
    <h1 style='color: red'>About Page!!!</h1>
    <p>This is a Machine Learning Project on Predictive Maintenance to predict the RUL of the engines.</p>
    <p>RUL stands for Remaining Useful Life of the engine.</p>
    <p>The Machine Learning model is trained on the data provided by the manufacturer and the data is used to predict the RUL of the engines.</p>

    <code>Flask is <em>awesome</em></code>
    """

def training():
    """
    Method : training
    Description : 1. Perform training data validation
                  2. Perform model training
    """
    file_object = open(os.path.join("Training_Logs", "TrainingMainLog.txt"), 'a+')
    log_writer = LoggerApp()
    try:
        #train_val_obj = Main_trainingDataValidation()
        #train_val_obj.train_validation()
        log_writer.log(file_object, 'Data Validation Completed Successfully')
        train_obj = train.training()
        train_obj.trainingModel()
        log_writer.log(file_object, 'Model Training Completed Successfully')
        file_object.close()
    except Exception as e:
        log_writer.log(file_object, 'This is a problem with Model Training' + str(e))
        file_object.close()
        raise Exception(str(e))
    return "Training Completed"


# training()

@app.route('/upload_txt', methods=['GET', 'POST' ])  # route to show the predictions in a web UI
@cross_origin()
def upload_txt():
    if request.method == 'POST':
        if request.files:
            txt_file = request.files["txt"]
            abs_path = os.path.abspath("Training_FileFromDB")
            txt_file.save(os.path.join(abs_path, txt_file.filename))

            print(f"{txt_file.filename} uploaded for prediction")
            return redirect(request.url)
    return render_template("public/upload_csv.html")

@app.route('/predict')
@cross_origin()
def predict():

    """
    Method : predict Description: With this method user will be able to take values from the user and able to predict
    the output based upon it
    """
    

    file_object = open("Prediction_Logs/PredictionLog.txt", 'a+')
    log_writer = LoggerApp()
    log_writer.log(file_object, 'Start For Gathering Data for prediction')

    try:

        p = pred.prediction()  # Predict A File
        data = p.convert_input_into_data()
        
        p.get_prediction(data)
        # log_writer.log(file_object, 'Start For Prediction')
        result = pd.read_csv(os.path.join("Prediction_Output_File", "Predictions.csv"))
        log_writer.log(file_object, "Prediction process Completed...")
        file_object.close()

    except Exception as e:
        log_writer.log(file_object, 'This is a problem with Prediction Process' + str(e))
        file_object.close()
        raise Exception(str(e))

    return render_template("public/predict.html", tables=[result.to_html(classes='data')], titles=result.columns.values)


if __name__ == "__main__":
    app.run(debug=True)

