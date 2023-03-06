#!/usr/bin/env python
#Script contains the function that cleans the null value in the dataset  

import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import datetime
#reading in the raws file and cleaning it, also discarding the raw file 
def clean_hackdata(raw_csv_file):
    
    honey_pot_data = pd.read_csv(raw_csv_file)
    null_filled_data = honey_pot_data.copy()
    #filling the null values with unknown
    for col in ['type','country','cc','locale','localeabbr','postalcode']:
        null_filled_data[col].fillna('unknown',axis=0,inplace=True)
    #filling the null values in case of floats with 0
    for col_name in ['spt','dpt']:
        #null_filled_data.fillna(0,inplace=True,axis=0)
        null_filled_data[col_name].fillna(0,inplace=True,axis=0)
    #creating the datetime_obj for easier manipulation later
    null_filled_data['datetime_obj'] = null_filled_data.datetime.apply(
            lambda x : datetime.datetime.strptime(x,'%m/%d/%y %H:%M')
            )
    #making three more columns, month and day of week
    null_filled_data['day_week'] = null_filled_data.datetime_obj. \
                apply(lambda x: x.day_name())

    null_filled_data['month_name'] = null_filled_data.datetime_obj. \
                apply(lambda x: x.month_name())

    null_filled_data['week_year'] = null_filled_data.datetime_obj. \
                apply(lambda x: x.weekofyear)

    null_filled_data['incident_hour'] = null_filled_data.datetime_obj. \
                apply(lambda x: x.hour)
    #dropping the column
    null_filled_data.drop(['datetime','Unnamed: 15'],inplace=True,axis=1)
    #removing the rows that have any null values
    null_filled_data.dropna(axis=0,inplace=True)
    #return the dataframe
    return null_filled_data

def group_by_col(datafrm,col_name):
    grp_df = datafrm.groupby(col_name).agg('count')
    grp_df.reset_index(inplace=True)
    grp_df.sort_values(by='src',ascending=False,inplace=True)
    return grp_df[[col_name,'src']]

def group_two_col(datafrm,col1, col2):
    grp_df = datafrm.groupby([col1,col2]).agg('count')
    grp_df.reset_index(inplace=True)
    grp_df.sort_values(by='src',ascending=False,inplace=True)
    return grp_df[[col1,col2,'src']]


