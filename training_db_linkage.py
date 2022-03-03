from Training_DataValidation.RawTrainingValidation import Raw_Data_validation
from Training_Database_Operations.Database_handler import Database_Operations
from application_logging.logging import LoggerApp
import os


class Main_trainingDataValidation:
    def __init__(self):
        self.logger = LoggerApp()
        self.Database_operations = Database_Operations()
        self.raw_data_validation = Raw_Data_validation(path='./Training_batch_files/')
        self.logger_file = os.path.join("Training_Logs","TrainingMainLog.txt")

    def train_validation(self):
        """
            Method : train_validation
            Aim : "This method connects the Database Module"
                    1.Validate the data files
                    2. create table and send data to the Cassandra database
                    3. Extract the data from table
                    4. Create seperate .csv file for imported dataset .
            Return : None
            On fault : raise the Exception .


        """
        log_f = open(self.logger_file, mode='a')
        self.logger.log(log_f, log_massage='\n' * 2)
        self.logger.log(log_f, log_massage='Training DB Operations started..')
        self.logger.log(log_f, log_massage='Connecting with database..')
        try:
            column_names, noofcolumns = self.raw_data_validation.valuesFromSchema()
            manual_regx = self.raw_data_validation.manualRegexCreation()
            # validate fIle name
            self.raw_data_validation.validationFileNameRaw(manual_regx)
            # validating the column lengths
            self.raw_data_validation.validateColumnLength(noofcolumns)
            # validating
            self.raw_data_validation.validateMissingValuesInWholeColumn()
            # Creating Database connection
            self.Database_operations.dbconnect()
            self.logger.log(log_f, log_massage='Database connection is successful')
            # creating GoodTraining table to store validated data (Good Data)
            self.Database_operations.CreateGoodTraining_table()

            self.logger.log(log_f, log_massage="Good Training Table Created Successfully....")
            self.logger.log(log_f, log_massage=" Inserting Good Data to the Table ....")
            
            self.Database_operations.DataInsertion()
            self.logger.log(log_f, log_massage="Database Insertion is Completed ....")

            
            # extracting the data from Database into the single .csv file
            self.logger.log(log_f, log_massage="Extracting the Good data  from Database....")
            self.Database_operations.DataImport()
            self.logger.log(log_f, log_massage="Data Extraction is completed stored in InputFile.csv ....")

            log_f.close()

        except Exception as e:
            self.logger.log(log_f, log_massage='Exception  : ' + str(e))
            log_f.close()
            raise e
