import pandas as pd
import re
from datetime import datetime

def prepData():
    #open files so we can see data easily
    f = open("testStuff.txt", 'r+')
    g = open("coordinates.txt", 'r+')

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


    #load data
    bike_parking_df = pd.read_csv('datasets/Bicycle Parking Map Data.csv')
    thefts_df = pd.read_csv('datasets/Bicycle_Thefts.csv')
    print(bike_parking_df, file=g)

    #get only data that we need
    thefts_df = thefts_df[['Occurrence_Date', 'Occurrence_Year', 'Occurrence_Month', 'Occurrence_DayOfWeek', 'Occurrence_DayOfMonth', 'Occurrence_DayOfYear', 'Occurrence_Hour', 'Longitude', 'Latitude']]

    #get latitude and longitude coords from 'geometry' column (cause the existing ones are empty)
    bike_parking_df['coords'] = bike_parking_df['geometry'].apply(getCoords)
    bike_parking_df[['Longitude', 'Latitude']] = bike_parking_df['coords'].str.split(",", 1, expand=True)
    bike_parking_df = bike_parking_df[['Longitude', 'Latitude', 'coords']] #keep only latitude and longitude data
    bike_parking_df = bike_parking_df.astype({'Longitude':'float', 'Latitude': 'float'})


    #change occurence date into datetime
    thefts_df['Occurrence_Date'] = thefts_df["Occurrence_Date"].apply(string2Datetime, args=('%Y/%m/%d',))
    thefts_df['Occurrence_Year'] = thefts_df["Occurrence_Year"].apply(string2Datetime, args=('%Y',))
    thefts_df['Occurrence_Month'] = thefts_df["Occurrence_Month"].apply(string2Datetime, args=('%B',))
    thefts_df['Occurrence_DayOfWeek'] = thefts_df["Occurrence_DayOfWeek"].apply(string2Datetime, args=('%A',))

    print(thefts_df, file=f)
    print(bike_parking_df, file=g)

    return thefts_df, bike_parking_df