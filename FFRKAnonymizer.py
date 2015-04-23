# FFRKAnonymizer.py
# Author: Mark Cerqueira (www.mark.gg)
#
# Hosted at: https://github.com/markcerqueira/ff-record-keeper
#
# Currently supported API responses for anonymizing:
#   * diff/party/list
#   * battle/get_battle_init_data
#
# Usage: python FFRKAnonymizer.py JSON_FILE_NAME
#
# Example: python FFRKAnonymizer.py battle-data.json
# This will anonymize the file battle-data.json and output the anonymized
# version to battle-data-1429807698 (number is current Unix time).

import sys
import json
import time

ANONYMOUS_USER_ID = str(1234567890)

MIN_USER_ID_LENGTH = 16

# set this to True if you want to force anonymization even if validate_user_id
# returns False (useful for debugging)
FORCE_ANONYMIZE = True

# return the suffix that will be appended to anonymized files (e.g. "-1429807698")
def get_anonymized_file_suffix():
    return "-" + get_unix_time_str();


# return unix time as string
def get_unix_time_str():
    return str(int(time.time()))


# anonymizes the file with name filename, scrubbing out user_id and replacing it
# with ANONYMOUS_USER_ID
def anonymize_file(filename, user_id):
    outfile = open(filename + get_anonymized_file_suffix(), 'w')

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


def main():
    with open(sys.argv[1]) as data_file:
        data = json.load(data_file)
        user_id = ""

        # battle/get_battle_init_data API
        if data.get('battle'):
            print "Anonymizing a battle/get_battle_init_data API response"
            user_id = data['battle']['buddy'][0]['ability_panels'][0]['uid']

        # diff/party/list
        if data.get('equipments') and data.get('materials'):
            print "Anonymizing a diff/party/list API response"
            user_id = str(data['party']['user_id'])

        # validate user_id before anonymizing
        if validate_user_id(user_id):
            anonymize_file(sys.argv[1], user_id)


if __name__ == "__main__":
    main()
