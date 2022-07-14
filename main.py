from fastapi import FastAPI, Path, Query, HTTPException, status
from fastapi.routing import APIRoute
from starlette.responses import RedirectResponse
from typing import Union
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as fdb

app = FastAPI()
tokens = []
with open('tokens.txt', 'r') as f:
    while True:
        line = f.readline().strip('\n')
        tokens.append(line)
        if not line:
            break
    
cred_obj = credentials.Certificate(tokens[0])
firebase_admin.initialize_app(cred_obj, {
    'databaseURL': tokens[1]
    })

ref = fdb.reference("/Data/Units")
ref2 = fdb.reference("/Skills/Units")

name_ref =  ref.order_by_child('name').get()
skill_ref = ref2.order_by_child('name').get()

game_titles = [
    "Path of Radiance",
    "The Blazing Blade",
    "Awakening",
    "Radiant Dawn",
    "Thracia 776",
    "Tokyo Mirage Sessions ♯FE Encore",
    "Echoes",
    "Heroes",
    "Genealogy of the Holy War",
    "Shadow Dragon / (New) Mystery",
    "The Binding Blade",
    "Three Houses",
    "Fates",
    "The Sacred Stones"
  ]

@app.get("/")
async def root():
    response = RedirectResponse(url="/docs")
    return response

#Unit Names
@app.get("/api/v1/units/names/")
async def fetch_all_unit_names(unit_name: Union[str, None]=Query(default=None, description="Filter results by starting letter, or by unit name. Example, 'Alm' will return all units that start with 'Alm'")):
    results_list = []
    try:
        unit_name = re.sub(r'[^a-zA-Z0-9:]', ' ', unit_name).strip()
    except:
        pass
    for key, value in name_ref.items():
        if unit_name is not None:
            if key[0].lower() == unit_name[0].lower() and key.lower().find(unit_name.lower()) != -1:
                results_list.append(key)
                
        else:
            results_list.append(key)
    results_dict = {0: results_list}
    return results_dict

#Unit Stats
@app.get("/api/v1/units/detailed")
async def fetch_all_units_detailed():
    """
    **Description**: Will return all detailed units. May be slow to load and cause the API to be less responsive.
    """
    return name_ref

@app.get("/api/v1/units/detailed/{unit_name}")
async def fetch_units_detailed(unit_name: str=Path(default=None, description="""Retrieve detailed stats of a unit. Example, 'Abel: The Panther'"""
                                                   """ returns stats of the given unit. Run 'fetch_all_unit_names' to fetch all unit names. Is case sensitive, and must match exactly""")):
    unit_name = re.sub(r'[^a-zA-Z0-9:]', ' ', unit_name).strip()
    try:
        ref = fdb.reference(f"/Data/Units/{unit_name}")
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) 
    return ref.get()

#Skills
@app.get("/api/v1/units/skills")
async def fetch_all_units_skills():
    """
    **Description**: Will return all default skills of all units. May be slow to load and cause the API to be less responsive.
    """
    return skill_ref

@app.get("/api/v1/units/skills/{unit_name}")
async def fetch_units_skills(unit_name: str=Path(default=None, description="""Retrieve detailed stats and skills of a unit. Example, 'Abel: The Panther'"""
                                                 """ returns stats and skills of the given unit. Run 'fetch_all_unit_names' to fetch all unit names. Is case sensitive, and must match exactly""")):
    unit_name = re.sub(r'[^a-zA-Z0-9:]', ' ', unit_name).strip()
    try:
        unit_ref = fdb.reference(f"/Data/Units/{unit_name}")
        data = unit_ref.get()
        unit_skill_ref = fdb.reference(f"/Skills/Units/{unit_name}")
        skills = unit_skill_ref.get()
        result = skills[unit_name] | data[unit_name]
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) 
    return result

#Game
@app.get("/api/v1/games/titles")
async def fetch_all_game_names():
    """
    **Description**: Return all game titles.
    """   
    return {0: game_titles}

@app.get("/api/v1/units/games/")
async def fetch_all_units_by_game(game_name: str=Query(default=None, description="""Filter results by game name. Example, 'Shadow Dragon /"""
                                                                    """ (New) Mystery' will return all units that appear in 'Shadow Dragon / (New) Mystery'. Run 'fetch_all_game_names' to fetch all valid game titles. NOTE, """
                                                                    """ Case is ignored, as are all non alpha characters. Example, 'sHaDoWdragonnewMYSTERY' will produce the same output as 'Shadow Dragon / (New) Mystery'""")):
    if game_name == None:
        return {"Need help? Use 'fetch_all_game_names'": 'Example input: The Sacred Stones'}
    results_list = []
    for key, value in name_ref.items():
        if re.sub(r'[^a-zA-Z0-9]', '', value.get(key).get('Game').lower()) == re.sub(r'[^a-zA-Z0-9]', '', game_name.lower()):
            results_list.append(key)
    results_dict = {0: results_list}
    return results_dict

