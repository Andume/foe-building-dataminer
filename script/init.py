from natsort import natsorted
import requests
import json
import os
version = 'v26.04.23.1-beta' #Version number of the dataminer, used to check for updates. Format: v[YY].[MM].[DD]-[beta/release]
dir = os.path.dirname(__file__) #Get directory of the script to access local files
def checkForUpdates():
    print('Checking for updates...')
    latest_version = json.loads(requests.get('https://raw.githubusercontent.com/Andume/foe-building-dataminer/refs/heads/main/version.json').text) #Get latest version number from GitHub
    if version == latest_version['release'] or version == latest_version['beta']:
        print('The dataminer is up to data, continuing.')   #Continue if the version number of the dataminer matches the latest version number of main or beta branch
        pass
    else: 
        print('! A new version is available, please update.') #Notify user of available update
        userinput = input('! You are running an old version of the dataminer. Do you want to continue? Y/N: ') #Ask user if they want to continue using the old version
        if userinput.lower == 'y':
            print('WARNING: You are using an old version of the dataminer. Doing so may result in errors or inaccurate data. It is recommended to update to the latest version as soon as possible. Contine anyway? Y/N: ') #Warn user of possible errors and ask if they want to continue
            if userinput.lower == 'y':
                pass
            else:
                exit()
        else:
            exit()
def checkForNewBuildings():
    print('Checking for new buildings...')
    with open(rf'{dir}\data\building_urls.json') as f:
        building_urls_local = json.loads(f.read()) #Load local building_urls.json to get list of buildings
    for attempt in range(2): #Try to fetch data from API, if it fails retry once
        try:
            building_urls_api = json.loads(requests.get('https://foeus.innogamescdn.com/start/metadata?id=building_entity_lookup-a0a14de917fd7e558bcba01255d482f15c4b05cf').text) #Get list of buildings from FoE API to check for new buildings
            break
        except requests.exceptions.RequestException:
            if attempt == 0:
                print('Error fetching API data, trying again...') #Notify user of error and try again
            else:
                print('Update failed, continuing with existing data...') #Notify user of error after second failed attempt
                break
    for i in building_urls_api:
        if i['identifier'].replace('building_entity_','') not in building_urls_local:
            print(f'New building found ({i["identifier"].replace("building_entity_","")}), updating...') #Notify user of new building
            building_urls_local.update({i['identifier'].replace('building_entity_',''): { #Add new building to local building_urls.json
                'name': json.loads(requests.get(i['url']).text)['name'], #Get building name from FoE API using building url
                'id': i['identifier'].replace('building_entity_',''),
                'url': i['url']
            }})
    with open(rf'{dir}\data\building_urls.json', 'w') as f:
        json.dump(dict(natsorted(building_urls_local.items())), f, indent=4) #Write updated building list to local building_urls.json
    print('Building list is up to date.')