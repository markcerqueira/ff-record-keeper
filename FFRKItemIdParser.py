# FFRKItemIdParser.py
# Author: Mark Cerqueira (www.mark.gg)
#
# Hosted at: https://github.com/markcerqueira/ff-record-keeper
# See sample JSON for parsing: https://github.com/markcerqueira/ff-record-keeper/blob/master/party-list.json
#
# Save the JSON text response from the dff/party/list API from FFRK
# and then run this program to print out the name, item ids, and rarity
#
# Usage: python FFRKItemIdParser.py JSON_FILE_NAME
#
# Example: python FFRKItemIdParse.py party-list.json > itemIds.csv
# This example reads data from party-list.json and ouputs the result to a file
# called itemIds.csv. You can then use Google Docs to convert CSV to another format
#
# NOTE: For equipment this outputs "base_rarity" and not "rarity." If you combine
# two one-star items, you get a two-star item. The "rarity" of this item is 2, but
# the "base_rarity" is 1. Gems only have "rarity" since you can't combine them.
#
# NOTE: Before sharing the output of this script with others, you should scrub out
# your user id using FFRKAnonymizer.py!

import sys
import json

# use a dictionary so we don't print multiple instances of an item mulitple times
item_dict = dict()


def get_equipment_id_from_json(data):
    result = ""

    # put equipment in the dictionary
    for equipment in data['equipments']:
        item_dict[equipment['name'].encode('utf8')] = [str(equipment['equipment_id']).encode('utf8'),
                                                       str(equipment['base_rarity']).encode('utf8')]

    # put materials in the dictionary
    for material in data['materials']:
        item_dict[material['name'].encode('utf8')] = [str(material['id']).encode('utf8'),
                                                      str(material['rarity']).encode('utf8')]

    # print out equipment/materials names to item ids and base_rarity
    for key in item_dict:
        result += key + ", " + str(item_dict[key][0]) + ", " + str(item_dict[key][1]) + "\n"

    return result


def main():
    with open(sys.argv[1]) as data_file:
        # load the JSON file
        data = json.load(data_file)
        get_equipment_id_from_json(data)


if __name__ == "__main__":
    main()
