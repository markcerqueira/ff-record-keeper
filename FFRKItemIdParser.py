# FFRKItemIdParser.py
# Author: Mark Cerqueira (www.mark.gg)
#
# Hosted at: https://gist.github.com/markcerqueira/dba639168700bd02a623
# See sample JSON for parsing: https://gist.github.com/markcerqueira/d4ec280f5c448d7ca45e
#
# Save the JSON text response from the diff/party/list API from FFRK
# and then run this program to print out the name and item ids
#
# Usage: python FFRKItemIdParser.py JSON_FILE_NAME
#
# Example: python FFRKItemIdParse.py party-list.json > itemIds.csv
# This example reads data from party-list.json and ouputs the result to a file
# called itemIds.csv. You can then use Google Docs to convert CSV to another format

import sys
import json

# use a dictionary so we don't print multiple instances of an item mulitple times
item_dict = dict()

with open(sys.argv[1]) as data_file: 
	# load the JSON file  
    data = json.load(data_file)
	
	# put equipment in the dictionary
    for equipment in data['equipments']:
		item_dict[equipment['name'].encode('utf8')] = str(equipment['equipment_id']).encode('utf8')
		
	# put materials in the dictionary
    for material in data['materials']:
		item_dict[equipment['name'].encode('utf8')] = str(equipment['id']).encode('utf8')

# print out equipment/materials names to item ids
for key in item_dict:
    print key + ", " + item_dict[key]