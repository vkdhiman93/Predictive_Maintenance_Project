# Predictive Maintenance ML Project

## Problem Statement
In industry, prognostics and health management are key topics for anticipating asset
state and avoiding downtime and breakdowns. Run-to-Failure simulation data from
turbofan jet engines is included.

The C-MAPSS software was used to simulate engine degradation. Four separate sets
of operational conditions and fault modes were simulated in four different ways. To
characterize fault progression, record numerous sensor channels. The Prognostics CoE
at NASA Ames provided the data set.

#### Prediction Goal
The main goal is to predict the remaining useful life (RUL) of each engine. RUL is
equivalent of number of flights remained for the engine after the last data point in the
test dataset.

The engine is operating normally at the start of each time series, and develops a fault at some point during the series.
In the training set, the fault grows in magnitude until system failure. In the test set, the time series ends some time prior to system failure.

The objective of the project is to predict the number of remaining operational cycles before failure in the test set, i.e., the number of operational cycles after the last cycle that the engine will continue to operate.
## Approach
  <p> The main goal is to predict the Remaining Useful Life (RUL) of each engine.<p>
  <pre>
  <li> Data Collection                    : Data has been collected from the Kaggle platform
  <li> Log creation                       : Created logging in order keep track of each step and to understand the workflow
  <li> Data insertion into Database       : Used Cassandra Db (datastax) for data Insertion
  <li> Exploratory data analysis          : Used Pandas profiling for EDA part and  generated a 
                                            report and stored in analysis folder
  <li> Feature Engineering                : Tried to keep relevant features(sensor readings) and 
                                            standardized the variables
  <li> Model creation and Model Tuning   : Tried to create Lasso CV and Support Vector Regression and by 
                                            using grid search cv and cross validation tried to tune the model.
 <li> Pickel file creation                : After Creation of model, saved model in pickle format.
 <li>Frontend and Deployment              : Used Flask web framework for frontend and Deployed the model on Heroku Cloud platform.
 </pre>
 
 ## Deployment Links (Heroku)
link : https://predictive-maintenance-project.herokuapp.com/ <br>

# Technologies Used

* VSCode, Pycharm used for IDE.
* For Visualization Of The Plots Matplotlib , Seaborn Are Used.
* Heroku is used For Model Deployment.
* Cassandra Database is used for Database Operations.
* Front End Deployment Is Done Using HTML , CSS.
* Flask is for creating the application server and pages.
* GitHub Is Used As A Version Control System.

* os is used for creating and deleting folders.
* csv is used for creating .csv format file.
* numpy is used for arrays computations and mathematical operations
* pandas is used for Manipulation and wrangling structured data
* scikit-learn is used for machine learning tool kit
* pickle is used for saving model
* Lasso Regression, SVR with GridSearchCV were used as the regression algorithms for model building