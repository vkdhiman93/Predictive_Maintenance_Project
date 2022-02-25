import pandas as pd
from application_logging.logging import LoggerApp
import warnings
import os

warnings.filterwarnings("ignore")


class Data_Getter:

    def __init__(self):
        # self.training_file='Training_FileFromDB/InputFile.csv' #Input File Link
        self.training_file = os.path.join("Training_FileFromDB", "InputFile.csv")
        # read test data from Training_FileFromDB
        self.test_file = os.path.join("Training_FileFromDB","test_FD001.txt")
        # self.predict_data = 'Prediction_Output_File/Predictions.csv' #Prediction file link
        self.predict_data = os.path.join("Prediction_Output_File", "Predictions.csv")
        # self.logfilepath="Training_Logs/GeneralLog.txt"
        self.logfilepath = os.path.join("Training_Logs", "GeneralLog.txt")
        self.logger_object = LoggerApp()

    def get_data(self):

        """
                Method Name: get_data
                Description: This function will read the training data file that have been captured from the database
                Output: data from Training_FileFromDB folder for training
                On Failure: Raise Exception


        """

        self.logfile = open(self.logfilepath, mode='a')
        self.logger_object.log(self.logfile, 'Entered the get_data method of the Data_Getter class')
        try:
            self.data = pd.read_csv(self.training_file)  # reading the training data file
            self.logger_object.log(self.logfile, 'Data Load Successful.Exited the get_data '
                                                 'method of the Data_Getter class')
            self.logfile.close()
            return self.data

        except Exception as e:
            self.logger_object.log(self.logfile, 'Exception occurred in get_data method of the Data_Getter class.'
                                                 ' Exception message: ' + str(e))
            self.logger_object.log(self.logfile, 'Data Load Unsuccessful.'
                                                 'Exited the get_data method of the Data_Getter class')
            self.logfile.close()
            raise Exception()

    def get_test_data(self):
        """
        Method Name: get_test_data
        Description : This function will read the test data file that have been captured from the database
        Output: test data from Training_FileFromDB folder

        """
        self.logfile = open(self.logfilepath, mode='a')
        self.logger_object.log(self.logfile, 'Entered the get_test_data method of the Data_Getter class')
        try:
            # define column names for easy indexing
            index_names = ['unit_nr', 'time_cycles']
            setting_names = ['setting_1', 'setting_2', 'setting_3']
            sensor_names = ['s_{}'.format(i) for i in range(1, 22)]
            col_names = index_names + setting_names + sensor_names
            # reading the test data file
            self.data = pd.read_csv(self.test_file, sep='\s+', header=None, names=col_names)

            self.logger_object.log(self.logfile, 'Data Load Successful.Exited the get_test_data '
                                                 'method of the Data_Getter class')
            self.logfile.close()
            return self.data

        except Exception as e:
            self.logger_object.log(self.logfile, 'Exception occurred in get_data method of the Data_Getter class.'
                                                 ' Exception message: ' + str(e))
            self.logger_object.log(self.logfile, 'Data Load Unsuccessful.'
                                                 'Exited the get_data method of the Data_Getter class')
            self.logfile.close()
            raise Exception()

    def prediction_data(self):
        """
                Method Name: prediction_data
                Description: This function will read the predict data created after preprocessing
                Output: data from Prediction_Output_File for prediction
                On Failure: Raise Exception


        """

        self.logfile = open(self.logfilepath, mode='a')
        self.logger_object.log(self.logfile, 'Entered the Prediction_data method of the Data_Getter class')
        try:
            self.data = pd.read_csv(self.predict_data)  # reading the data file
            self.logger_object.log(self.logfile, 'Data Load Successful.Exited the Prediction_data '
                                                 'method of the Data_Getter class')
            self.logfile.close()
            return self.data

        except Exception as e:
            self.logger_object.log(self.logfile,
                                   'Exception occurred in Prediction_data method of the Data_Getter class. '
                                   'Exception message: ' + str(e))
            self.logger_object.log(self.logfile, 'Data Load Unsuccessful.Exited the Prediction_data'
                                                 ' method of the Data_Getter class')
            self.logfile.close()
            raise Exception()