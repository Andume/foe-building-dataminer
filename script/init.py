import requests
import json
import os
version = '26.04.21.0'
dir = os.path.dirname(__file__)
def checkForUpdates():
    print('Checking for updates...')
    latest_version = json.loads(requests.get('https://raw.githubusercontent.com/Andume/foe-building-dataminer/refs/heads/main/version.json').text)
    if version == latest_version['main'] or version == latest_version['beta']:
        print('The dataminer is up to data, continuing.')
        pass
    else: 
        print('! A new version is available, please update.')
        userinput = input('! You are running an old version of the dataminer. Do you want to continue? Y/N: ')
        if userinput == 'Y' or 'y':
            pass
        else:
            exit()
def checkForNewBuildings():
    print('Checking for new buildings...')
    with open(rf'{dir}\data\building_urls.json') as f:
        building_urls_local = json.loads(f.read())
    building_urls_api = json.loads(requests.get('https://foeus.innogamescdn.com/start/metadata?id=building_entity_lookup-a0a14de917fd7e558bcba01255d482f15c4b05cf').text)
    for i in building_urls_api:
        if i['identifier'].replace('building_entity_','') not in building_urls_local:
            print('New building found! Updating...')
            print(i['identifier'].replace('building_entity_',''))
            building_urls_local.update({i['identifier']:{
                'name': json.loads(requests.get(i['url']).text)['name'],
                'id': i['identifier'],
                'url': i['url']
            }})
    print('Building list is up to date.')
