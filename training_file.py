from scipy.stats.stats import mode
import pandas as pd
from Data_Ingestion import data_loader
from Data_Preprocessing import preprocessing
from Model_Finder import model
from Save_Model import save_methods
import add_rul as add_rul
from sklearn.model_selection import train_test_split
from application_logging.logging import LoggerApp
import warnings

warnings.filterwarnings("ignore")

"""
This is the for Training the Machine Learning Model.
"""


class training:
    """
    Method : training
    Function Performed  : trainingModel()

    """

    def __init__(self):
        self.logger = LoggerApp()

    def trainingModel(self):
        """
            Method : trainingModel
            Aim : "This method connects modules [Preprocessing + Model_Finder + Save_Model]"
                    1. Preprocess the data
                        1.1 Perform null values imputing
                        1.2 Encoding of Categorical values
                        1.3 Splitting of Input and target variables
                        1.4 Scaling the input data
                        1.5 Removing the unnecessary columns
                        1.6 Train test split of the data
                    2. Will get best model from Model_Finder Function
                    3. Model will be saved in a folder for further use.
            Return : None
            On fault : raise the Exception .


        """
        self.file = open('Training_Logs/ModelTrainingLog.txt', mode='a')
        self.logger.log(self.file, "Training Operation Started....")
        try:
            # Getting the data from the source
            data_getter = data_loader.Data_Getter()
            data = data_getter.get_data()

            # add RUL
            data = add_rul.add_remaining_useful_life(data)

            # data preprocessing
            preprocessor = preprocessing.Preprocessor()

            # check if missing values are present in the dataset
            is_null_present, cols_with_missing_values = preprocessor.is_null_present(data)

            # if missing values are there, replace them appropriately.

            # Convert categorical values to numeric values

            # create separate features and labels
            X, Y = preprocessor.separate_label_feature(data, label_column_name='RUL')



            # remove the following columns as they don't contribute to prediction.

            index_names = ['unit_nr', 'time_cycles']
            setting_names = ['setting_1', 'setting_2', 'setting_3']
            drop_sensors = ['s_1', 's_5', 's_6', 's_10', 's_16', 's_18', 's_19']
            drop_labels = index_names + setting_names + drop_sensors
            X = preprocessor.remove_columns(X,drop_labels)

            # scaling the X values
            X = preprocessor.scale_numerical_columns(X)

            # parsing all the clusters and looking for the best ML algorithm to fit on individual cluster
            x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.20, random_state=100)

            # object initialization
            model_finder = model.ModelFinder()

            # Getting the best model for each of the clusters
            best_model_name, best_model = model_finder.get_best_model(x_train, x_test, y_train, y_test)

            # saving the best model to the directory.
            model_op = save_methods.Model_Operation()
            save_model = model_op.save_model(best_model, best_model_name)
            self.logger.log(self.file, "Training Operation Completed SuccessFully....")
            self.file.close()

        except Exception as e:
            # logging the unsuccessful Training
            self.logger.log(self.file,
                            'class : training , filelocation : trainingfile.py : Unsuccessful End of Training' + str(e))
            self.file.close()
            raise Exception()
