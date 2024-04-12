#%%
import psycopg2
import os
from utils import *
import logging

config_path = "../config_file/db_config.json"
config_data = load_config(config_path)
#%%

def get_logger():
    # Configurazione del logger
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='app.log',
                        filemode='a')

    # Creazione di un logger
    logger = logging.getLogger()
    logger.propagate = False

    # Aggiungi un gestore di console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
logger = get_logger()


class dbutils:
    def __init__(self) -> None:
        # Parametri di connessione al database
        self.__dbname = config_data["dbname"]
        self.__user = config_data["user"]
        self.__password = config_data["password"]
        self.__host = config_data["host"]
        self.__port = config_data["port"]
    def open_connection(self):
        """ Function that open the connection to the database provided"""
    # Connessione al database
        connec_succ=True
        try:
            conn = psycopg2.connect(dbname=self.__dbname, user=self.__user, password=self.__password, host=self.__host, port=self.__port)
            logger.info("Connessione riuscita!")
            return connec_succ, conn
        except Exception as e:
            logger.warning(f"Errore durante la connessione al database: {e}")
            connec_succ=False
            return connec_succ, e
    def close_connection(self,connection):
        """ Function that close the connection passed as parameter"""
        connection.close()
    def insert_and_write_data_to_db(self,query:str,param:tuple=None,batch=False)->None:
        """ Functions that helps to write rows or create table and returns nothing
        """
        _, connection = self.open_connection()

        cursor = connection.cursor()
        logger.info("Writing data to db...")

        if not batch:

            if param is None:
                cursor.execute(query)
            else:
                cursor.execute(query, param)
            
        else:
            cursor.executemany(query, param)

        connection.commit()
        self.close_connection(connection)


    
    def retrieve_data(self,query:str)->list:
        """ Functions that helps to write rows or create table and returns nothing
        """
        logger.info('Launching query...')

        _, connection = self.open_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

#%%