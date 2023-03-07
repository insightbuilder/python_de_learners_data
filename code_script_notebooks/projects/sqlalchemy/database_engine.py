#!/usr/bin/env python
import pandas as pd
import sqlite3

def load_data(database_loc, data_file,table_name):
    """Database located at best in the same location as the file.
    When the data is provided, ensure the full path is provided.
    The table with the given name will be created."""
    conn = sqlite3.connect(database_loc)
    dataframe = pd.read_csv(data_file)
    dataframe.drop('Unnamed: 0',axis=1,inplace=True)
    dataframe.to_sql(table_name, conn, if_exists='append',index=True)
    print(f'Data uploaded into {database_loc}')

db_loc = 'trial_data.db'
data_loc = '~/sample_data.csv'
table_name = 'hack_data'

load_data(db_loc,data_loc,table_name)
