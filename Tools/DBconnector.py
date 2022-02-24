# import cassandra
import yaml
from yaml.loader import SafeLoader
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from application_logging.logging import LoggerApp
import os


def yaml_parser(yaml_file_path):
    a = LoggerApp()
    try:
        file_ = open(os.path.join("Training_Logs","DataBaseConnectionLog.txt"), 'a+')
        a.log(file_object=file_, log_massage=" Entered into : DBconnectionInfo-YamlParser..")
        with open(yaml_file_path, 'r') as f:
            info = list(yaml.load_all(f, Loader=SafeLoader))
            f.close()
        a.log(file_,log_massage='Retrieved DatabaseInfo :  \n \t \t \t \t \t \t \t DatabaseName : {}  \n \t \t \t \t '
                                '\t \t \t client_id : {} \n  \t \t \t \t \t \t \t path_to_zip : {} '.format(info[0]['Database_name'], info[0]['keys_']['client_id'], info[0]['keys_']['path_to_zip']))
        file_.close()

    except Exception as e:
        a.log(file_, "YamlParser Exception : " + str(e))
        file_.close()
        raise e
    return info


class DBconnector:
    """ This Class will help to connect with server side cassandra database

    """

    def __init__(self):
        self.logger = LoggerApp()
        self.yml_path = os.path.join("Controllers","DBconnection_info.yaml")
        self.dataLoader = yaml_parser(self.yml_path)
        self.path_toZip = self.dataLoader[0]['keys_']['path_to_zip']
        self.client_id = self.dataLoader[0]['keys_']['client_id']
        self.client_sec = self.dataLoader[0]['keys_']['client_seck']

    def connect(self):
        """
            task : this method helps to connect the server based Cassandra Database..
            Inputs : secure .zip file , client_id , client_secret
            return: session or (cursor)
        """

        try:
            self.f = open(os.path.join("Training_Logs","DataBaseConnectionLog.txt"), 'a+')
            self.logger.log(self.f, 'entered into class : DBconnector')

            cloud_config = {
                'secure_connect_bundle': self.path_toZip
            }
            auth_provider = PlainTextAuthProvider(self.client_id, self.client_sec)
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            session = cluster.connect()
            session.default_timeout = 60
            row = session.execute("select release_version from system.local").one()
            if row:
                self.logger.log(self.f, ' DataBase Connected successfully....!')
                self.f.close()
            else:
                self.logger.log(self.f, 'Some Error Occurred in DataBase Connection.....!')
                self.f.close()

        except Exception as e:
            self.logger.log(self.f, 'Exception : ' + str(e))
            self.f.close()
            raise e

        return session

























