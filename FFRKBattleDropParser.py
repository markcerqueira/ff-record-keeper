# FFRKBattleDropParser.py
# Author: Mark Cerqueira (www.mark.gg)
#
# Hosted at: https://github.com/markcerqueira/ff-record-keeper
# See sample JSON for parsing: https://gist.github.com/markcerqueira/59cf24051f0ca404f66c
#
# Save the JSON text response from the battle/get_battle_init_data API from FFRK
# and then run this program to print out a summary of items that will drop
#
# Usage: python FFRKItemDropParser.py JSON_FILE_NAME
#
# Example: python FFRKItemDropParser.py battle-data.json
# This example reads data from battle-data.json and ouputs drops that will occur
# at the end of each round (item type) and items that will drop when enemies are
# defeated (item_id)

import sys
import json

with open(sys.argv[1]) as data_file: 
    # load the JSON file  
    data = json.load(data_file)

    # load data for all rounds
    round_data = data['battle']['rounds']
    
    i = 1
    for round in round_data:
        # print the drop for the round (all enemies in round killed) if any
        for round_item_drop in round['drop_item_list']:
            print "Round " + str(i) + " - round drop type = " + str(round_item_drop.get('type'))

        # print drops for each enemy
        for enemy in round['enemy']:
            for enemy_child in enemy['children']:
                for enemy_child_drop in enemy_child['drop_item_list']:
                    if enemy_child_drop.get('item_id'):
                        if enemy_child_drop.get('type') == 51:
                            print "Round " + str(i) + " - enemy will drop ORB with id = " + str(enemy_child_drop.get('item_id'))
                        else:
                            print "Round " + str(i) + " - enemy will drop EQUIPMENT with id = " + str(enemy_child_drop.get('item_id'))
                    elif enemy_child_drop.get('amount'):
                        print "Round " + str(i) + " - enemy drop will drop GOLD amount = " + str(enemy_child_drop.get('amount'))

        i = i + 1