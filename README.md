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

*NOTE* - Avoid using training route while running on cloud as i have used Heroku Free Tier, 
which do not provides enough computation for model training and causes high memory usage error.  


## WorkFlow

![Project Flow - Flowchart (1)](https://user-images.githubusercontent.com/65784413/162396512-010cc8c4-5c44-4ddf-a0ee-5f9fd2f5198c.png)

# Snippets of Project
#### 1) Home Page:
![Home Page](https://user-images.githubusercontent.com/65784413/156516622-6855a63c-5aa8-4fc0-906c-9bde69044108.png)

#### 3) Training:
![Training](https://user-images.githubusercontent.com/65784413/156574546-682e12d2-8f89-4a41-b486-a369014e4f06.png)

#### 2) Prediction:
![Prediction](https://user-images.githubusercontent.com/65784413/156516644-1c4b70b7-742c-427b-ad83-bfd6b9931eba.png)


# Technologies & Packages Used


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

## Run Locally

Clone the project

```bash
git clone https://github.com/vkdhiman93/Predictive_Maintenance_Project.git
```

Go to the project directory

```bash
cd Predictive_Maintenance_Project
```

Install dependencies

```bash
pip install -r requirements.txt
```


Start the server

```bash
python app.py
```


## Usage

In Development If You Want to contribute? Great!

To fix a bug or enhance an existing module, follow these steps:

* Fork the repo

* Create a new branch
```javascript
git checkout -b new-branch
```

* Make the appropriate changes in the file

* Commit your changes
```javascript
git commit -am "New feature added"
```

* Push to the branch
```javascript
git push origin new-branch
```

* Create a pull request
```javascript
git pull
```

## Directory Structure

```
Predictive_Maintenance_Project
|   .gitignore
|   add_rul.py
|   app.py
|   prediction_file.py
|   Procfile
|   README.md
|   requirements.txt
|   runtime.txt
|   secure-connect-rul-project.zip
|   training_db_linkage.py
|   training_file.py
|   Training_Schema.json
|   
+---Analysis
|       EDA_RUL_assumption_and_SVR.ipynb
|       RUL_FD001.txt
|       test_FD001.txt
|       train_FD001.txt
|       
+---application_logging
|       logging.py 
|           
+---Controllers
|       DBconnection_info.yaml
|       
+---Data_Information
+---Data_Ingestion
|       data_loader.py
|           
+---Data_Preprocessing
|       preprocessing.py
|           
+---Model
|   \---Lasso Regression
|           Lasso Regression.sav
|           
+---Model_Finder
|       model.py
|           
+---Prediction_Logs
|       PredictionLog.txt
|       
+---Prediction_Output_File
|       Predictions.csv
|       
+---Save_Model
|       save_methods.py
|           
+---static
|   +---css
|   |       style.css
|   |       
|   \---js
|           app.js
|           
+---templates
|   +---macros
|   |       input_macros.html
|   |       
|   \---public
|       |   index.html
|       |   predict.html
|       |   training.html
|       |   upload_csv.html
|       |   
|       \---templates
|               public_template.html
|               
+---Tools
|       DBconnector.py
|       training_logFilesCretaor.py
|       YamlParser.py
|       __init__.py
|           
+---Training_Batch_Files
|       train_FD001.txt
|       
+---Training_Database_Operations
|       Database_handler.py
|       __init__.py
|           
+---Training_DataValidation
|       RawTrainingValidation.py
|           
+---Training_FileFromDB
|       InputFile.csv
|       RUL_FD001.txt
|       test_FD001.txt
|       
+---Training_Logs
|       columnValidationLog.txt
|       DataBaseConnectionLog.txt
|       DataImportExport.txt
|       Datapreprocessing_logs.txt
|       GeneralLog.txt
|       missingValuesInColumn.txt
|       ModelTrainingLog.txt
|       nameValidationLog.txt
|       TrainingDatabseInfo.txt
|       TrainingMainLog.txt
|       valuesfromSchemaValidationLog.txt
|       yaml_parser.txt
|       
+---Training_Raw_files_validated
    +---Bad_Raw
    \---Good_Raw
            train_FD001.txt
```
