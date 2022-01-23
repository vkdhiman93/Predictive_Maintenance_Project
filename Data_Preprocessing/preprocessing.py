import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
# from imblearn.under_sampling import NearMiss
from application_logging.logging import LoggerApp
import warnings
# from sklearn import preprocessing
import os

warnings.filterwarnings("ignore")


class Preprocessor:

    def __init__(self):
        try:
            # self.logFilePath ="Training_Logs/Datapreprocessing_logs.txt"
            self.logFilePath = os.path.join("Training_Logs", "Datapreprocessing_logs.txt")
            self.logger_object = LoggerApp()
        except Exception as e:
            raise e

    def is_null_present(self, data):
        """
        Method: is_null_present
        Description : The function will check if there are any null values present inside the data or not

        """

        self.logfile = open(self.logFilePath, mode='a')
        self.logger_object.log(self.logfile, 'Entered the is_null_present method of the Preprocessor class')
        self.null_present = False
        self.cols_with_missing_values = []
        self.data = data
        self.cols = self.data.columns
        try:
            self.null_counts = self.data.isnull().sum()  # check for the count of null values per column
            for i in range(len(self.null_counts)):
                if self.null_counts[i] > 0:
                    self.null_present = True
                    self.cols_with_missing_values.append(self.cols[i])

            if (self.null_present):  # write the logs to see which columns have null values
                self.dataframe_with_null = pd.DataFrame()
                self.dataframe_with_null['columns'] = self.cols
                self.dataframe_with_null['missing values count'] = np.asarray(self.data.isnull().sum())
                self.dataframe_with_null.to_csv(os.path.join("Data_Information", "null_values.csv"))
                # storing the null column information to file
            self.logger_object.log(self.logfile,
                                   'Finding missing values is a success.Data written to the null values file. '
                                   'Exited the is_null_present method of the Preprocessor class')
            self.logfile.close()
            return self.null_present, self.cols_with_missing_values

        except Exception as e:
            self.logger_object.log(self.logfile,
                                   'Exception occurred in is_null_present method of the Preprocessor class. '
                                   'Exception message:  ' + str(e))
            self.logger_object.log(self.logfile,
                                   'Finding missing values failed. '
                                   'Exited the is_null_present method of the Preprocessor class')
            self.logfile.close()
            raise Exception()

    def separate_label_feature(self, data, label_column_name):
        """
        Method: separate_label_feature
        Description : This method will separate the input or independent features as X and output or target variable as Y


        """

        self.logfile = open(self.logFilePath, mode='a')
        self.logger_object.log(self.logfile, 'Entered the separate_label_feature method of the Preprocessor class')
        self.data = data
        self.column = label_column_name

        try:
            self.X = self.data.drop(
                columns=[self.column])  # drop the columns specified and separate the feature columns
            self.Y = self.data[self.column]  # Filter the Label columns
            self.logger_object.log(self.logfile,
                                   'Label Separation Successful. '
                                   'Exited the separate_label_feature method of the Preprocessor class')
            self.logfile.close()
            # print('Train Data')
            # print(self.X)
            # print('Label Data')
            # print(self.Y)
            return self.X, self.Y

        except Exception as e:
            self.logger_object.log(self.logfile,
                                   'Exception occurred in separate_label_feature method of the Preprocessor class. '
                                   'Exception message:  ' + str(e))
            self.logger_object.log(self.logfile,
                                   'Label Separation Unsuccessful. '
                                   'Exited the separate_label_feature method of the Preprocessor class')
            self.logfile.close()
            raise Exception()

    def scale_numerical_columns(self, data):
        """
        Method: scale_numerical_columns
        Description : This method will scale all the input features so that all the values should come under a specific range, this is done to equalize the distribution of the features which
        will make the data good for model building .

        """

        self.logfile = open(self.logFilePath, mode='a')
        self.logger_object.log(self.logfile, 'Entered the scale_numerical_columns method of the Preprocessor class')
        self.data = data

        try:
            # self.num_df = self.data.select_dtypes(include=['int64','float64']).copy()
            self.scaler = StandardScaler()  # initializing standard scaler
            self.scaler.fit(self.data)
            self.scaled = self.scaler.transform(self.data)

            self.scaled_data = pd.DataFrame(data=self.scaled, columns=self.data.columns)
            self.logger_object.log(self.logfile,
                                   'scaling for numerical values successful. '
                                   'Exited the scale_numerical_columns method of the Preprocessor class')
            self.logfile.close()
            # print('scaled data')
            # print(self.scaled_data)
            return self.scaled_data

        except Exception as e:
            self.logger_object.log(self.logfile,
                                   'Exception occurred in scale_numerical_columns method of the Preprocessor class. '
                                   'Exception message:  ' + str(e))
            self.logger_object.log(self.logfile,
                                   'scaling for numerical columns Failed. '
                                   'Exited the scale_numerical_columns method of the Preprocessor class')
            self.logfile.close()
            raise Exception()

    def remove_columns(self, data, columns):
        """
        Method: scale_numerical_columns Description : This method will remove the not so important features came out
        of our testing based on feature selection techniques .

        """

        self.logfile = open(self.logFilePath, mode='a')

        self.logger_object.log(self.logfile, 'Entered the remove_columns method of the Preprocessor class')
        self.data = data
        self.columns = columns

        try:
            self.useful_data = self.data.drop(columns=self.columns)
            # drop the labels specified in the columns
            self.logger_object.log(self.logfile,
                                   'Column removal Successful.'
                                   'Exited the remove_columns method of the Preprocessor class')
            self.logfile.close()
            # print('data after column removed')
            # print(self.useful_data)
            return self.useful_data

        except Exception as e:
            self.logger_object.log(self.logfile,
                                   'Exception occurred in remove_columns method of the Preprocessor class. '
                                   'Exception message:  ' + str(e))
            self.logger_object.log(self.logfile,
                                   'Column removal Unsuccessful. '
                                   'Exited the remove_columns method of the Preprocessor class')
            self.logfile.close()
            raise Exception()