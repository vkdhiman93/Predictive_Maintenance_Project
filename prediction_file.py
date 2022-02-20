# this module will predict the o./p
from Data_Ingestion import data_loader
from Save_Model import save_methods
from application_logging.logging import LoggerApp
import pandas as pd
from Data_Preprocessing import preprocessing
from sklearn.preprocessing import StandardScaler
import warnings
import os

warnings.filterwarnings("ignore")


class prediction:
    def __init__(self):
        self.log_writer = LoggerApp()
        self.filepath = os.path.join("Prediction_Logs", "PredictionLog.txt")

    def convert_input_into_data(self):
        """
            Method : convert_input_into_data
            Aim : "This method connects modules [Preprocessing + Model_Finder + Save_Model]"
                    1. Preprocess the data
                        1.1 Perform null values imputing
                        1.2 Encoding of Categorical values
                        1.3 Scaling the input data
                        1.4 Removing the unnecessary columns

            Return : None
            On fault : raise the Exception .


        """
        self.file_object = open(self.filepath, 'a')
        self.log_writer.log(self.file_object, 'Enter In Convert_input_into_data')
        # self.input = user_input
        # print(self.input)
        try:
            # Getting the data from the source
            data_getter = data_loader.Data_Getter()
            data = data_getter.get_test_data()

            # data preprocessing
            preprocessor = preprocessing.Preprocessor()

            index_names = ['unit_nr', 'time_cycles']
            setting_names = ['setting_1', 'setting_2', 'setting_3']
            drop_sensors = ['s_1', 's_5', 's_6', 's_10', 's_16', 's_18', 's_19']
            drop_labels = index_names + setting_names + drop_sensors

            # Remove the columns not required in prediction

            # Since the true RUL values for the test set are only provided for the last time cycle of each engine,
            # the test set is subsetted to represent the same
            df = data.groupby('unit_nr').last().reset_index().drop(drop_labels, axis=1)

            df = preprocessor.scale_numerical_columns(df)

            self.file_object.close()
            return df

        except Exception as error:
            self.log_writer.log(self.file_object,
                                'Error occurred while running the convert_input_into_data!! Error:: %s' % error)
            self.file_object.close()
            raise error

    def get_prediction(self, data):
        """
            Method : convert_input_into_data
            Aim : "This method connects modules [Save_Model]"
                    1. load the ML model on the input data
                    2. Will get the output as prediction
                    3. csv file will be created with that prediction output

            Return : None
            On fault : raise the Exception .


        """
        # Logging the start of Prediction
        self.file_object = open(self.filepath, 'a')
        self.log_writer.log(self.file_object, 'Start of get_prediction')
        self.data = data
        try:
            model_loader = save_methods.Model_Operation()
            model_name = model_loader.find_correct_model_file()
            model = model_loader.load_model(model_name)
            result = list(model.predict(self.data))
            result = pd.DataFrame(result, index=range(1, 101), columns=['Predicted RUL']).rename_axis('Engine No.')
            path = os.path.join("Prediction_Output_File", "Predictions.csv")
            result.to_csv(path, header=True, mode='w+')
            self.log_writer.log(self.file_object, 'End of get_prediction')
            self.file_object.close()

        except Exception as error:
            self.log_writer.log(self.file_object, 'Error occurred while running the prediction!! Error:: %s' % error)
            self.file_object.close()
            raise error
