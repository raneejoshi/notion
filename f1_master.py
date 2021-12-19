import pandas as pd
from zipfile import ZipFile
from urllib.request import urlopen   
import pandas as pd
import os

URL = \
    'http://ergast.com/downloads/f1db_csv.zip'

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

qualifying=pd.read_csv('qualifying.csv')
qualifying = qualifying[qualifying['qualifyId']>qualifying_rowid]
qualifying.insert(0, column = "DB", value = "Qualifying") 

results=pd.read_csv('results.csv')
results = results[results['resultId']>results_rowid]
results.insert(0, column = "DB", value = "Driver Results")  

constructor_results=pd.read_csv('constructor_results.csv')
constructor_results = constructor_results[constructor_results['constructorResultsId']>constructor_results_rowid]
constructor_results.insert(0, column = "DB", value = "Constructor Results")  

constructor_standings=pd.read_csv('constructor_standings.csv')
constructor_standings = constructor_standings[constructor_standings['constructorStandingsId']>constructor_standings_rowid]
constructor_standings.insert(0, column = "DB", value = "Constructor Standings")  

driver_standings=pd.read_csv('driver_standings.csv')
driver_standings = driver_standings[driver_standings['driverStandingsId']>driver_standings_rowid]
driver_standings.insert(0, column = "DB", value = "Driver Standings")  

pit_stops=pd.read_csv('pit_stops.csv')
pit_stops = pit_stops[pit_stops['raceId']>pit_stops_raceid]
pit_stops.insert(0, column = "DB", value = "Pitstops")  


lap_times=pd.read_csv('lap_times.csv')
lap_times = lap_times[lap_times['raceId']>lap_times_raceid]
lap_times.insert(0, column = "DB", value = "Lap Time")  

file= pd.concat([constructor_results, constructor_standings])
file = pd.merge(file, races, on ='raceId', how ='left')
file = pd.merge(file, constructors, on ='constructorId', how ='left')
file["Name"] = file["name_x"] + str(" - ") + file.raceId.astype(str)

file2= pd.concat([qualifying, results, driver_standings,lap_times])
file2 = pd.merge(file2, races, on ='raceId', how ='left')
file2 = pd.merge(file2, constructors, on ='constructorId', how ='left')
file2 = pd.merge(file2, drivers, on ='driverId', how ='left')
file2["Driver"] = file2["forename"] + " " + file2["surname"]
file2["Name"] = file2["Driver"] + str(" - ") + file2.raceId.astype(str)

file3= pd.merge(pit_stops, races, on ='raceId', how ='left')
file3 = pd.merge(file3, drivers, on ='driverId', how ='left')
file3["Driver"] = file3["forename"] + " " + file3["surname"]
file3["Name"] = file3.time_x.astype(str)
file3 = file3.rename(columns={'name': 'name_x'})

import_file= pd.concat([file,file2,file3])
import_file = pd.merge(import_file, status, on ='statusId', how ='left')
import_file = import_file[['Name',
'DB',
'constructorId',
'name_y',
'driverId',
'Driver',
'raceId',
'name_x',
'duration',
'lap',
'milliseconds',
'points',
'status_y',
'stop',
'time',
'constructorResultsId',
'number',
'position',
'positionText',
'wins',   
'constructorStandingsId',
'q1',
'q2',
'q3',
'qualifyId',
'fastestLap',
'fastestLapSpeed',
'fastestLapTime',
'grid',
'laps',
'positionOrder',
'rank',
'driverStandingsId',
'resultId',
'statusId']]

import_file = import_file.rename(columns={'name_y':'Constructor',
'Driver':'Driver',
'duration':'Duration',
'fastestLap':'FastestLap',
'fastestLapSpeed':'FastestLapSpeed',
'fastestLapTime':'FastestLapTime',
'grid':'Grid',
'lap':'Lap',
'laps':'Laps',
'milliseconds':'Milliseconds',
'number':'Number',
'points':'Points',
'position':'Position',
'positionOrder':'PositionOrder',
'positionText':'PositionText',
'name_x':'Race',
'rank':'Rank',
'status_y':'Status',
'stop':'Stop',
'time':'Time',
'wins':'Wins'})

import_file.head()

print("qualifyId= ", qualifying_rowcount+len(qualifying.index), "\n"
      "resultId= ", results_rowcount+len(results.index), "\n"
      "constructorResultsId= ", constructor_results_rowcount+len(constructor_results.index), "\n"
      "constructorStandingsId= ", constructor_standings_rowcount+len(constructor_standings.index), "\n"
      "driverStandingsId= ", driver_standings_rowcount+len(driver_standings.index), "\n"
      "Pitstops= ", pit_stops_rowcount+ len(pit_stops.index), "\n"
      "Lap Time= ", lap_times_rowcount+len(lap_times.index))

print("qualifyId= ", import_file['qualifyId'].max(), "\n"
      "resultId= ", import_file["resultId"].max(), "\n"
      "constructorResultsId= ", import_file["constructorResultsId"].max(), "\n"
      "constructorStandingsId= ", import_file["constructorStandingsId"].max(), "\n"
      "driverStandingsId= ", import_file["driverStandingsId"].max(), "\n"
      "Pitstops= ", import_file["raceId"].max(), "\n"
      "Lap Time= ", import_file["raceId"].max())
