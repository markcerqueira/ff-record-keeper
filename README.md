# ff-record-keeper
Tools for [Final Fantasy Record Keeper][1]

#### Files
* **battle-data.json** - Sample response from the battle/get_battle_init_data API
* **FFRKBattleDropParser.py** - With JSON response from the battle/get_battle_init_data API prints out items that will be dropped
* **FFRKItemIdParser.py** - With JSON response from the diff/party/list API prints out item names, item ids, and rarity
* **party-list.json** - Sample response from the diff/party/list API

#### Environment
These tools were developed on Mac OS Yosemite (10.10) using Python 2.7.9 (installed via homebrew). The Python files do not use any exotic libraries so these tools should work across different platforms.

#### Learn More
* [Blog post][2] describing more reliable Black Cowl farming using FFRKBattleDropParser.py
* [Reddit post][3] about more reliable Black Cowl farming

[1]: http://www.finalfantasyrecordkeeper.com/
[2]: http://mark.gg/2015/04/18/peeking-into-final-fantasy-record-keeper/
[3]: https://www.reddit.com/r/FFRecordKeeper/comments/332buz/method_to_more_reliably_farm_black_cowls_or_any/
