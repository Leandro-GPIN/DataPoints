#!/usr/bin/env python

import os
from geopy.geocoders import Nominatim
import psycopg2
from config import config

# read data points file
def read_text_file():
    latitude = []
    longitude = []
    
    path = os.getcwd()
    resource = os.path.join(path,'resource')
    
    for file_name in os.listdir(resource):
        with open(os.path.join(resource, file_name), 'r', encoding='utf-8') as t:
            for n, i in enumerate(t.readlines()):
                if('Latitude' == i.split(':')[0]):
                    latitude.append(i.split(':')[1].strip().split('  ')[1])
                elif('Longitude' == i.split(':')[0]):
                    longitude.append(i.split(':')[1].strip().split('  ')[1])
                    
    return latitude, longitude

# get data points information
def getaddress(lat, lng, language="en"):
        try:
            geolocator = Nominatim(user_agent="data_points")
            string = str(lat) + ', ' +str(lng)
            location = geolocator.reverse(string, language=language)
            data = location.raw
            data = data['address']
            address = data
        except:
            address='error'
            
        return address
    
# insert information into database
def insert_data(lat, lng, data):
    
    # initialize variables to data receive
    road = house_number = suburb = city = postalCode = state = country = ''
    
    # verify if information exist
    if 'road' in data:
        road = str(data['road']).strip()

    if 'house_number' in data:  
        house_number = str(data['house_number']).strip()

    if 'suburb' in data: 
        suburb = str(data['suburb']).strip().upper()

    if 'city' in data:
        city = str(data['city']).strip().upper()

    if 'postcode' in data:    
        postalCode = str(data['postcode']).strip()

    if 'state' in data: 
        state = str(data['state']).strip()

    if 'country' in data: 
        country  = str(data['country']).strip()
    
    # sql to insert information into database
    sql = """INSERT INTO data_points(latitude, longitude, rua, numero, bairro, cidade, cep, estado, pais)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    conn = None
   
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (lat, lng, road, house_number, suburb, city, postalCode, state, country))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
 
    # get coordenates
    print('Reading File!')
    x, y = read_text_file()
     
    print('Geting information and inserting to database!')
    # execute for each coordenate
    total = len(x)
    for i in range(0, total):
        #get geo information by coordenates
        data = getaddress(x[i], y[i])
        #if error don't execute insert into databse
        if(data != 'error'):
            insert_data(str(x[i]), str(y[i]), data)
        else:
            print('line error: ', i)
            
        if(i % int(total * 0.1) == 0):
            print('Progress: {0:.2f}%'.format((i / total)*100))
        
            
    print('Completed!!!')
            
         