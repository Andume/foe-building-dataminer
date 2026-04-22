import json
import os
from natsort import natsorted
dir = os.path.dirname(__file__)
with open(fr'{dir}\data\special_grouped.json') as f:
    building_data = json.loads(f.read())
def listStats(building):
    building_stats = {}
    def listProducts(path):
        product_list = {}
        if path['type'] == 'resources':
            for p in path['playerResources']['resources']:
                product_list[p] = path['playerResources']['resources'][p]
        if path['type'] == 'guildResources':
            for p in path['guildResources']['resources']:
                product_list['guild_'+str(p)] = path['guildResources']['resources'][p]
        if path['type'] == 'genericReward':
            rewardID = path['reward']['id']
            product_list[('genericReward'+str(o))] = building['components'][i]['lookup']['rewards'][rewardID]['name']
        return product_list
    for i in building['components']:
        building_stats[i] = {'passive': {}, 'production': {}}
        if 'ally' in building['components'][i]:
            building_stats[i]['passive']['ally'] = building['components'][i]['ally']['rooms'][0]['allyType']
        if 'staticResources' in building['components'][i]:
            building_stats[i]['passive']['population'] = building['components'][i]['staticResources']['resources']['resources']['population']
        if 'happiness' in building['components'][i] and 'provided' in building['components'][i]['happiness']:
            building_stats[i]['passive']['happiness'] = building['components'][i]['happiness']['provided'] 
        if 'boosts' in building['components'][i]:
            if 'boosts' not in building_stats[i]['passive']:
                building_stats[i]['passive']['boosts'] = {}
            for o in range(len(building['components'][i]['boosts']['boosts'])):
                building_stats[i]['passive']['boosts'][building['components'][i]['boosts']['boosts'][o]['targetedFeature'] + '_' + building['components'][i]['boosts']['boosts'][o]['type']] = building['components'][i]['boosts']['boosts'][o]['value']
        if 'production' in building['components'][i]:
            for u in range(len(building['components'][i]['production']['options'])):
                if ('option ' + str(u)) not in building_stats[i]['production']:
                    building_stats[i]['production']['option ' + str(u)] = {'always':{'normal':{},'random':{}},'onlyWhenMotivated':{'normal':{},'random':{}}}
                building_stats[i]['production']['option ' + str(u)]['time'] = building['components'][i]['production']['options'][u]['time']
                for o in range(len(building['components'][i]['production']['options'][u]['products'])):
                    if 'onlyWhenMotivated' in building['components'][i]['production']['options'][u]['products'][o] and building['components'][i]['production']['options'][u]['products'][o]['onlyWhenMotivated'] == True:
                        whenProduced = 'onlyWhenMotivated'
                    else:
                        whenProduced = 'always'
                    if building['components'][i]['production']['options'][u]['products'][o]['type'] == 'resources':
                        building_stats[i]['production']['option ' + str(u)][whenProduced]['normal'].update(listProducts(building['components'][i]['production']['options'][u]['products'][o]))
                    if building['components'][i]['production']['options'][u]['products'][o]['type'] == 'guildResources':
                        building_stats[i]['production']['option ' + str(u)][whenProduced]['normal'].update(listProducts(building['components'][i]['production']['options'][u]['products'][o]))
                    if building['components'][i]['production']['options'][u]['products'][o]['type'] == 'genericReward':
                        building_stats[i]['production']['option ' + str(u)][whenProduced]['normal'].update(listProducts(building['components'][i]['production']['options'][u]['products'][o]))
                    if building['components'][i]['production']['options'][u]['products'][o]['type'] == 'random':
                        for p in range(len(building['components'][i]['production']['options'][u]['products'][o]['products'])):
                            building_stats[i]['production']['option ' + str(u)][whenProduced]['random'][p] = {'dropChance':building['components'][i]['production']['options'][u]['products'][o]['products'][p]['dropChance'],'product':listProducts(building['components'][i]['production']['options'][u]['products'][o]['products'][p]['product'])}
    return building_stats
def listMultilevelStats(id):
    building_stats = {}
    for i in building_data[id]:
        building_stats[i] = listStats(building_data[id][i])
    building_stats = dict(natsorted(building_stats.items()))
    return building_stats
