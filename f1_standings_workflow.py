import os
import requests
from datetime import datetime
from pyergast import pyergast
import pandas as pd
import json
import re

F1_NOTION_API_KEY= os.environ['F1_NOTION_API_KEY']
DRIVERS_DATABASE_KEY = os.environ['DRIVERS_DATABASE_KEY']

#F1_NOTION_API_KEY="secret_tSV9N1ab6tRQDiphT8ys2qmOYuwIF8EUdI9c0kA8Nel"
#DRIVERS_DATABASE_KEY ="c6f234cec054482fb15ccc8d423779d2"

def create_post_drivers_standings(driverID, position, positionText, points, wins, driver, nationality, constructor, constructorID):

    headers = {
        'Authorization': f"Bearer {F1_NOTION_API_KEY}",
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16',
    }
   
    data = { "parent": { "database_id": DRIVERS_DATABASE_KEY }, "properties": { 
        "driver":  {"title": [ { "text": { "content":  driver}} ] },
        "position": { "number": int(position)},
        "positionText":  {"rich_text": [{"text": {"content":  str(positionText)}}]},
        "points": { "number": float(points)},
        "wins": { "number": int(wins)},
        "driverID":  {"rich_text": [{"text": {"content": driverID}}]},
        "nationality": {"rich_text": [{"text": {"content": nationality}}]},
        "constructor":  {"rich_text": [{"text": {"content": constructor}}]},
        "constructorID":  {"rich_text": [{"text": {"content": constructorID}}]},
    },  }
        
    c=requests.post('https://api.notion.com/v1/pages', headers=headers, json=data)
    if c.status_code != 200:
        raise RuntimeError(c.content)
        print(data)
        #i=i+1

def get_drivers_standings():
    drivers_standings=pyergast.driver_standings()
    #drivers_standings = drivers_standings.astype({"nationality": str, "driver": str})
    for index, row  in drivers_standings.iterrows():
        create_post_drivers_standings(row.driverID, row.position, row.positionText, row.points, row.wins, row.driver, row.nationality, row.constructor, row.constructorID)
get_drivers_standings()

CONSTRUCTORS_DATABASE_KEY = os.environ['CONSTRUCTORS_DATABASE_KEY']
def create_post_constructors_standings(name, position, positionText, points, wins, nationality, constructorID):

    headers = {
        'Authorization': f"Bearer {F1_NOTION_API_KEY}",
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16',
    }
   
    data = { "parent": { "database_id": CONSTRUCTORS_DATABASE_KEY }, "properties": { 
        #"name":  {"title": [ { "text": { "content":  str(name)}} ] },
        "name":  {"title": [ { "text": { "content":  str(constructorID).title().replace("_"," ")}} ] },
        "position": { "number": int(position)},
        "positionText":  {"rich_text": [{"text": {"content":  str(positionText)}}]},
        "points": { "number": float(points)},
        "wins": { "number": int(wins)},
        "nationality": {"rich_text": [{"text": {"content": nationality}}]},
        "constructorID":  {"rich_text": [{"text": {"content": constructorID}}]},
    },  }
        
    c=requests.post('https://api.notion.com/v1/pages', headers=headers, json=data)
    if c.status_code != 200:
        raise RuntimeError(c.content)
        print(data)
        #i=i+1

def get_constructors_standings():
    constructors_standings=pyergast.constructor_standings()
    #drivers_standings = drivers_standings.astype({"nationality": str, "driver": str})
    for index, row  in constructors_standings.iterrows():
        create_post_constructors_standings(row.name, row.position, row.positionText, row.points, row.wins, row.nationality, row.constructorID)

get_constructors_standings()
#update
