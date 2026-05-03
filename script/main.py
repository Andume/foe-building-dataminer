import init # type: ignore
import json
import os
import re
import requests
from process_data import listStats  # type: ignore
import tkinter as tk
from tkinter import filedialog
init.checkForUpdates() 
init.checkForNewBuildings()
dir = os.path.dirname(__file__) #Get directory of the script to access local file
def getBuildingID(building_name):
    with open(rf'{dir}\data\building_urls.json') as f:
        building_urls_local = json.loads(f.read()) #Load local building_urls.json to get building names/ids/urls
    building_id = next((k for k, v in building_urls_local.items() if v['name'] == building_name), None) #Get building id from building name
    return building_id
def getBuildingLevels(building_id):
    with open(rf'{dir}\data\building_urls.json') as f:
        building_urls_local = json.loads(f.read()) #Load local building_urls.json to get building names/ids/urls
    multilevel_building_id = re.sub(r"\d*\D?$", "", building_id) #Remove level number from building id to get multilevel building id (e.g. W_MultiAge_ANNI23A1 -> W_MultiAge_ANNI23A) to find all levels of the building
    building_ids = [] #Prepare list to store building ids of all levels of the building
    for keys in building_urls_local.keys():
        if keys.startswith(multilevel_building_id):
            building_ids.append(keys) #Add building id to list if it starts with the multilevel building id
    return building_ids
def getBuildingData(building_id):
    with open(rf'{dir}\data\building_urls.json') as f:
        building_urls_local = json.loads(f.read()) #Load local building_urls.json to get building names/ids/urls    
    return json.loads(requests.get(building_urls_local[building_id]['url']).text) #Retrieve building data from FoE API and return it as json
while True:
    print('Please enter building information to retrieve data.')
    isMultilevel = input('Is the building multilevel? Y/N: ') #Ask user if the building is multilevel
    if isMultilevel.lower() == 'y':
        print('Please enter full name of any level of the building (e.g. Mk I Anomaly Extractor - Lv. 1): ') #Ask user for building name
        while True:
            userinput_building_name = input()
            if getBuildingID(userinput_building_name) != None: #If building name is valid, get building ID and break loop; if not, ask user to try again until a valid building name is entered.
                building_ID = getBuildingID(userinput_building_name)
                print('Building found, retrieving levels...')
                break
            else: print('Building not found, please try again.')
        building_IDs = getBuildingLevels(building_ID) #Get building IDs for all levels of the building using the building ID of the level entered by the user, and store them in a list
        print('Levels found, retrieving data...') #Notify user of success
    else:
        print('Please enter full name of the building (e.g. Vortex Arena): ') #Ask user for building name
        while True:
            userinput_building_name = input()
            if getBuildingID(userinput_building_name) != None: #If building name is valid, get building ID and break loop; if not, ask user to try again until a valid building name is entered.
                building_ID = getBuildingID(userinput_building_name)
                print('Building found, retrieving data...')
                break
            else: print('Building not found, please try again.')
        building_IDs = [building_ID] #If building is not multilevel, just put the single building ID in a list to be processed the same way as multilevel buildings
    building_data = {} #Initialize empty dict for building data
    for i in range(len(building_IDs)):
        building_data[i] = listStats(getBuildingData(building_IDs[i])) #Get building data for each level of the building and store it in a dictionary
    print('Data retrieved, please select a folder to save the data to.') #Notify user of success and ask them to select a folder to save the data
    root = tk.Tk()
    root.withdraw()
    save_file_path = filedialog.askdirectory() #Open file dialog to ask user to select a folder to save the data, and store the file path of the selected folder. If user cancels out of the file dialog, the file path will be an empty string.
    if save_file_path == '': #If file path is empty, user cancelled out of the file dialog, so exit the program.
        print('No folder selected, exiting program.')
        exit()
    print('Saving...')
    if isMultilevel.lower() == 'y': #If building is multilevel, save data in a file named after the building without the level number (e.g. W_MultiAge_ANNI23A.json); if building is not multilevel, save data in a file named after the full building ID.
        while True:
            try:
                with open(f'{save_file_path}/{re.sub(r"\d*\D?$", "", building_ID)}.json', 'x') as f:
                    f.write(json.dumps(building_data, indent=2))
            except FileExistsError: #If a file with the same name already exists in the selected folder, add a number in parentheses to the end of the file name to distinguish it from the existing file (e.g. W_MultiAge_ANNI26A(1).json, W_MultiAge_ANNI26A(2).json, etc.). If files with the same name and a number in parentheses already exist, keep increasing the number until a unique file name is found.
                attempt = 1
                while True:
                    try:
                        with open(f'{save_file_path}/{re.sub(r"\d*\D?$", "", building_ID)}({attempt}).json', 'x') as f:
                            f.write(json.dumps(building_data, indent=2))
                        break
                    except FileExistsError:
                        attempt += 1
                        pass
            break
    else:
        while True:
            try:
                with open(f'{save_file_path}/{building_ID}.json', 'x') as f:
                    f.write(json.dumps(building_data, indent=2))
            except FileExistsError: #If a file with the same name already exists in the selected folder, add a number in parentheses to the end of the file name to distinguish it from the existing file (e.g. W_MultiAge_ANNI26D1(1).json, W_MultiAge_ANNI26D1(2).json, etc.). If files with the same name and a number in parentheses already exist, keep increasing the number until a unique file name is found.
                attempt = 1
                while True:
                    try:
                        with open(f'{save_file_path}/{building_ID}({attempt}).json', 'x') as f:
                            f.write(json.dumps(building_data, indent=2))
                        break
                    except FileExistsError:
                        attempt += 1
                        pass
            break
    print('Saved.')
    if input('Do you want to get data for another building? Y/N: ').lower() == 'n': #Ask user if they want to get data for another building; if not, exit the program; if yes, repeat the process.
        break