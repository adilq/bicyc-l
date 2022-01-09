import pandas as pd
import re
from datetime import datetime

def prepData():
    #open files so we can see data easily
    # f = open("testStuff.txt", 'r+')
    # g = open("coordinates.txt", 'r+')

    #some functions that are helpful to format data
    def getCoords(geometry):
        '''look through the geometry thing given and extract coordinates into a tuple'''
        coords = re.search('[- ]\d+.\d+,[- ]\d+.\d+', geometry).group()
        return coords

    def string2Datetime(data, format):
        if type(data) == str:
            data = data.split()[0]
        else:
            data = str(data)
        return datetime.strptime(data, format)

    def getMonth(date):
        return date.month

    def getYear(date):
        return date.year

    def getDay(date):
        return date.day

    #load data
    bike_parking_df = pd.read_csv('datasets/Bicycle Parking Map Data.csv')
    thefts_df = pd.read_csv('datasets/Bicycle_Thefts.csv')


    #get only data that we need
    thefts_df = thefts_df[['Occurrence_Date', 'Occurrence_DayOfWeek', 'Occurrence_DayOfYear', 'Longitude', 'Latitude']]

    #get latitude and longitude coords from 'geometry' column (cause the existing ones are empty)
    bike_parking_df['coords'] = bike_parking_df['geometry'].apply(getCoords)
    bike_parking_df[['Longitude', 'Latitude']] = bike_parking_df['coords'].str.split(",", 1, expand=True)
    bike_parking_df = bike_parking_df[['Longitude', 'Latitude', 'coords']] #keep only latitude and longitude data
    bike_parking_df = bike_parking_df.astype({'Longitude':'float', 'Latitude': 'float'})


    #change occurence date into datetime
    thefts_df['Occurrence_Date'] = thefts_df["Occurrence_Date"].apply(string2Datetime, args=('%Y/%m/%d',))
    thefts_df['Month'] = thefts_df["Occurrence_Date"].apply(getMonth)
    thefts_df['Year'] = thefts_df["Occurrence_Date"].apply(getYear)
    thefts_df['Day'] = thefts_df["Occurrence_Date"].apply(getDay)


    return thefts_df, bike_parking_df