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
# Example:

import sys
import json
import time

ANONYMOUS_USER_ID = str(1234567890)

MIN_USER_ID_LENGTH = 16

def get_unix_time_str():
    return str(int(time.time()))


def anonymize_file(filename, user_id):
    outfile = open(filename + "-" + get_unix_time_str(), 'w')

    with open(filename, 'r+') as f:
        for line in f:
            if user_id in line:
                outfile.write(line.replace(user_id, ANONYMOUS_USER_ID))
            else:
                outfile.write(line)

        outfile.close()


def validate_user_id(user_id):
    if not user_id:
        print "ERROR - user_id is empty. Aborting!"
        return False

    if user_id == ANONYMOUS_USER_ID:
        print "ERROR - file has already been anonymized. Aborting!"
        return False

    if len(user_id) < MIN_USER_ID_LENGTH:
        print "ERROR - user_id appears to be too short. Aborting!"
        return False

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
