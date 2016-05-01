# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 15:34:33 2016

@author: Mike

Kaggle competition - preliminary ideas and exploration.
"""
import numpy as np
import pandas as pd
import pylab as P
import matplotlib.colors as colours
import datetime

#Import and clean the data.

def maketime(t):
    return int(str(i)[:2]) 

def read_data():
    raw_data = pd.read_csv("train.csv")
    
    processed_data = pd.DataFrame( )
    processed_data['date'] = pd.to_datetime(raw_data['Dates'],format = "%Y-%m-%d %H:%M:%S")
    processed_data['year'] = processed_data.date.map(lambda x:x.year)
    processed_data[['Address','X','Y','Category']] = raw_data[['Address','X','Y','Category']]
    weekdays = {"Monday":0, "Tuesday":1, "Wednesday":2, "Thursday":3, "Friday":4, "Saturday":5, "Sunday":6}
    processed_data['day'] = raw_data['DayOfWeek'].replace(weekdays)
    processed_data['PdDistrict'] = raw_data['PdDistrict']
    districts = {raw_data['PdDistrict'].unique()[i]:i for i in range(0,len(raw_data['PdDistrict'].unique()))}
    processed_data['district'] =  raw_data['PdDistrict'].replace(districts)
    processed_data['time'] = processed_data['date'].apply( lambda x:x.time())
    processed_data['hour'] = processed_data['time'].apply( maketime)
    
    
    #Filter out some apparent errors in the location data. 
    processed_data = processed_data[processed_data['X']<-122.0]#[processed_data.any('X'>-122.0,'X'<-123.0)]]#['X'] > -122.0  processed_data['X'] < -123.0]]
    
    return(processed_data)

def read_test_data():
    raw_data = pd.read_csv("test.csv")
    
    processed_data = pd.DataFrame( )
    processed_data['date'] = pd.to_datetime(raw_data['Dates'],format = "%Y-%m-%d %H:%M:%S")
    processed_data['year'] = processed_data.date.map(lambda x:x.year)
    processed_data[['Address','X','Y']] = raw_data[['Address','X','Y']]
    weekdays = {"Monday":0, "Tuesday":1, "Wednesday":2, "Thursday":3, "Friday":4, "Saturday":5, "Sunday":6}
    processed_data['day'] = raw_data['DayOfWeek'].replace(weekdays)
    districts = {raw_data['PdDistrict'].unique()[i]:i for i in range(0,len(raw_data['PdDistrict'].unique()))}
    processed_data['district'] =  raw_data['PdDistrict'].replace(districts)
    processed_data['PdDistrict'] = raw_data['PdDistrict']
    processed_data['time'] = processed_data['date'].apply( lambda x:x.time())
    processed_data['hour'] = processed_data['time'].apply( maketime)
    
    
    return(processed_data)


jet = P.get_cmap('jet')
greys = P.get_cmap('pink')


#Print a plot of where prostitution took place by year. 

def crime_loc_plot(types = "all", y = "all"):   
        print("printing...")  
        printdata = processed_data
        if types != "all":
            printdata = printdata[ printdata['Category'].isin(types)]
        if y != "all":
            printdata = printdata[ (printdata['year'] == y)]
        printdata.info()
        P.figure(figsize = (10,10))
        P.scatter(printdata['X'],printdata['Y'],cmap = greys,c = printdata['year'], s=16, lw=0)

def crime_year_graph(types = "all"):
    if types != "all":
        crimes_by_year = pd.DataFrame(index = range(2003,2015+1), columns = types)
        crimes_by_year_norm = pd.DataFrame(index = range(2003,2015+1), columns = types)
        
        for type in types:
            crimes_by_year[type] = [ processed_data[ (processed_data['Category'] == type) & (processed_data['year'] == y)].shape[0] for y in range(2003,2015+1)]
            tot = crimes_by_year[type].sum()
            crimes_by_year_norm[type] = [float(crimes_by_year[type][y])/float(tot) for y in range(2003,2015+1)]
    
        P.figure(figsize = (10,10))
        for type in crimes_by_year_norm.columns:    
            P.plot(crimes_by_year_norm[type], c = P.cm.jet(crimes_by_year_norm.columns.get_loc(type) * 5))

    else:
       
       crimes_by_year = pd.DataFrame(index = range(2003,2015+1), columns = ["total"])
       crimes_by_year_norm = pd.DataFrame(index = range(2003,2015+1), columns = ["total"])
        
       crimes_by_year["total"] = [ processed_data[ (processed_data['year'] == y)].shape[0] for y in range(2003,2015+1)]
       tot = crimes_by_year["total"].sum()
       crimes_by_year_norm["total"] = [float(crimes_by_year["total"][y])/float(tot) for y in range(2003,2015+1)]
    
    P.figure(figsize = (10,10))
    for type in crimes_by_year_norm.columns:    
        P.plot(crimes_by_year_norm[type], c = P.cm.jet(crimes_by_year_norm.columns.get_loc(type) * 5))
       
       
def crime_time_graph(types = "all", y = "all"):   
    if types != "all":
        crimes_by_time = pd.DataFrame(index = [datetime.time(h,0) for h in range(0,24)], columns = types)
        crimes_by_time_norm = pd.DataFrame(index = [datetime.time(h,0) for h in range(0,24)], columns = types)
    else:
        crimes_by_time = pd.DataFrame(index = [datetime.time(h,0) for h in range(0,24)], columns = ["total"])
        crimes_by_time_norm = pd.DataFrame(index = [datetime.time(h,0) for h in range(0,24)], columns = ["total"])

    #timeinrange = lambda t: processed_data['time'].apply(lambda y : (y >= processed_data['time']) & (y < ())
            
    
    for t in crimes_by_time.index:        
        tplus = (datetime.datetime.combine(datetime.date.today(),t) + datetime.timedelta(seconds = 3600)).time()
        if t < datetime.time(23):
            processed_data['inrange'] = (processed_data['time'] < tplus) & (processed_data['time'] >= t)
        else:
            processed_data['inrange'] = (processed_data['time'] >= t)
        
        if types != "all":
            for type in types:
                    print(t,"   ",type)
                    crimes_by_time[type][t] = processed_data[ (processed_data['Category'] == type) & processed_data['inrange'] == True].shape[0]
        else:
            crimes_by_time["total"][t] = processed_data[ processed_data['inrange'] == True].shape[0]

         
    totalcrimes = [crimes_by_time[type].sum() for type in crimes_by_time.columns]
    for type in enumerate(crimes_by_time.columns):
        crimes_by_time_norm[type[1]] = crimes_by_time[type[1]].apply(lambda x: float(x) / float(totalcrimes[type[0]]))
    
    P.figure(figsize = (20,15))
    P.plot(crimes_by_time_norm)
                #crimes_by_time_norm[type] = [float(crimes_by_time[type][y])/float(tot) for y in  crimes_by_time['Time'] ]
               

#crimes_by_year = [ processed_data[ processed_data['Category'] == type]['year'].value_counts().sort_index() for 
