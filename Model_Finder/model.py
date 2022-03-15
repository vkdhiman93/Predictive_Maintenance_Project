from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge, Lasso, RidgeCV, LassoCV
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from application_logging.logging import LoggerApp
import numpy as np
import warnings
from sklearn import *
import os

warnings.filterwarnings("ignore")


class ModelFinder:
    def __init__(self):
        try:
            self.logger_object = LoggerApp()
            # self.logFilepath = "Training_Logs/ModelTrainingLog.txt"
            self.logFilepath = os.path.join("Training_Logs", "ModelTrainingLog.txt")
            self.logfile = open(self.logFilepath, mode="a")
            self.lasso = Lasso()
            self.svr = SVR(kernel="linear")
            self.logger_object.log(
                self.logfile, "Instances have been created for all the models"
            )
            self.logfile.close()

        except Exception as e:
            self.logger_object.log(self.logfile, log_massage="Exception : " + str(e))
            self.logfile.close()
            raise e

    def get_best_params_for_lasso_regression(self, x_train, y_train):
        """
                Method Name: get_best_params_for_lasso_regression
                Description: This method will load the Lasso Regression model and will tune the in-build parameter to
                get best possible accuracy.
                Output: None
                On Failure: Raise Exception


        """
        self.logfile = open(self.logFilepath, mode="a")
        self.logger_object.log(
            self.logfile,
            "Entered the get_best_params_for_lasso_regression method of the "
            "Model_Finder class",
        )

        try:

            # Creating an object of the lasso Regularization
            self.lassocv = LassoCV(alphas=None, cv=50, max_iter=200000, normalize=True)

            # finding the best parameter
            self.lassocv.fit(x_train, y_train)

            # Creating a new model with required parameter
            self.lasso = Lasso(alpha=self.lassocv.alpha_)

            # Training the new model
            self.lasso.fit(x_train, y_train)
            self.logger_object.log(
                self.logfile,
                "Lasso Regression best params: "
                + str(self.lassocv.alpha_)
                + ". Exited the get_best_params_for_linear_regression method of the Model_Finder "
                "class",
            )
            self.logfile.close()
            return self.lasso

        except Exception as e:
            self.logger_object.log(
                self.logfile,
                "Exception occurred in get_best_params_for_lasso_regression method "
                "of the Model_Finder class.",
            )
            self.logger_object.log(
                self.logfile,
                "Lasso Repressor Parameter tuning  failed.Exited the "
                "get_best_params_for_random_forest method of the Model_Finder class",
            )
            self.logfile.close()
            raise Exception()

    def get_best_params_for_SVR(self, x_train, y_train):
        """
                Method Name: get_best_params_for_SVR
                Description: This method will load the SVR model and will tune the in-build parameter to
                get best possible accuracy.
                Output: None
                On Failure: Raise Exception


        """
        self.logfile = open(self.logFilepath, mode="a")
        self.logger_object.log(
            self.logfile,
            "Entered the get_best_params_for_SVR method of the " "Model_Finder class",
        )

        try:
            # Values for C
            C_values = [0.1, 1, 10, 100]

            # Values for epsilon
            epsilon_values = [0.3, 0.2, 0.1,]

            self.svr_grid = {
                "kernel": ["linear"],
                "C": C_values,
                "epsilon": epsilon_values,
            }

            # Creating an object of the SVR CV
            self.svr_cv = GridSearchCV(
                estimator=SVR(kernel="linear"),
                param_grid=self.svr_grid,
                scoring="r2",
                cv=5,
                verbose=5,
                n_jobs=4
            )

            # finding the best parameter
            self.svr_cv.fit(x_train, y_train)

            # Creating a new model with required parameter
            self.svr = self.svr_cv.best_estimator_

            # Training the new model
            self.svr.fit(x_train, y_train)
            self.logger_object.log(
                self.logfile,
                "SVR best params: "
                + str(self.svr.C)
                + ". Exited the get_best_params_for_linear_regression method of the Model_Finder "
                "class",
            )
            self.logfile.close()
            return self.svr

        except Exception as e:
            self.logger_object.log(
                self.logfile,
                "Exception occurred in get_best_params_for_SVR method "
                "of the Model_Finder class.",
            )
            self.logger_object.log(
                self.logfile,
                "SVR Parameter tuning  failed.Exited the "
                "get_best_params_for_random_forest method of the Model_Finder class",
            )
            self.logfile.close()
            raise Exception()

    def get_best_model(self, x_train, x_test, y_train, y_test):

        self.logfile = open(self.logFilepath, mode="a")
        self.logger_object.log(
            self.logfile, "Entered the get_best_model method of the Model_Finder class"
        )
        self.list_of_files = []
        self.list_of_files_score = []

        try:
            # create best model for linear regression
            self.lasso = self.get_best_params_for_lasso_regression(x_train, y_train)
            self.prediction_lasso = self.lasso.predict(x_test)

            # Train Accuracy of Lasso Regression
            self.lasso_score_train = self.lasso.score(x_train, y_train)
            # print('lasso Train accuracy ', str(self.lasso_score_train))

            # Test Accuracy of Lasso Regression
            self.lasso_score_test = metrics.r2_score(y_test, self.prediction_lasso)
            # print('lasso Test accuracy ', str(self.lasso_score_test))
            self.list_of_files_score.append(self.lasso_score_test)

            # Difference in train and test accuracy
            self.diff_lasso = abs(self.lasso_score_train - self.lasso_score_test)
            # print('lasso accuracy train and test difference ', str(self.diff_lasso))
            self.list_of_files.append(self.diff_lasso)
            self.logfile = open(self.logFilepath, mode="a")
            self.logger_object.log(
                self.logfile,
                "Test Accuracy for Lasso Regression Model :"
                + str(self.lasso_score_test),
            )
            self.logger_object.log(
                self.logfile,
                "Train and Test Accuracy difference for Lasso Regression Model :"
                + str(self.diff_lasso),
            )
            # create best model for SVRegression
            self.svr = self.get_best_params_for_SVR(x_train, y_train)
            self.prediction_svr = self.svr.predict(x_test)

            # Train Accuracy of SVR
            self.svr_score_train = self.svr.score(x_train, y_train)

            # Test Accuracy of SVR
            self.svr_score_test = metrics.r2_score(y_test, self.prediction_svr)

            self.list_of_files_score.append(self.svr_score_test)
            # Difference in train and test accuracy
            self.diff_svr = abs(self.svr_score_train - self.svr_score_test)
            self.list_of_files.append(self.diff_svr)
            self.logfile = open(self.logFilepath, mode="a")
            self.logger_object.log(
                self.logfile, "Test Accuracy for SVR Model :" + str(self.svr_score_test)
            )
            self.logger_object.log(
                self.logfile,
                "Train and Test Accuracy difference for SVR Model :"
                + str(self.diff_svr),
            )
            self.logfile.close()

            # Keeping model with highest accuracy
            maxi = max(self.list_of_files_score)
            if maxi == self.lasso_score_test:
                return "Lasso Regression", self.lasso

            else:
                return "SVR Regression", self.svr

        except Exception as e:
            self.logger_object.log(
                self.logfile,
                "Exception occurred in get_best_model method of the Model_Finder class.Exception "
                "message:  " + str(e),
            )
            self.logger_object.log(
                self.logfile,
                "Model Selection Failed. Exited the get_best_model method of the Model_Finder class",
            )
            self.logfile.close()
            raise Exception()

