import pandas as pd
import shutil
import warnings
warnings.filterwarnings('ignore')

get_file_name = input("Provide the data zip file full path: ")

shutil.unpack_archive(get_file_name)

honey_pot_data = pd.read_csv('AWS_Honeypot_marx-geo.csv')
null_filled_data = honey_pot_data.copy()
#filling the null values with unknown 
for col in ['type','country','cc','locale','localeabbr','postalcode']:
    null_filled_data[col].fillna('unknown',axis=0,inplace=True)
#filling the null values in case of floats with 0
for col_name in ['spt','dpt']:
    #null_filled_data.fillna(0,inplace=True,axis=0)
    null_filled_data[col_name].fillna(0,inplace=True,axis=0)
#dropping the column 
null_filled_data.drop('Unnamed: 15',inplace=True,axis=1)
#removing the rows that have any null values
null_filled_data.dropna(axis=0,inplace=True)
#writing out the file
out_file_name = input('Your data is ready. Provide fileName: ')
#writing the dataframe to file
null_filled_data.to_csv(out_file_name,index=False)


