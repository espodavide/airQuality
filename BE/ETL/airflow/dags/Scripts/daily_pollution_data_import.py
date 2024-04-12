#%%
import requests
import pandas as pd
import json
import time
import datetime
import logging
import sys

from utils.dbUtilis import *
from utils.utils import load_config
from geopy.geocoders import Nominatim

config_path = "config_file/api_config.json"
config_data = load_config(config_path)

APP_ID = config_data["APP_ID"]
#%%
def get_logger():
    # logger config
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='app.log',
                        filemode='a')

    # logger creation
    logger = logging.getLogger()
    logger.propagate = False

    # console handler creation
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

logger = get_logger()

# Formatting the dates
now = datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)

date_start =  now - datetime.timedelta(days=2)
logger.info(f"Extraxing data from date: {date_start}")
date_start=int(time.mktime(date_start.timetuple()))

date_end = now - datetime.timedelta(days=1)
logger.info(f"Extraxing data to : {date_end}")
date_end=int(time.mktime(date_end.timetuple()))


# Instatiate DB tables
db_utils = dbutils()
#%%
# Query the db for the list of city with lati and longi
query= 'Select * from CITIES;'


data = db_utils.retrieve_data(query)
df_city=pd.DataFrame(data, columns=['ID','CITY','LATI','LONGI'])


# Starting api calls for historical pollution data
df_list=[]
count=0
for row in df_city.iterrows():
    lat = row[1]['LATI']
    lon = row[1]['LONGI']
    city = row[1]['CITY']
    id = row[1]['ID']

    logger.info(f'Getting the date for the city: {city}....')

    url = f'http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={date_start}&end={date_end}&appid={APP_ID}'
    logger.debug(url)
    res=requests.get(url=url)

    data = res.json()['list']
    extracted_data = [{'aqi': entry['main']['aqi'],
                    'co': entry['components']['co'],
                    'no': entry['components']['no'],
                    'no2': entry['components']['no2'],
                    'o3': entry['components']['o3'],
                    'so2': entry['components']['so2'],
                    'pm2_5': entry['components']['pm2_5'],
                    'pm10': entry['components']['pm10'],
                    'nh3': entry['components']['nh3'],
                    'dt': entry['dt']} for entry in data]

    df = pd.DataFrame(extracted_data)
    df['CITY'] = [city for _ in range(len(df))]
    df['CITY_ID'] = [id for _ in range(len(df))]

    df_list.append(df)
    time.sleep(5)
    
    count +=1
    logger.info(f"% of completition',{count/len(df_city)}")
    

df_final = pd.concat(df_list) 
df_final=df_final.reset_index(drop=True)
#%%

# Cols in name in caps
df_final.columns = [cols.upper() for cols in df_final.columns] 


# Converting the date
df_final['DATE']=df_final['DT'].apply(lambda x: datetime.datetime.utcfromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S') ) 
df_final['DATE'] = pd.to_datetime(df_final['DATE'], format='%Y-%m-%d %H:%M:%S')

# Strip the hours information
df_final['DATE']= df_final['DATE'].dt.date

# Calculate daily average
df_final= df_final.groupby(["CITY","CITY_ID","DATE"]).mean().reset_index()


# Inserting all the rows into the table in db

# Creation della query di inserimento
columns = ', '.join(df_final.columns)
values_template = ', '.join(['%s'] * len(df_final.columns))



insert_query = f"""INSERT INTO CITIES_POLLUTION ({columns}) VALUES ({values_template}) 
ON CONFLICT (CITY_ID, DATE) DO UPDATE  
SET  
    AQI = EXCLUDED.AQI,  
    CO = EXCLUDED.CO, 
    NO = EXCLUDED.NO, 
    NO2 = EXCLUDED.NO2,
    O3 = EXCLUDED.O3,
    SO2 = EXCLUDED.SO2,
    PM2_5 = EXCLUDED.PM2_5,
    PM10 = EXCLUDED.PM10,
    NH3 = EXCLUDED.NH3,
    DT = EXCLUDED.DT;"""

# Creation of tuples list
data_values = [tuple(x) for x in df_final.to_numpy()]

#Inserting data
db_utils.insert_and_write_data_to_db(insert_query,data_values,batch=True)


#%%

