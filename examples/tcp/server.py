# !/usr/bin/python3.4
import sys
import argparse
from socketserver import ThreadingTCPServer, BaseRequestHandler

from jsonrpc import JSONRPCResponseManager
from jsonrpc.utils import json_datetime_hook, json_datetime_default

from tools import recv_all, send_all
from api import *
import time


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class RequestHandler(BaseRequestHandler):
    def handle(self):
        start = time.clock()
        req = recv_all(socket=self.request)
        response = JSONRPCResponseManager(
            serialize_hook=json_datetime_default,
            deserialize_hook=json_datetime_hook).handle(req, dispatcher)
        send_all(socket=self.request, message=response.json)
        end = time.clock()
        if response.error is None:
            print('{}[{:2.4f}s]{} Method: {}{:16s}{} | Params: {}{}{}'.format(
                Colors.BLUE, end - start, Colors.ENDC,
                Colors.GREEN, response._request.method, Colors.ENDC,
                Colors.HEADER, response._request.params, Colors.ENDC
            ))
        else:
            print('{}[{:2.4f}s]{} Error: {}{}{} | Request: {}{}{}'.format(
                Colors.BLUE, end - start, Colors.ENDC,
                Colors.FAIL, response.error['data']['type'], Colors.ENDC,
                Colors.HEADER, req, Colors.ENDC
            ))


class Server(ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def run_server(host=None, port=None):

    server = Server((host, port), RequestHandler)
    print('Starting server…')
    try:
        print('{0}[OK!]{1}'.format(Colors.GREEN, Colors.ENDC))
        server.serve_forever()
    except KeyboardInterrupt:
        print('{0}[Stopped]{1}'.format(Colors.WARNING, Colors.ENDC))
        sys.exit(0)
    except Exception as exc:
        print('{0}[FAIL]{1} {2}'.format(Colors.FAIL, Colors.ENDC, str(exc)))


def parse_args(arguments=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-P', '--port', type=int, default=4000, help='server port')
    parser.add_argument('-H', '--host', default='127.0.0.1', help='server host')
    return parser.parse_args(arguments)


if __name__ == '__main__':
    args = parse_args()
    run_server(args.host, args.port)
