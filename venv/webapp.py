#Bonus exercise: write a Web Service
#Wrap the output of the second exercise in a web service that returns the data in JSON format
# (instead of printing to the standard output). The web service should accept a parameter n>0.
# For the top 10 airports, n is 10. For the X top airports, n is X.

#Note:
#Webapp implementation is done entirely using python with a help of a library known as PyWebIo

#About PyWebIo
#PyWebIO provides a series of imperative functions to obtain user input and output on the browser, turning the browser
# into a “rich text terminal”, and can be used to build simple web applications or browser-based GUI applications.
# Using PyWebIO, developers can write applications just like writing terminal scripts (interaction based on input and
# print), without the need to have knowledge of HTML and JS. PyWebIO can also be easily integrated into existing
# Web services. PyWebIO is very suitable for quickly building applications that do not require complex UI.

#It is highly recommend to run this file within its own virtual environment "venv" to avoid errors.

#Installation
#pip3 install -U pywebio

#Importing pywebio
from pywebio.input import*
from pywebio.output import*

#Importing other essential libraries
import pandas as pd
import ssl
import time
import os

#ssl certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

#amadeus logo url
put_image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Amadeus_%28CRS%29_Logo.svg/648px-Amadeus_%28CRS%29_Logo.svg.png")

#User input to fetch the desired number top airports
n= input("Enter the desired value of n-top airports",type=NUMBER)

#processbar to track the status
put_processbar("Please Wait",1,"Fetching the requested data...",True)

#process conformation message
put_text("Preparing the list of top %d airports based on arrival in 2013" %n)

#Reading the booking.csv file using pandas, ^ is used as a delimiter
df = pd.read_csv(r"/Users/jimharrington/Desktop/amadeus_assignment/data challenge/bookings.csv",error_bad_lines=False,
                sep = '^')

#Selcting records only from 2013
df=df[df['year']==2013.0]

#Aggregating the pax using Sum function and Groupby is used to group the sum function result on airport level granularity
top=df.groupby(['arr_port'])['pax'].sum()

#Sorting the values in descending order
top=top.sort_values(ascending=False)

#Selecting only top airports
top=top[:n]

#Converting the results into a data frame
df_top=top.to_frame()
df_top=df_top.reset_index()


#Changing column name from "arr_port" to "Code"
df_top=df_top.rename({'arr_port': 'Code'}, axis=1)

## Geo-location data URL
url="https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports-extended.dat"

##Fetching the data from Github, the header is set to none, and index column is set to 0
df_geo=pd.read_csv(url,error_bad_lines=False,header=None,index_col=0)

#Printing the column names
#print ("Columns names : ", df_geo.columns)

#Selecting only necessary columns
df_geo=df_geo.loc[:,[1,2,3,4]]

#Renaming the columns
df_geo=df_geo.rename({1: 'Airport Name', 2: 'City', 3:'Country', 4:'Code'}, axis=1)

#48 null values identified in city name, null values are dropped
df_geo=df_geo.dropna()

#Trimming the whitespace present in the code column of top10 dataframe
df_top['Code']=df_top['Code'].str.strip()

##The left joint is implemented on the df_top and df_geo using the merge function to retrieve the geo details of the top 10 airports
top_airports = pd.merge(df_top, df_geo,how="left", on=["Code", "Code"])

#saving the result as json
top_airports.to_json("top_airport_list.json")

#getting the file location
base_file=os.path.dirname(__file__)

#concardinating the file location and output file name
final_file =base_file + "/top_airport_list.json"

#success message
put_success("The requested list of the top %d airports is ready and saved in this file location"%n,final_file)


