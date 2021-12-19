import pandas as pd
from zipfile import ZipFile
from urllib.request import urlopen   
import pandas as pd
import os

URL = 'http://ergast.com/downloads/f1db_csv.zip'

# open and save the zip file onto computer
url = urlopen(URL)
output = open('f1db_csv.zip', 'wb')    # note the flag:  "wb"        
output.write(url.read())
output.close()

circuits=pd.read_csv('f1db_csv.zip/circuits.csv')
races=pd.read_csv('f1db_csv.zip/races.csv')
constructors=pd.read_csv('f1db_csv.zip/constructors.csv')
drivers=pd.read_csv('f1db_csv.zip/drivers.csv')
seasons=pd.read_csv('f1db_csv.zip/seasons.csv')
status=pd.read_csv('status.csv')
