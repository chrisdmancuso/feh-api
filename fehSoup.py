from bs4 import BeautifulSoup
import requests
from fastapi import FastAPI
from typing import List
from uuid import uuid4
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as fdb
import json

#Read tokens from file for db auth
tokens = []
with open('tokens.txt', 'r') as f:
    while True:
        line = f.readline().strip('\n')
        tokens.append(line)
        if not line:
            break
        
#Setup db connection and web scraping        
cred_obj = credentials.Certificate(tokens[0])
firebase_admin.initialize_app(cred_obj, {
    'databaseURL': tokens[1]
    })
ref = fdb.reference("/")
ref.set({
    "Data": {
        "Units": -1
        }
    })
ref.update({
        "Skills": {
            "Units": -1
            }
        })
source = requests.get('https://feheroes.fandom.com/wiki/Level_40_stats_table').text
soup = BeautifulSoup(source, 'lxml')
source2 = requests.get('https://feheroes.fandom.com/wiki/Hero_skills_table').text
soup2 = BeautifulSoup(source2, 'lxml')
tbody = soup.find('tbody')
tbody2 = soup2.find('tbody')
tr = tbody.find_all('tr', class_='hero-filter-element')
tr2 = tbody2.find_all('tr', class_='hero-filter-element')
#then create a new ref('Skills/Units'), then commit like below for skills,
#then create api for grabbing a units skills
for unit in tr2:
    result_dict2 = {}
    all_td2 = unit.find_all('td')
    ref = fdb.reference(f"/Skills/Units/{all_td2[0].a['title']}")
    weapons = all_td2[4].find_all('a')
    
    temp_dict2 = {'Name': all_td2[0].a['title']}
    for i, v  in enumerate(weapons):
        temp_dict2.update({f'Weapon {i+1}': v['title']})
    temp_dict2.update({'Assist': all_td2[5].text})
    temp_dict2.update({'Special': all_td2[6].text})
    temp_dict2.update({'A-Skill': all_td2[7].text})
    temp_dict2.update({'B-Skill': all_td2[8].text})
    temp_dict2.update({'C-Skill': all_td2[9].text})
    result_dict2.update({all_td2[0].a['title']: temp_dict2})
    ref.update(result_dict2)
    
#Commit data to db
for unit in tr:
    result_dict = {}
    all_td = unit.find_all('td')
    ref = fdb.reference(f"/Data/Units/{all_td[0].a['title']}")
    
    temp_dict = {'Name': all_td[0].a['title']}
    temp_dict.update({'Game': all_td[2].img['alt']})
    temp_dict.update({'Move Type': all_td[3].img['alt']})
    temp_dict.update({'Weapon Type': all_td[4].img['alt']})
    temp_dict.update({'HP': all_td[5].text})
    temp_dict.update({'ATK': all_td[6].text})
    temp_dict.update({'SPD': all_td[7].text})
    temp_dict.update({'DEF': all_td[8].text})
    temp_dict.update({'RES': all_td[9].text})
    temp_dict.update({'BST': all_td[10].text})
    
    result_dict.update({all_td[0].a['title']: temp_dict})
    
    ref.update(result_dict)
