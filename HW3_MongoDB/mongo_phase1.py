#!/usr/bin/env python
import sys, json, pymongo
from bson import json_util
from urllib.request import urlopen
from pymongo import MongoClient
# load the find to mongodb
def initail():
	myurl = "https://gist.githubusercontent.com/tdreyno/4278655/raw/7b0762c09b519f40397e4c3e100b097d861f5588/airports.json"
	response = urlopen(myurl)
	data = json_util.loads(response.read())
	connection = MongoClient(port=27017)
	db = connection.Airports
	db.Airports.insert_many(data)

def Find(field, val):
    try:

	connection = MongoClient(port=27017)
	find = db.Airports.find({field: val})

    print("Here are the information: \n")
    for item in find:
        print(find)

    except Exception, e:
    print str(e)

def Add(code, latitude, longitude, name, city, state, country, woeid, tz, phone, email, url, runway, elevation, icao, flights, carriers):
    try:
    client = MongoClient()

    entry = {"code": code,
             "lat": latitude,
             "lon": longitude,
             "name": name,
             "city": city,
             "state": state,
             "country": country,
             "woeid": woeid,
             "tz": tz,
             "phone": phone,
             "email": email,
             "url": url,
             "runway_length": runway,
             "elev": elevation,
             "icao": icao,
             "direct_flights": flights,
             "carriers": carriers
             }
    
    db.Airports.insert(entry)
    
    except Exception, e:
    print str(e)


 def Update(query, field, value):
        try:
            
        client = MongoClient()
        db = client.Airports
        updateValue = {field:value}
        db.Airports.update_one(query, updateValue)
        
        except Exception, e:
            print str(e)


def main(): 
     if __name__ == "__main__":
        os.system("mongod")
        Initialize()
        while(1):
            selection = raw_input("Choose an action to perform on airport database:\n -To insert new airport type 1\n -For searching type 2\n -To update type 3\n")

            if selection == 1:
                    print("Please enter the following fields: \n")
                code = raw_input("Airport code: ")
                lat = raw_input("Latitude coordinate: ")
                lon = raw_input("Longitude coordinate: ")
                name = raw_input("Airport name: ")
                city = raw_input("City: ")
                state = raw_input("State: ")
                country = raw_input("Country: ")
                woeid = raw_input("woeid: ")
                tz = raw_input("tz: ")
                phone = raw_input("Phone number: ")
                email = raw_input("Email address: ")
                url = raw_input("url: ")
                runway = raw_input("runway length: ")
                elevation = raw_input("elevation: ")
                icao = raw_input("icao: ")
                directFlights = raw_input("direct flights: ")
                carriers = raw_input("carriers: ")
                Add(code, lat, lon, name, city, state, country, woeid, tz, phone, email, url, runway, elevation, icao, directFlights, carriers)
                Find(field, val)
            elif selection == 2:
                query = raw_input("Please enter the field you are looking for: ")
                projection = raw_input("Please enter a keyword: ")
                Search(query, projection)
            elif selection == 3:
                query = raw_input("Please enter the code for the airport to update: ")
                field = raw_input("Please enter a field to update: ")
                val = raw_input("Please enter the updated value for the field: ") 
                Update(query, field, val)
            else:
                print("ERROR! Invalid input")
