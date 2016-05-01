# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 19:08:45 2016

@author: Mike
"""


import numpy as np
import pandas as pd
import pylab as P
import matplotlib.colors as colours
import datetime
import sklearn.ensemble



test_forest = sklearn.ensemble.RandomForestClassifier(n_estimators = 50)

print(processed_data.info())
processed_data_X = processed_data[['year','X','Y','day','hour']]
processed_data_y = processed_data['Category']

test_forest.fit(processed_data_X,processed_data_y)
test_forest.score(processed_data_X,processed_data_y)

test_data = read_test_data()

test_data_X = test_data[['year','X','Y','day','hour']]
submission = test_forest.predict(test_data_X)

types = processed_data['Category'].unique()
types.sort()
submission_formatted = np.DataFrame(columns = ['Id']+types, index = range(0,len(submission)))

for type in submission_formatted.columns:
    submission_formatted[type] = 1*(submission == str(type))

submission_formatted['Id'] = range(0,len(submission))
submission_formatted.to_csv("submission.csv",sep=',',index=False)