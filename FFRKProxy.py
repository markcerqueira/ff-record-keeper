# FFRKProxy.py
# Author: Mark Cerqueira (www.mark.gg)
#
# Hosted at: https://github.com/markcerqueira/ff-record-keeper
#
# A simple proxy (using libmproxy) that prints out data when known
# parsable APIs pass through it
#
# Currently supported API print outs:
#   * dff/party/list
#   * battle/get_battle_init_data
#
# Usage: python FFRKProxy.py PORT
# Note: PORT is optional. If it is not provided the default
#       specified below at DEFAULT_PORT (8080) will be used.

import sys
import json
import socket

from libmproxy import controller, proxy
from libmproxy.protocol.http import decoded
from libmproxy.proxy.server import ProxyServer

from FFRKBattleDropParser import print_drops_from_json
from FFRKItemIdParser import print_equipment_id_from_json

from Utils import get_suffix_with_unix_time
from Utils import dump_json_to_file


DEFAULT_PORT = 8080

# dump handled content to a file; WARNING - files are not anonymized and may include
# sensitive user information. See FFRKAnonymizer.py for more info
DUMP_CONTENT_TO_FILES = True

FFRK_HOST = 'ffrk.denagames.com'

EQUIPMENT_LIST_PATH = 'dff/party/list'
EQUIPMENT_LIST_FILENAME = 'party_list'

BATTLE_INFO_PATH = 'get_battle_init_data'
BATTLE_INFO_FILENAME = 'get_battle_init_data'

class FFRKProxy(controller.Master):
    def __init__(self, server):
        controller.Master.__init__(self, server)

    def run(self):
        try:
            return controller.Master.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_request(self, flow):
        flow.reply()

    def handle_response(self, flow):
        # we only care about URLs that are going to FFRK_HOST


        if FFRK_HOST in flow.request.host:
            # get_battle_init_data call
            if BATTLE_INFO_PATH in flow.request.path:
                print flow.request.path + " called"
                with decoded(flow.response):
                    json_data = json.loads(flow.response.content)
                    print_drops_from_json(json_data)

                    if DUMP_CONTENT_TO_FILES:
                        dump_json_to_file(json_data, BATTLE_INFO_FILENAME + get_suffix_with_unix_time())

                print ""

            # dff/party/list call
            elif EQUIPMENT_LIST_PATH in flow.request.path:
                print flow.request.path + " called"
                with decoded(flow.response):
                    json_data = json.loads(flow.response.content)
                    print_equipment_id_from_json(json_data)

                    if DUMP_CONTENT_TO_FILES:
                        dump_json_to_file(json_data, EQUIPMENT_LIST_FILENAME + get_suffix_with_unix_time())

                print ""

            else:
                print flow.request.path + " called; no processing done"
                print ""

        # forward the reply so it gets passed on
        flow.reply()


def main(argv):
    # if port specified as option, use that instead
    proxy_port = DEFAULT_PORT
    if len(argv) >= 2:
        proxy_port = int(argv[1])

    # sanity check
    if proxy_port < 1024 or proxy_port > 65535:
        print "WARNING - port number specified is outside the \"good\" range (1024-65535)"
        proxy_port = DEFAULT_PORT

    print "IP Address = " + socket.gethostbyname(socket.gethostname()) + ", Port = " + str(proxy_port) + "\n"

    config = proxy.ProxyConfig(port=proxy_port)
    server = ProxyServer(config)
    ffrk_proxy = FFRKProxy(server)
    ffrk_proxy.run()


if __name__ == "__main__":
    main(sys.argv)
