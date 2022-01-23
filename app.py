# importing the necessary dependencies
from flask import Flask, render_template, request
from flask_cors import cross_origin
# from training_val_linkage import Main_trainingDataValidation
import training_file as train
import prediction_file as pred
from Data_Ingestion import data_loader
from application_logging.logging import LoggerApp
import os
import warnings

warnings.filterwarnings("ignore")


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
        # print(data)
        p.get_prediction(data)
        # log_writer.log(file_object, 'Start For Prediction')






        log_writer.log(file_object, "Prediction process Completed...")
        file_object.close()

    except Exception as e:
        log_writer.log(file_object, 'This is a problem with Prediction Process' + str(e))
        file_object.close()
        raise Exception(str(e))
    msg = print("Prediction Completed")
    return msg

predict()

