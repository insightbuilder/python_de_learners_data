#!/usr/bin/env python
#Script creates the streamlit dashboard for the honeypot hackers data
import plotly.express as px
import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from cleaning_ds import clean_hackdata,group_by_col,group_two_col

#setting up the page config
st.set_page_config(page_title='Honeypot Dashboard',layout='wide')

#reading in the style sheet
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#lets fill in the overview of the data
st.markdown('## Honeypot Hacking Dashboard ')
st.markdown('##### Loading the 451K rows and 12 columns of data and cleaning it')
cleaned_df = clean_hackdata('hack_data.csv') 

#creating individual columns in streamlit
#st.write("### The visual overview who and what?")
host_grp = group_by_col(cleaned_df,'host')
country_grp = group_by_col(cleaned_df,"country")

#lets get some stacks going
country_hst_grp = group_two_col(cleaned_df,'host','country')
country_top_10 = list(country_grp['country'].values)
country_top_10 = country_top_10[:10] 

#st.write(country_top_10)
country_host_filter = country_hst_grp[country_hst_grp.country.isin(country_top_10)]
st.write("#### Which hosts the countries are attacking?")

#st.dataframe(country_host_filter)
fig_cnt_hst = px.bar(country_host_filter,x='host',y='src',color='country')
st.plotly_chart(fig_cnt_hst,use_container_width=True)

#how many incidents, how many hosts, how many attackers and how many countries
incidents = cleaned_df.shape[0]
hosts = len(cleaned_df.host.unique())
attackers = len(cleaned_df.srcstr.unique())
countries = len(cleaned_df.country.unique())
#filtering the top 10 countries
bar1, bar2 = st.columns(2)
bar1.write("#### Hosts attacked most")
bar1.bar_chart(host_grp,x='host',y='src')
bar2.write('#### Country attacking the most')
bar2.bar_chart(country_grp.iloc[:10,:],x='country',y='src')

#starting the overview
col1,col2,col3,col4 = st.columns(4)
col1.write("#### Incidents")
col1.write(f"#### {incidents}")
col2.write("#### Hosts")
col2.write(f"#### {hosts}")
col3.write("#### Attackers")
col3.write(f"#### {attackers}")
col4.write("#### Origin")
col4.write(f"#### {countries}")
st.write("#### Which hosts are most attacked?")

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
col5.write("#### Month")
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

#filter the data based on host. Group it based on week and make a bar chart
host_week_grp = group_two_col(cleaned_df, 'host','week_year')
host_week_filter = host_week_grp[host_week_grp.host == focus_host]   
st.write(f"#### Attacks per week on {focus_host}")
st.bar_chart(host_week_filter,x='week_year',y='src')

#get the data grouped on hosts and months
host_month_grp = group_two_col(cleaned_df,'host','month_name')
#create the line chart based on above data
pivot_hm_grp = pd.pivot(host_month_grp,index='month_name',
                        columns='host',values='src')
col9, col10 = st.columns(2)
col9.write('#### Pivoted DF')
col9.dataframe(pivot_hm_grp)
col10.write('#### Source DF')
col10.dataframe(host_month_grp)
st.write("#### Changes in the attack counts each month over the year")
st.line_chart(pivot_hm_grp)

st.write("### Thanks for viewing the dashboard")
#printing the dataframe
st.dataframe(cleaned_df)

