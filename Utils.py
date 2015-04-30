# Utils.py
# Author: Mark Cerqueira (www.mark.gg)
#
# Hosted at: https://github.com/markcerqueira/ff-record-keeper
#
# Shared utility methods used by the various FFRK scripts

import os
import json
import time

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
