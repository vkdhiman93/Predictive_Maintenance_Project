# this file helps to create the Good_training_tables
from cassandra.concurrent import execute_concurrent_with_args
from cassandra.query import dict_factory
from application_logging.logging import LoggerApp
from Tools.DBconnector import DBconnector
from Tools.YamlParser import YamlParser
import csv
import os
import pandas as pd
# from pathlib import Path


class Database_Operations:
    def __init__(self):
        try:
            self.logger = LoggerApp()
            self.f_ = open(
                os.path.join("Training_Logs", "TrainingDatabseInfo.txt"), "a"
            )

            self.goodfilepath = os.path.join("Training_Raw_files_validated", "Good_Raw")

            self.yaml_path = os.path.join("Controllers", "DBconnection_info.yaml")
            # self.session = DBconnector().connect()
            self.key_space = YamlParser(self.yaml_path).yaml_parser()[0][
                "Good_training_tables_info"
            ]["keyspace_name"]
            self.Good_training_TableName = YamlParser(self.yaml_path).yaml_parser()[0][
                "Good_training_tables_info"
            ]["table_name"]
            self.logger.log(self.f_, "All the required Files are initialized ....")
            self.f_.close()
        except Exception as e:
            self.logger.log(file_object=self.f_, log_massage="Exception : " + str(e))
            self.f_.close()
            raise e

    def dbconnect(self):
        try:
            self.logger = LoggerApp()
            self.f_ = open(
                os.path.join("Training_Logs", "TrainingDatabseInfo.txt"), "a"
            )
            self.session = DBconnector().connect()
            self.logger.log(self.f_, "Database connection is successful")
            self.f_.close()
        except Exception as e:
            self.logger.log(file_object=self.f_, log_massage="Exception : " + str(e))
            self.f_.close()
            raise e

    def CreateGoodTraining_table(self):
        """ Task : this method will create the GoodTraining Table to store the Validated data.
            Inputs : Receives the Inputs from "DBconnection_info.yaml" files
            Ip/1 : database connector pointer
            Ip/2 : Good-Training-TableName
            Ip/3 : particular keyspace
            return : None
        """
        try:
            self.f_ = open(
                os.path.join("Training_Logs", "TrainingDatabseInfo.txt"), "a"
            )
            self.logger.log(
                self.f_, "Entered into the class : CreateGoodTraining_table ...."
            )
            self.session.execute(f"use {self.key_space}")
            self.session.execute(
                f"CREATE TABLE if not exists {self.Good_training_TableName} (unit_nr  float , time_cycles  float , setting_1  float, "
                f"setting_2 float, setting_3 float,s_1 float, s_2 float, s_3 float, s_4 float, s_5 float, s_6 float, s_7 float, "
                f"s_8 float, s_9 float, s_10 float, s_11 float, s_12 float, s_13 float, s_14 float, s_15 float, s_16 float, "
                f"s_17 float, s_18 float, s_19 float, s_20 float, s_21 float, PRIMARY KEY(unit_nr, time_cycles, setting_1, setting_2,"
                f"setting_3, s_1, s_2, s_3, s_4, s_5, s_6, s_7, s_8, s_9, s_10, s_11, s_12, s_13, s_14, s_15, s_16, s_17, s_18, s_19, s_20, s_21)) ;"
            )
            self.logger.log(
                self.f_, f"{self.Good_training_TableName}  created Successfully !...."
            )
            self.f_.close()
        except Exception as e:
            self.logger.log(file_object=self.f_, log_massage="Exception : " + str(e))
            self.f_.close()
            raise e

    def DataInsertion(self):
        """
                Method Name: DataInsertion
                Description: This method inserts the Good data files from the Training_Raw_files folder into the
                            above created table.
                Output: None
                On Failure: Raise Exception


        """

        goodfilepath = self.goodfilepath
        log_f = open(os.path.join("Training_Logs", "DataImportExport.txt"), "a")
        self.logger.log(
            log_f, "Entered Into Class : DataBaseOperations > DataInsertion "
        )
        self.logger.log(
            log_f,
            f"Files found in Training Raw dirs  :{str(os.listdir(self.goodfilepath))}",
        )

        try:
            self.session.execute(f"use {self.key_space}")
            files = [file_ for file_ in os.listdir(self.goodfilepath)]
            for file_ in files:
                f_path = os.path.join(goodfilepath, file_)
                # pandas operations
                # define column names for easy indexing
                index_names = ["unit_nr", "time_cycles"]
                setting_names = ["setting_1", "setting_2", "setting_3"]
                sensor_names = ["s_{}".format(i) for i in range(1, 22)]
                col_names = index_names + setting_names + sensor_names
                data = pd.read_csv(f_path, sep="\s+", header=None, names=col_names)
                a = data.values
                try:
                    prepared = self.session.prepare(
                        f"INSERT INTO {self.Good_training_TableName} (unit_nr,time_cycles,setting_1,setting_2,setting_3,"
                        f"s_1,s_2,s_3,s_4,s_5,s_6,s_7,s_8,s_9,s_10,s_11,s_12,s_13,s_14,s_15,s_16,s_17,s_18,s_19,s_20,s_21)"
                        f" VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    )
                    execute_concurrent_with_args(self.session, prepared, a)


                    self.logger.log(
                        log_f, log_massage="Data Uploaded successfully ...."
                    )
                    log_f.close()

                except Exception as e:
                    self.logger.log(
                        log_f, "Exception Occurs in Data Insertion Process  ... . "
                    )
                    self.logger.log(log_f, "Exception " + str(e))
                    raise e

        except Exception as e:
            self.logger.log(file_object=log_f, log_massage="Exception : " + str(e))
            log_f.close()
            raise e

    def DataImport(self):
        """
                MethodName : DataImport
                Task : This  method will Import the Data from  Table & convert / store this data into the Csv Format .
                Output file location : 'Training_FileFromDB/'
                return : None


        """
        self.fileFromDb = "Training_FileFromDB/"
        self.fileName = "InputFile.csv"  # the file In which data will be storing
        log_f = open(
            os.path.join("Training_Logs", "DataImportExport.txt"), "a"
        )  # Log File to Capture Process
        self.logger.log(log_f, "Entered Into Class : DataBaseOperations > DataImport ")

        # creating the Dir to store the Data
        if not os.path.isdir(self.fileFromDb):
            os.makedirs(self.fileFromDb)

        try:
            self.session.execute(f"use {self.key_space}")
            Query = f"select * from {self.Good_training_TableName} ;"
            self.session.row_factory = dict_factory
            rows = list(self.session.execute(Query))
            # storing the data into csv file
            try:
                fieldnames = [
                    "unit_nr",
                    "time_cycles",
                    "setting_1",
                    "setting_2",
                    "setting_3",
                    "s_1",
                    "s_2",
                    "s_3",
                    "s_4",
                    "s_5",
                    "s_6",
                    "s_7",
                    "s_8",
                    "s_9",
                    "s_10",
                    "s_11",
                    "s_12",
                    "s_13",
                    "s_14",
                    "s_15",
                    "s_16",
                    "s_17",
                    "s_18",
                    "s_19",
                    "s_20",
                    "s_21",
                ]
                with open(
                    self.fileFromDb + self.fileName, mode="w", newline=""
                ) as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)

                self.logger.log(
                    file_object=log_f,
                    log_massage=f" Data Imported in to file {os.path.join(self.fileFromDb, self.fileName)}",
                )
                log_f.close()

            except Exception as e:
                self.logger.log(
                    log_f, log_massage="Exception : Method : DataImport => " + str(e)
                )
                log_f.close()
                raise e

        except Exception as e:
            self.logger.log(
                log_f, log_massage="Exception : Method : DataImport => " + str(e)
            )
            log_f.close()
            raise e
