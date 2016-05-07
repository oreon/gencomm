import datetime

import pandas as pd


def calcDates(frequency, endDate = '2017-12-31'):
    END_DATE = pd.to_datetime(endDate)
    timeNow = datetime.datetime.today()
    anotherTime = timeNow
    
    listRetDates = []
    i = 1
    
    if frequency == 0:
        frequency = 30
    
    while anotherTime < END_DATE:
        anotherTime = timeNow + datetime.timedelta(days=frequency * (i))
        i = i+1
        listRetDates.append(anotherTime)
        
    return listRetDates


    
#print ( calcDates(40) )