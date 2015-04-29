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


DEFAULT_PORT = 8080

FFRK_HOST = 'ffrk.denagames.com'

PATH_EQUIPMENT_LIST = 'dff/party/list'
PATH_BATTLE_INFO = 'get_battle_init_data'


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
            if PATH_BATTLE_INFO in flow.request.path:
                print flow.request.path + " called"
                with decoded(flow.response):
                    print_drops_from_json(json.loads(flow.response.content))
                print ""

            # dff/party/list call
            if PATH_EQUIPMENT_LIST in flow.request.path:
                print flow.request.path + " called"
                with decoded(flow.response):
                    print_equipment_id_from_json(json.loads(flow.response.content))
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
