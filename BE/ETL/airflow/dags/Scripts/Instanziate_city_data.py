# %%
import json
import time
import datetime
import logging

from utils.dbUtilis import *
from utils.utils import load_config

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="GetLoc")

geo_json_path="BE/ETL/config_file/limits_IT_provinces.geojson"
config_path = "config_file/api_config.json"
config_data = load_config(config_path)

APP_ID = config_data["APP_ID"]
# %%
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
# Formatting the dates

date_start = datetime.datetime(2024, 4, 1)
logger.info(f"Extraxing data from date: {date_start}")
date_start=int(time.mktime(date_start.timetuple()))

date_end = datetime.datetime.now()
logger.info(f"Extraxing data to : {date_end}")
date_end=int(time.mktime(date_end.timetuple()))

# %% [markdown]
# # Instatiate DB tables

db_utils = dbutils()
create_city_table_query="""
    CREATE TABLE IF NOT EXISTS CITIES (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(255) NOT NULL,
        LATITUDE DECIMAL(9,6) NOT NULL,
        LONGITUDE DECIMAL(9,6) NOT NULL
    );
"""
db_utils.insert_and_write_data_to_db(create_city_table_query)

# Create city pollution table
create_table_query = """
CREATE TABLE IF NOT EXISTS CITIES_POLLUTION (
    AQI INT,
    CO FLOAT,
    NO FLOAT,
    NO2 FLOAT,
    O3 FLOAT,
    SO2 FLOAT,
    PM2_5 FLOAT,
    PM10 FLOAT,
    NH3 FLOAT,
    DT INT,
    CITY VARCHAR(300),
    CITY_ID INT,
    DATE DATE
);
"""

db_utils.insert_and_write_data_to_db(create_table_query)

f=open(geo_json_path)
geo_data=json.load(f)
city_name_json=[]
for i in range(len(geo_data['features'])):
    prov_name=geo_data['features'][i]['properties']['prov_name']
    reg_name=geo_data['features'][i]['properties']['reg_name']
    city_name_json.append(f'{prov_name}, {reg_name}')
city_name_json.sort()


failed_city =[]
for loc in city_name_json:
    try:
        location = geolocator.geocode(loc)
        city,latitude,longitude= (location.address,location.latitude, location.longitude)

        logger.debug(city)
        query_str = f"INSERT INTO CITIES (NAME, LATITUDE, LONGITUDE) VALUES (%s, %s, %s);" # Utilizzo di escape per i valori della stringa per evitare SQL injection
        db_utils.insert_and_write_data_to_db(query_str,(city, latitude, longitude))
        time.sleep(5)

    except Exception as e:
        logger.warning(f'The city: {loc} has failed')
        failed_city.append(loc)
    
        

for loc in failed_city:
    try:
        location = geolocator.geocode(loc.split("/")[0])
        city,latitude,longitude= (location.address,location.latitude, location.longitude)

        logger.debug('Creating query for',city)
 
        query_str = f"INSERT INTO CITIES (NAME, LATITUDE, LONGITUDE) VALUES (%s, %s, %s);" # Utilizzo di escape per i valori della stringa per evitare SQL injection
        db_utils.insert_and_write_data_to_db(query_str,(city, latitude, longitude))
        time.sleep(1)
        
    except Exception as e:
        logger.warning(f'The city: {loc} has failed')
        raise e
        


# check that all the citiescoordinate are in the citiescoordinate table.

# Query di conteggio delle righe
query = "SELECT COUNT(*) FROM CITIES;"

count_list = db_utils.retrieve_data(query)
# Ottieni il risultato della query
count = count_list[0][0]
logger.debug(f"The number of cities in the database are: {count}")


