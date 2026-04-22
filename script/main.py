import init # type: ignore
import json
import os
import re
import requests
from process_data import listStats  # type: ignore
init.checkForUpdates() 
init.checkForNewBuildings()
dir = os.path.dirname(__file__) #Get directory of the script to access local files
def getBuildingId(building_name):
    with open(rf'{dir}\data\building_urls.json') as f:
        building_urls_local = json.loads(f.read()) #Load local building_urls.json to get building names/ids/urls
    building_id = next((k for k, v in building_urls_local.items() if v['name'] == building_name), None) #Get building id from building name
    return building_id
def getBuildingLevels(building_id):
    with open(rf'{dir}\data\building_urls.json') as f:
        building_urls_local = json.loads(f.read()) #Load local building_urls.json to get building names/ids/urls
    multilevel_building_id = re.sub(r"\d*?$", "", building_id) #Remove level number from building id to get multilevel building id (e.g. W_MultiAge_ANNI23A1 -> W_MultiAge_ANNI23A) to find all levels of the building
    building_ids = [] #Prepare list to store building ids of all levels of the building
    for keys in building_urls_local.keys():
        if keys.startswith(multilevel_building_id):
            building_ids.append(keys) #Add building id to list if it starts with the multilevel building id
    return building_ids
def getBuildingData(building_id):
    with open(rf'{dir}\data\building_urls.json') as f:
        building_urls_local = json.loads(f.read()) #Load local building_urls.json to get building names/ids/urls    
    return json.loads(requests.get(building_urls_local[building_id]['url']).text) #Retrieve building data from FoE API and return it as json
