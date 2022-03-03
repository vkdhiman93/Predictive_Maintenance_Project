# input the filepath/or databasepath / link where the data is sored
# tentative file

import os
import json
import pandas as pd
from datetime import datetime
import shutil
from application_logging.logging import LoggerApp
import re


class Raw_Data_validation:
    def __init__(self, path):
        # path = Data dir path ,
        # path can be : Database path or Dirs Path
        self.schema_path = 'Training_Schema.json'
        self.Batch_Directory = path  # directory where the raw data is placed
        self.logger = LoggerApp()

    def valuesFromSchema(self):
        """
        this function read the training_json file and store the all validation requirement
        information in dictionary which will be use in  further process
        :return:
        schema_ditionary : (key :values)
        """
        try:
            with open(self.schema_path, 'r') as f:
                schema_dictionary = json.load(f)
                f.close()

            # All the required info
            pattern = schema_dictionary['SampleFileName']
            number_of_columns = schema_dictionary["NumberofColumns"]
            column_names = schema_dictionary["ColName"]

            # write the info in logs
            # log_file_path  = "Training_Logs/valuesfromSchemaValidationLog.txt"
            log_file_path = os.path.join("Training_Logs", "valuesfromSchemaValidationLog.txt")
            file_log = open(log_file_path, "a+")
            message = "NumberofColumns:: %s" % number_of_columns + "\n"
            self.logger.log(file_log, message)
            file_log.close()

        except ValueError:
            # log_file_path = "Training_Logs/valuesfromSchemaValidationLog.txt"
            log_file_path = os.path.join("Training_Logs", "valuesfromSchemaValidationLog.txt")
            file_log = open(log_file_path, "a+")
            message = "ValueError : Value not found inside schema_training.json"
            self.logger.log(file_log, message)
            file_log.close()
            raise ValueError

        except KeyError:
            # log_file_path = "Training_Logs/valuesfromSchemaValidationLog.txt"
            log_file_path = os.path.join("Training_Logs", "valuesfromSchemaValidationLog.txt")
            file_log = open(log_file_path, "a+")
            message = "KeyError:Key value error incorrect key passed"
            self.logger.log(file_log, message)
            file_log.close()
            raise KeyError

        except Exception as e:
            # log_file_path = "Training_Logs/valuesfromSchemaValidationLog.txt"
            log_file_path = os.path.join("Training_Logs", "valuesfromSchemaValidationLog.txt")
            file_log = open(log_file_path, 'a+')
            self.logger.log(file_log, str(e))
            file_log.close()
            raise e

        return column_names, number_of_columns

    def manualRegexCreation(self):
        """
                                Method Name: manualRegexCreation
                                Description: This method contains a manually defined regex based on the "FileName" given in "Schema" file.
                                            This Regex is used to validate the filename of the training data.
                                Output: Regex pattern
                                On Failure: None
        """
        regex = "['train']+['\_']+['FD']+[\d]+\.txt"
        return regex

    def createDirectoryForGoodBadRawData(self):
        """
            method Name : createDirectoryForGoodBadRawData
            Aim : create  the directories for the good data and bad raw data if not exist
            Error: OSError
            dir_path = "Training_Raw_files_validated/", "Good_Raw/"
            :return: None
        """
        try:
            path = os.path.join("Training_Raw_files_validated/", "Good_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)

            # for the bad data
            path = os.path.join("Training_Raw_files_validated/", "Bad_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)

        except OSError as ex:
            file = open(os.path.join("Training_Logs", "GeneralLog.txt"), 'a+')
            self.logger.log(file, "Error while creating Directory %s:" % ex)
            file.close()
            raise OSError

    def deleteExistingGoodDataTrainingFolder(self):
        """
                Method name : def deleteExistingGoodDataTrainingFolder
                Aim : to delete the existing good data folder once we move the good data
                        to the  Databases , increases the usability
                Error : on failure : OSError
                  :return: None

        """
        path = 'Training_Raw_files_validated/'

        try:
            if os.path.isdir(os.path.join(path, "Good_Raw/")):
                shutil.rmtree(os.path.join(path, "Good_Raw/"))
                log_file = open(os.path.join("Training_Logs", "GeneralLog.txt"), 'a+')
                self.logger.log(log_file, "GoodRaw directory deleted successfully!!!")
                log_file.close()

        except OSError as s:
            er_file = open(os.path.join("Training_Logs", "GeneralLog.txt"), 'a+')
            self.logger.log(er_file, "Error while Deleting Directory : %s" % s)
            er_file.close()
            raise OSError

    def deleteExistingBadDataTrainingFolder(self):
        """
           Method Name: deleteExistingBadDataTrainingFolder
            Description: This method deletes the directory made  to store the Bad Data
                      after moving the data in an archive folder. We archive the bad
                      files to send them back to the client for invalid data issue.
            On Failure: OSError
           return :None """
        path = 'Training_Raw_files_validated/'
        log_file = open(os.path.join("Training_Logs", "GeneralLog.txt"), 'a+')

        try:
            if os.path.isdir(os.path.join(path, "Bad_Raw/")):
                shutil.rmtree(os.path.join(path, "Bad_Raw/"))

                self.logger.log(log_file, "Bad_Raw directory deleted successfully!!!")
                log_file.close()

        except OSError as s:
            er_file = open(os.path.join("Training_Logs", "GeneralLog.txt"), 'a+')
            self.logger.log(log_file, "Error while Deleting Directory : " + str(s))
            log_file.close()
            raise OSError

    def moveBadFilesToArchiveBad(self):
        """
                Method Name: moveBadFilesToArchiveBad
                Description:   This method move the Bad Data
                               in an archive folder. We archive the bad
                              files to send them back to the client for invalid data issue.
                Output: None
                On Failure: OSError
                :return: None

        """
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")
        try:
            # source = 'Training_Raw_files_validated/Bad_Raw/'
            source = os.path.join("Training_Raw_files_validated/", "Bad_Raw/")
            if os.path.isdir(source):
                path = "TrainingArchiveBadData"
                if not os.path.isdir(path):
                    # creating TrainingArchiveBadData folder
                    os.makedirs(path)
                destination = 'TrainingArchiveBadData/BadData_' + str(date) + "_" + str(time)
                # making new dir
                if not os.path.isdir(destination):
                    os.makedirs(destination)

                files = os.listdir(source)  # getting the all bad files present in bad data folder
                for f in files:
                    if f not in os.listdir(destination):
                        shutil.move(source + f, destination)
                log_file = open("Training_Logs/GeneralLog.txt", 'a+')
                self.logger.log(log_file, "Bad Files Move to Archive")

                # delete the bad raw data folder
                path = 'Training_Raw_files_validated/'
                if os.path.isdir(os.path.join(path, "Bad_Raw/")):
                    shutil.rmtree(os.path.join(path, "Bad_Raw/"))
                self.logger.log(log_file, "Bad Raw Data Folder Deleted successfully!!")
                log_file.close()

        except Exception as e:
            file = open("Training_Logs/GeneralLog.txt", 'a+')
            self.logger.log(file, "Error while moving bad files to archive:: %s" % e)
            file.close()
            raise e

    def validationFileNameRaw(self, regex):
        """
            method : validationFileNameRaw
            Description : this method Validate the Training File names
            : # param regex: "['train']+['\_']+['FD']+[\d]+\.txt"
            
            :return:
        """
        # delete the directories for good and bad data in case last run was unsuccessful and
        # folders were not deleted.
        self.deleteExistingBadDataTrainingFolder()
        self.deleteExistingGoodDataTrainingFolder()

        # create new directories for the good and bad data
        self.createDirectoryForGoodBadRawData()
        only_files = [x for x in os.listdir(self.Batch_Directory)]

        try:

            log_file = open("Training_Logs/nameValidationLog.txt", "a+")
            for filename in only_files:
                if re.match(regex, filename):
                    
                    shutil.copy(os.path.join("Training_Batch_Files", filename),
                                os.path.join("Training_Raw_files_validated", "Good_Raw"))
                    self.logger.log(log_file, "Valid File name!! File moved to GoodRaw Folder :: %s" % filename)

                else:
                    shutil.copy(os.path.join("Training_Batch_Files", filename),
                                os.path.join("Training_Raw_files_validated", "Bad_Raw"))
                    self.logger.log(log_file, "Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
            log_file.close()

        except Exception as e:
            f = open(os.path.join("Training_Logs", "nameValidationLog.txt"), 'a+')
            self.logger.log(f, "Error Occurs while validating FileName %s" % e)
            f.close()
            raise e

    def validateColumnLength(self, NumberofColumns):
        """
              Method Name: validateColumnLength
              Description: This function validates the number of columns in the txt or csv files.
                           It is should be same as given in the schema file.
                           If not same file is not suitable for processing and thus is moved to Bad Raw Data folder.
                           If the column number matches, file is kept in Good Raw Data for processing.
              Output: None
              On Failure: Exception

        """
        try:
            f = open(os.path.join("Training_Logs", "columnValidationLog.txt"), 'a+')
            self.logger.log(f, "Column Length Validation Started!!")
            for file_ in os.listdir(os.path.join("Training_Raw_files_validated/", "Good_Raw/")):
                df = pd.read_csv(os.path.join("Training_Raw_files_validated/", "Good_Raw/") + file_, sep='\s+', header=None)
                if df.shape[1] == NumberofColumns:
                    pass
                else:
                    shutil.move(os.path.join("Training_Raw_files_validated", "Good_Raw") + file_,
                                os.path.join("Training_Raw_files_validated", "Bad_Raw"))
                    self.logger.log(f,
                                    "Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file_)
            self.logger.log(f, "Column Length Validation Completed!!")

        except OSError:
            f = open(os.path.join("Training_Logs", "columnValidationLog.txt"), 'a+')
            self.logger.log(f, "Error Occurred while moving the file :: %s" % OSError)
            f.close()
            raise OSError

        except Exception as e:
            f = open(os.path.join("Training_Logs", "columnValidationLog.txt"), 'a+')
            self.logger.log(f, "Error Occurred:: %s" % e)
            f.close()
            raise e
        f.close()

    def validateMissingValuesInWholeColumn(self):
        """
            Method Name: validateMissingValuesInWholeColumn
            Description: This function validates if any column in the txt or csv file has all values missing.
                       If all the values are missing, the file is not suitable for processing.
                       SUch files are moved to bad raw data.
            Output: None
            On Failure: Exception
        :return: None

        """
        try:
            f = open(os.path.join("Training_Logs", "missingValuesInColumn.txt"), 'a+')
            self.logger.log(f, "Missing Values Validation Started!!")

            for file_ in os.listdir(os.path.join("Training_Raw_files_validated/", "Good_Raw/")):
                csv = pd.read_csv(os.path.join("Training_Raw_files_validated/", "Good_Raw/") + file_, sep='\s+', header=None)
                count = 0
                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count += 1
                        shutil.move(os.path.join("Training_Raw_files_validated/", "Good_Raw/") + file_,
                                    os.path.join("Training_Raw_files_validated", "Bad_Raw"))
                        self.logger.log(f,
                                        "Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file_)
                        break
                
            self.logger.log(f, "Missing Values Validation Completed!!")
        except OSError:
            f = open(os.path.join("Training_Logs", "missingValuesInColumn.txt"), 'a+')
            self.logger.log(f, "Error Occurred while moving the file :: %s" % OSError)
            f.close()
            raise OSError
        except Exception as e:
            f = open(os.path.join("Training_Logs", "missingValuesInColumn.txt"), 'a+')
            self.logger.log(f, "Error Occurred:: %s" % e)
            f.close()
            raise e
        f.close()
