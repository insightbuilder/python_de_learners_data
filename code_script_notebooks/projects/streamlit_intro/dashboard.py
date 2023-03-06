#!/usr/bin/env python
#Script creates the streamlit dashboard for the honeypot hackers data

import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from cleaning_ds import clean_hackdata,group_by_col,group_two_col 
import os
import shutil
st.set_page_config(page_title='Honeypot Dashboard',layout='wide')
st.markdown('## Honeypot Hacking Dashboard ')
clean_file = st.checkbox('Check this box if you want to clean below dataframe')
#reading in the raw file first using pandas if it exists 
if not clean_file:
    #extract data from zip
    shutil.unpack_archive('archive.zip')
    #read in the file delivered by the zip
    if os.path.isfile('AWS_Honeypot_marx-geo.csv'):
        try:
            raw_data = pd.read_csv('AWS_Honeypot_marx-geo.csv')
        except Exception as e:
            st.write('Remove the check mark on the above checkbox')
        #using streamlit to present the data
        st.write('The raw file available for analysis')
        st.dataframe(raw_data)
    else:
        st.write('Refer below cleaned dataframe')
else:
    #cleaning the data 
    st.write("Unpacking the file.3..2..1..")
    shutil.unpack_archive('archive.zip')
    st.write("Cleaning the dataframe.3..2..1..")
    cleaned_df = clean_hackdata('AWS_Honeypot_marx-geo.csv') 
    #printing the dataframe
    st.dataframe(cleaned_df)
    #lets fill in the overview of the data
    #how many incidents, how many hosts, how many attackers and how many countries
    incidents = cleaned_df.shape[0]
    hosts = len(cleaned_df.host.unique())
    attackers = len(cleaned_df.srcstr.unique())
    countries = len(cleaned_df.country.unique())
    #creating individual columns in streamlit
    st.write("### The overview of who and what is involved")
    col1,col2,col3,col4 = st.columns(4)
    col1.write("#### Total Incidents")
    col1.write(f"#### {incidents}")
    col2.write("#### Total Hosts")
    col2.write(f"#### {hosts}")
    col3.write("#### Total Attackers")
    col3.write(f"#### {attackers}")
    col4.write("#### Origin Country")
    col4.write(f"#### {countries}")
    #lets first create a drop down for the hosts
    hosts = cleaned_df.host.unique()
    filt1,filt2 = st.columns(2)
    focus_host = filt1.selectbox('Which host you want to drill down?',
                                 hosts,index=0)
    filter_host_df = cleaned_df[cleaned_df.host == focus_host]
    #Which month, day, hour and week the max attack happend for the host 
    #Lets get the grouped dataframes for the filtered dataframe
    month_grp = group_by_col(filter_host_df,'month_name')
    day_grp = group_by_col(filter_host_df,'day_week')
    hour_grp = group_by_col(filter_host_df,'incident_hour')
    week_grp = group_by_col(filter_host_df,'week_year')
    st.write("#### When the host is getting attacked the most")
    col5,col6,col7,col8 = st.columns(4)
    #populating max month
    max_month= month_grp.iloc[0,0] 
    max_month_count = month_grp.iloc[0,1]
    col5.write("Month")
    col5.write(f"#### {max_month}")
    col5.write(f"#### {max_month_count}")
    #populating max week 
    max_week = week_grp.iloc[0,0] 
    max_week_count = week_grp.iloc[0,1]
    col6.write("#### Week")
    col6.write(f"#### {max_week}")
    col6.write(f"#### {max_week_count}")
    #populating max day 
    max_day = day_grp.iloc[0,0] 
    max_day_count = day_grp.iloc[0,1]
    col7.write("#### Day")
    col7.write(f"#### {max_day}")
    col7.write(f"#### {max_day_count}")
    #populating max month
    max_hour = hour_grp.iloc[0,0] 
    max_hour_count = hour_grp.iloc[0,1]
    col8.write("#### Hour")
    col8.write(f"#### {max_hour}")
    col8.write(f"#### {max_hour_count}")
    
    #get the data grouped on hosts and months
    host_month_grp = group_two_col(cleaned_df,'host','month_name')
    #create the line chart based on above data
    st.dataframe(host_month_grp)
    pivot_hm_grp = pd.pivot(host_month_grp,index='month_name',
                            columns='host',values='src')
    st.dataframe(pivot_hm_grp)
    st.line_chart(pivot_hm_grp)
