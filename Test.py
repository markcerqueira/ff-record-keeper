
import json

from Utils import get_description_for_item_id
from FFRKBattleDropParser import get_drops_from_json
from FFRKItemIdParser import get_equipment_id_from_json

# runs some tests on get_description_for_item_id
def test_get_description_for_item_id():
    # standard tests on each CSV file for item ids that are present
    assert 'Iron Sword (XII)' in get_description_for_item_id(str(21002002))  # WEAPON: Iron Sword (XII), rarity = 2*, id = 21002002
    assert 'Sniper Eye (VI)' in get_description_for_item_id(str(23080016))  # ACCESSORY: Sniper Eye (VI), rarity = 1*, id = 23080016
    assert 'Carbon Bangle (VII)' in get_description_for_item_id(str(22056004))  # ARMOR: Carbon Bangle (VII), rarity = 2*, id = 22056004
    assert 'Greater Black Orb' in get_description_for_item_id(str(40000014))  # ORB: Greater Black Orb, rarity = 4*, id = 40000014

    # test when an item id does not exist in the respective CSV file
    assert 'Unknown ARMOR' in get_description_for_item_id(str(22000000))  # Unknown ARMOR with id = 22000000

    # test when we get an unknown prefix
    assert 'Unknown prefix' in get_description_for_item_id(str(32000000)) # Unknown prefix for item id = 32000000


# test FFRKBattleDropParser.py
def test_battle_drop_parser():
    with open('json/get_battle_init_data-1430543134.json') as data_file:
        result = get_drops_from_json(json.load(data_file))
        assert 'White Orb' in result and 'Round 1' in result

    with open('json/get_battle_init_data-1430542137.json') as data_file:
        result = get_drops_from_json(json.load(data_file))
        assert 'Twist Headband (V)' in result and 'Round 1' in result
        assert 'Minor White Orb' in result and 'Round 2' in result


# test FFRKItemIdParser.py
def test_item_id_parser():
    with open('json/party_list-1430322460.json') as data_file:
        result = get_equipment_id_from_json(json.load(data_file))
        assert 'Iron Bangle (VII)' in result and 'Dark Orb' in result


if __name__ == "__main__":
    test_get_description_for_item_id()

    test_battle_drop_parser()

    test_item_id_parser()