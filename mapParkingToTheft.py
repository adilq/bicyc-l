from functools import partial
import pandas as pd
import re
from datetime import datetime
import numpy as np
import dataprep

#import data, prep it
theft, parking = dataprep.prepData()
parking_size = len(parking.index)
parking['Theft Count'] = np.zeros(parking_size)


#define what the radius is going to be
radius = 0.001 #111m

#make a list to count the number of thefts near each parking spot
count = []

for i in range(0, parking_size - 1):
    long, lat = parking.iloc[i]['Longitude'], parking.iloc[i]['Latitude']
    
    #make a new dataframe for each parking spot which is full of the nearby thefts
    nearby_long = abs(theft['Longitude'] - long) <= radius
    nearby_lat = abs(theft['Latitude'] - lat) <= radius 
    
    theft_i = theft[nearby_lat & nearby_long]

    #count how many thefts happened w/in the parking spot radius and add to the list
    count.append(len(theft_i.index))

#add count to the theft count column of the dataframe
parking['Theft Count'] = pd.Series(count)

print(parking.head(30))