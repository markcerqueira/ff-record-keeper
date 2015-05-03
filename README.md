# ff-record-keeper [![Build Status](https://travis-ci.org/markcerqueira/ff-record-keeper.svg?branch=master)](https://travis-ci.org/markcerqueira/ff-record-keeper)
Tools for [Final Fantasy Record Keeper][1]

The most useful script here is FFRKProxy. It creates a proxy using [libmproxy/mitmproxy][7]. See the Environment section below for how to set up Python and libmproxy/mitmproxy. Then run FFRKProxy.py and point your device at your computer's IP address and the port number specified by FFRKProxy. Then watch the data roll in as you play FFRK.

    ~src/ff-record-keeper [master] python FFRKProxy.py
    IP Address = 10.0.0.1, Port = 8080
    
    /dff/battle/?timestamp=1430363386&battle_id=720151 called; no processing done
    
    /dff/event/challenge/4/get_battle_init_data called
    Round 1 - enemy will drop ORB: Lesser Earth Orb, rarity = 2*, id = 40000047
    Round 2 - enemy will drop ARMOR: Copper Cuirass (V), rarity = 1*, id = 22053001
    Round 3 - round drop type = 22
    Round 3 - enemy will drop GOLD amount = 733
    
    /dff/party/list called
    Knight Armor (III), 22054008, 3
    Major Earth Orb, 40000050, 5
    
    /dff/battle/get_battle_init_data called
    
#### File/Folder Descriptions
* **FFRKAnonymizer.py** - Given a JSON response, "anonymizes" it by removing the user_id and replacing it with 1234567890
* **FFRKBattleDropParser.py** - With JSON response from the battle/get_battle_init_data API prints out items that will be dropped
* **FFRKItemIdParser.py** - With JSON response from the diff/party/list API prints out item names, item ids, and rarity
* **FFRKProxy.py** - Runs a simple proxy that wraps the response-parsing functionality of the other Python files. You set your
device to point at the proxy and when a known API passes through the proxy, the proxy will parse relevant information out of the 
response body and print just that. See "Example FFRKProxy Output" for an example of what this looks like.
* **Test.py** - Unit tests that exercise functionality of scripts.
* **Utils.py** - Shared utility methods used by the other scripts.

* **data** - Contains CSV files used by Utils.py to map item ids to weapons, armor, orbs, and accessories. Data fetched from the [r/FFRecordKeeper][11] community-maintained [Google spreadsheet][10].
* **json** - Sample JSON from the /dff/party/list and get_battle_init_data APIs (anonymized using FFRKAnonymizer)

#### Environment
These tools were developed on Mac OS Yosemite (10.10), [PyCharm CE][4], and Python 2.7.9 (installed via [homebrew][5]). 
The Python files except FFRKProxy do not use any exotic libraries so these tools should just work.
FFRKProxy uses [libmproxy][7]. Visit the [Installation][8] page to learn how to install it.

##### Set-up on Mac
1. Install [homebrew][5].
2. On command-line: brew install python
3. Install Xcode from the App Store.
4. On command-line: xcode select --install
5. On command-line: pip install mitmproxy

Please feel free to share instructions for set up on other platforms and I will post them here! And please let me know
if any of the above instructions do not work.

#### Contribute
Please feel free to fork, improve, and open a [pull request][6]. More JSON data (anonymized of course) would be greatly appreciated! If you want to contribute without using GitHub, feel free to email me at: {GitHub username} at gmail dot com.

#### Learn More
* [Blog post][2] describing more reliable Black Cowl farming using FFRKBattleDropParser.py
* [Reddit post][3] about more reliable Black Cowl farming
* Jon Chang's [Record Peeker][9], a cleverly-named proxy that is similar to this one!

[1]: http://www.finalfantasyrecordkeeper.com/
[2]: http://mark.gg/2015/04/18/peeking-into-final-fantasy-record-keeper/
[3]: https://www.reddit.com/r/FFRecordKeeper/comments/332buz/method_to_more_reliably_farm_black_cowls_or_any/
[4]: https://www.jetbrains.com/pycharm/
[5]: http://brew.sh/
[6]: https://help.github.com/articles/using-pull-requests/
[7]: https://mitmproxy.org/doc/scripting/libmproxy.html
[8]: https://mitmproxy.org/doc/install.html
[9]: https://github.com/jonchang/recordpeeker
[10]: https://docs.google.com/spreadsheets/d/1A4evEuBVvMzq9ap_5aWLLgnmKwB76coff22_WeBzhyM/edit#gid=554203550
[11]: https://www.reddit.com/r/FFRecordKeeper/
