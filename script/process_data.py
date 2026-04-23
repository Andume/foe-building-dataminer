import json
import os
dir = os.path.dirname(__file__) #Get directory of the script to access local files
def listStats(building):
    building_stats = {'name': building['name']} #Initialize empty dict to store building stats
    def listProducts(path): #Convert 'products' json object into a more readable dict with product names and amounts
        product_list = {} #Initialize empty dict to store products
        if path['type'] == 'resources': #Check product type; if 'type' = 'resources', product can be added to list normally
            for p in path['playerResources']['resources']: #Iterate through all products in 'resources' and add them to the list
                product_list[p] = path['playerResources']['resources'][p] #Add product to list with name as key and amount as value
        if path['type'] == 'guildResources': #If 'type' = 'guildResources', product must be added with 'guild_' prefix to distinguish guild resources from normal resources
            for p in path['guildResources']['resources']: #Iterate through all products in 'guildResources' and add them to the list with 'guild_' prefix
                product_list['guild_'+str(p)] = path['guildResources']['resources'][p] #Add product to list with 'guild_' prefix, name as key, and amount as value
        if path['type'] == 'genericReward': #If 'type' = 'genericReward', product must be added with rewardID as key and reward description as value, since the 'products' object only contains a rewardID and not the actual product name or amount. Amount produced is stated in reward description, so no need to add amount to the list.
            rewardID = path['reward']['id'] #Get rewardID from 'products' object
            product_list[rewardID] = building['components'][i]['lookup']['rewards'][rewardID]['name'] #Add product to list with rewardID as key and reward description as value by looking up rewardID in building 'lookup' object, which contains the reward descriptions. 
        return product_list #Return list of products with product names as keys and amounts (or reward descriptions) as values
    for i in building['components']: #Component keys are the building ages, so iterate through all ages of the building to get all stats for the building
        building_stats[i] = {'passive': {}, 'production': {}} #Initialize dict for the current age with 'passive' and 'production' subdicts to store passive and production stats, respectively
        if 'ally' in building['components'][i]: #If building can house an ally, add ally type to the list of passive stats for the building
            building_stats[i]['passive']['ally'] = building['components'][i]['ally']['rooms'][0]['allyType'] #Add ally type to passive stats with key 'ally' and value ally type, which is found in the 'ally' object of the building component for the current age. The 'rooms' array contains objects for each room in the building, but currently all buildings with allies only have one room, so we can just look at the first element of the 'rooms' array to get the ally type. Also, since there is currently only one ally type, the value will always be 'military', but this code will still work if new ally types are added in the future.
        if 'staticResources' in building['components'][i]: #If building provides staticResources, add to list of passive stats for the building
            building_stats[i]['passive']['population'] = building['components'][i]['staticResources']['resources']['resources']['population'] #Currently, the only static resource provided by buildings is population, so we can just add the population amount to the passive stats with key 'population' and value equal to the population amount found in the 'staticResources' object of the building component for the current age. This code will need to be updated if new types of static resources are added in the future.
        if 'happiness' in building['components'][i] and 'provided' in building['components'][i]['happiness']: #If building provides happiness, add to list of passive stats for the building
            building_stats[i]['passive']['happiness'] = building['components'][i]['happiness']['provided'] #Add happiness amount to passive stats with key 'happiness' and value equal to the happiness amount found in the 'happiness' object of the building component for the current age. Happiness provided can be a positive or negative number, so this code will work for both happiness-providing and happiness-reducing buildings.
        if 'boosts' in building['components'][i]: #If building has boosts, add to list of passive stats for the building
            if 'boosts' not in building_stats[i]['passive']: #If the passive stats for the building does not already have a 'boosts' object, create an empty 'boosts' object in the passive stats to store the building boosts
                building_stats[i]['passive']['boosts'] = {} #Initialize empty 'boosts' object
            for o in range(len(building['components'][i]['boosts']['boosts'])): #Iterate through all boosts provided by the building
                building_stats[i]['passive']['boosts'][building['components'][i]['boosts']['boosts'][o]['targetedFeature'] + '_' + building['components'][i]['boosts']['boosts'][o]['type']] = building['components'][i]['boosts']['boosts'][o]['value'] #Add boost to passive stats with key as the boost target and type (e.g. 'all_forge_points_production' or 'guild_raids_att_def_boost_attacker_defender') and value as the boost amount found in the 'boosts' object for the current age. This code will work for any type of boost, such as production boosts or military boosts, as it just uses the targeted feature and type to create the key for the boost in the passive stats.
        if 'production' in building['components'][i]: #If building has productions, add to list of production stats for the building
            for u in range(len(building['components'][i]['production']['options'])): #Iterate through all production options for the building to get all production stats for the building. If the building has only one production option, it will be listed as option 0.
                if ('option ' + str(u)) not in building_stats[i]['production']: #Check if object for the cu
                    building_stats[i]['production']['option ' + str(u)] = {'always':{'normal':{'player':{},'guild':{}},'random':{'player':{},'guild':{}}},'onlyWhenMotivated':{'normal':{'player':{},'guild':{}},'random':{'player':{},'guild':{}}}} #If not, create it with subobjects for 'always' and 'onlyWhenMotivated' products, which each have 'normal' and 'random' subobjects to store the normal and random products for the production option, respectively. 
                building_stats[i]['production']['option ' + str(u)]['time'] = building['components'][i]['production']['options'][u]['time'] #Add production time for the production option to the production stats with key 'time' and value equal to the production time in seconds
                for o in range(len(building['components'][i]['production']['options'][u]['products'])): #Iterate through all products
                    if 'onlyWhenMotivated' in building['components'][i]['production']['options'][u]['products'][o] and building['components'][i]['production']['options'][u]['products'][o]['onlyWhenMotivated'] == True: #Check if product is only produced when the building is motivated
                        whenProduced = 'onlyWhenMotivated'
                    else:
                        whenProduced = 'always'
                    #Check product type and add products to production stats accordingly, using listProducts.
                    if building['components'][i]['production']['options'][u]['products'][o]['type'] == 'resources': 
                        building_stats[i]['production']['option ' + str(u)][whenProduced]['normal']['player'].update(listProducts(building['components'][i]['production']['options'][u]['products'][o]))
                    if building['components'][i]['production']['options'][u]['products'][o]['type'] == 'guildResources':
                        building_stats[i]['production']['option ' + str(u)][whenProduced]['normal']['guild'].update(listProducts(building['components'][i]['production']['options'][u]['products'][o]))
                    if building['components'][i]['production']['options'][u]['products'][o]['type'] == 'genericReward':
                        building_stats[i]['production']['option ' + str(u)][whenProduced]['normal']['player'].update(listProducts(building['components'][i]['production']['options'][u]['products'][o]))
                    if building['components'][i]['production']['options'][u]['products'][o]['type'] == 'random': #Check if product type is 'random'; random products are handled differently
                        for p in range(len(building['components'][i]['production']['options'][u]['products'][o]['products'])): #Iterate through all random products 
                            building_stats[i]['production']['option ' + str(u)][whenProduced]['random'][p] = {'dropChance':building['components'][i]['production']['options'][u]['products'][o]['products'][p]['dropChance'],'product':listProducts(building['components'][i]['production']['options'][u]['products'][o]['products'][p]['product'])} #Add random product to production stats, as a dictionary which includes product and drop chance.
    return building_stats