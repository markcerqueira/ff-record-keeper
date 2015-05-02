# Utils.py
# Author: Mark Cerqueira (www.mark.gg)
#
# Hosted at: https://github.com/markcerqueira/ff-record-keeper
#
# Shared utility methods used by the various FFRK scripts

import os
import csv
import json
import time

ITEM_ID_WEAPON_PREFIX = '21'
ITEM_ID_ARMOR_PREFIX = '22'
ITEM_ID_ACCESSORY_PREFIX = '23'
ITEM_ID_ORB_PREFIX = '40'

# return the suffix that will be appended to anonymized files (e.g. "-1429807698")
def get_suffix_with_unix_time():
    return "-" + get_unix_time_str();


# return unix time as string
def get_unix_time_str():
    return str(int(time.time()))


# if a file with filename does not exists, creates that file and dumps json_data to it
def dump_json_to_file(json_data, filename):
    filename = clean_up_filename(filename)

    if not os.path.isfile(filename):
        with open(filename, 'w') as outfile:
            json.dump(json_data, outfile, sort_keys=False, indent=4)


# ensures .json is the file name extension
def clean_up_filename(filename):
    if '.json' in filename and not filename.endswith('.json'):
        filename = filename.replace('.json', '')

    if not filename.endswith('.json'):
        filename += '.json'

    return filename


# helper method for get_description_for_item_id below
def get_description_for_item_id_with_csv_file(item_id, file, item_type_prefix):
    csv_file = csv.reader(file)
    for row in csv_file:
        if str(row[1]) == item_id:
            return item_type_prefix + ": " + row[0] + ", rarity = " + str(row[2]) + "*, id = " + str(item_id)

    return "Unknown " + item_type_prefix + " with id = " + str(item_id)


# returns a string describing the item with id item_id
def get_description_for_item_id(item_id):
    if item_id.startswith(ITEM_ID_WEAPON_PREFIX):
        return get_description_for_item_id_with_csv_file(item_id, open('data/weapons.csv'), "WEAPON")
    elif item_id.startswith(ITEM_ID_ARMOR_PREFIX):
        return get_description_for_item_id_with_csv_file(item_id, open('data/armor.csv'), "ARMOR")
    elif item_id.startswith(ITEM_ID_ACCESSORY_PREFIX):
        return get_description_for_item_id_with_csv_file(item_id, open('data/accessories.csv'), "ACCESSORY")
    elif item_id.startswith(ITEM_ID_ORB_PREFIX):
        return get_description_for_item_id_with_csv_file(item_id, open('data/orbs.csv'), "ORB")
    else:
        return "Unknown prefix for item id = " + str(item_id)


# runs some tests on get_description_for_item_id
def test_get_description_for_item_id():
    # standard tests on each CSV file for item ids that are present
    print get_description_for_item_id(str(21002002))  # WEAPON: Iron Sword (XII), rarity = 2*, id = 21002002
    print get_description_for_item_id(str(23080016))  # ACCESSORY: Sniper Eye (VI), rarity = 1*, id = 23080016
    print get_description_for_item_id(str(22056004))  # ARMOR: Carbon Bangle (VII), rarity = 2*, id = 22056004
    print get_description_for_item_id(str(40000014))  # ORB: Greater Black Orb, rarity = 4*, id = 40000014

    # test when an item id does not exist in the respective CSV file
    print get_description_for_item_id(str(22000000))  # Unknown ARMOR with id = 22000000

    # test when we get an unknown prefix
    print get_description_for_item_id(str(32000000))  # Unknown prefix for item id = 32000000


if __name__ == "__main__":
    test_get_description_for_item_id()
