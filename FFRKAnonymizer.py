# FFRKAnonymizer.py
# Author: Mark Cerqueira (www.mark.gg)
#
# Hosted at: https://github.com/markcerqueira/ff-record-keeper
#
# Currently supported API responses for anonymizing:
#   * dff/party/list
#   * battle/get_battle_init_data
#
# Usage: python FFRKAnonymizer.py JSON_FILE_NAME
#
# Example: python FFRKAnonymizer.py battle-data.json
# This will anonymize the file battle-data.json and output the anonymized
# version to battle-data-1429807698 (number is current Unix time).

import sys
import json

from Utils import get_suffix_with_unix_time
from Utils import dump_json_to_file
from Utils import clean_up_filename

# Your user id will be replaced with this user id
ANONYMOUS_USER_ID = str(1234567890)

# When validating the user id, we check to see if it is this long
MIN_USER_ID_LENGTH = 16

# set this to True if you want to force anonymization even if validate_user_id
# returns False (useful for debugging)
FORCE_ANONYMIZE = False


# anonymizes the file with name filename, scrubbing out user_id and replacing it
# with ANONYMOUS_USER_ID
def anonymize_file(filename, user_id):
    out_filename = clean_up_filename(filename + get_suffix_with_unix_time())

    outfile = open(out_filename, 'w')

    with open(filename, 'r+') as f:
        for line in f:
            if user_id in line:
                outfile.write(line.replace(user_id, ANONYMOUS_USER_ID))
            else:
                outfile.write(line)

        outfile.close()


# some basic sanity checking on the user_id we plan to scrub
def validate_user_id(user_id):
    if not user_id:
        print "ERROR - user_id is empty. Aborting!"
        return FORCE_ANONYMIZE or False

    if user_id == ANONYMOUS_USER_ID:
        print "ERROR - file has already been anonymized. Aborting!"
        return FORCE_ANONYMIZE or False

    if len(user_id) < MIN_USER_ID_LENGTH:
        print "ERROR - user_id appears to be too short. Aborting!"
        return FORCE_ANONYMIZE or False

    return True


# pulls the user id from json_data and dumps json_data to filename if a
# file with that name does not exist (this case can happen if anonymize_json
# is called externally with just JSON and no file)
def anonymize_json(json_data, filename):
    # this method may be called with a filename that does not exist
    # so we want to create the file which is required for subsequent logic
    dump_json_to_file(json_data, filename)

    user_id = ""

    # battle/get_battle_init_data API
    if json_data.get('battle'):
        print "Anonymizing a battle/get_battle_init_data API response"
        user_id = json_data['battle']['buddy'][0]['ability_panels'][0]['uid']

    # dff/party/list
    if json_data.get('equipments') and json_data.get('materials'):
        print "Anonymizing a dff/party/list API response"
        user_id = str(json_data['party']['user_id'])

    # validate user_id before anonymizing
    if validate_user_id(user_id):
        anonymize_file(filename, user_id)


def main():
    with open(sys.argv[1]) as data_file:
        data = json.load(data_file)
        anonymize_json(data, sys.argv[1])


if __name__ == "__main__":
    main()
