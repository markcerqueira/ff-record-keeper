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
