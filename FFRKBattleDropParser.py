# FFRKBattleDropParser.py
# Author: Mark Cerqueira (www.mark.gg)
#
# Hosted at: https://github.com/markcerqueira/ff-record-keeper
# See sample JSON for parsing: https://github.com/markcerqueira/ff-record-keeper/blob/master/battle-data.json
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
#
# NOTE: Before sharing the output of this script with others, you should scrub out
# your user id using FFRKAnonymizer.py!

import sys
import json

from Utils import get_description_for_item_id

def print_drops_from_json(data):
    # load data for all rounds
    all_rounds_data = data['battle']['rounds']

    i = 1
    for round_data in all_rounds_data:
        # print the drop for the round (all enemies in round killed) if any
        for round_item_drop in round_data['drop_item_list']:
            print "Round " + str(i) + " - round drop type = " + str(round_item_drop.get('type'))

        # print drops for each enemy
        for enemy in round_data['enemy']:
            for enemy_child in enemy['children']:
                for enemy_child_drop in enemy_child['drop_item_list']:
                    if enemy_child_drop.get('item_id'):
                        print "Round " + str(i) + " - enemy will drop " + get_description_for_item_id(enemy_child_drop.get('item_id'))
                    elif enemy_child_drop.get('amount'):
                        print "Round " + str(i) + " - enemy will drop GOLD amount = " + str(enemy_child_drop.get('amount'))

        i += 1


def main():
    with open(sys.argv[1]) as data_file:
        # load the JSON file
        data = json.load(data_file)
        print_drops_from_json(data)


if __name__ == "__main__":
    main()
