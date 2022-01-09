from functools import partial
from typing import final
import pandas as pd
import re
from datetime import datetime
import numpy as np
from sklearn.utils.validation import indexable
import dataprep

#import data, prep it
theft, parking = dataprep.prepData()
parking_size = len(parking.index)
parking['Theft Count'] = np.zeros(parking_size)

f = open("testStuff.txt", 'w')

#define what the radius is going to be
radius = 0.001 #111m

#make a new df to store all the info
final_df = pd.DataFrame(columns=['Month', 'Day', 'DOW', "Thefts"], index= ["Coordinates"])

for i in range(0, parking_size - 1):
    long, lat = parking.iloc[i]['Longitude'], parking.iloc[i]['Latitude']
    
    #make a new dataframe for each parking spot which is full of the nearby thefts
    nearby_long = abs(theft['Longitude'] - long) <= radius
    nearby_lat = abs(theft['Latitude'] - lat) <= radius 
    
    #narrow down to inside radius
    theft_i = theft[nearby_lat & nearby_long]

    #grouped by month, day, day of week and counted how many occurrences there were
    theft_i_grouped = theft_i.groupby(['Month', 'Day', 'Occurrence_DayOfWeek']).size()
    print(theft_i_grouped, file=f)
    
    #add to final dataframe
    for t in theft_i_grouped.index:
        temp = pd.DataFrame(data={"Month": t[0], 'Day': t[1], 'DOW': t[2], 'Thefts': theft_i_grouped.loc[t]}, index=[(long, lat)])
        final_df = final_df.append(temp)
    

print(final_df.head(30), file=f)