import json
import socket
import uuid

from jsonrpc.utils import json_datetime_default, json_datetime_hook

from tools import recv_all, send_all


class RequestError(Exception):
    pass


class ParamsError(Exception):
    pass


class Proxy:
    server_address = None

    def __init__(self, server_address):
        self.server_address = server_address

    def __getattr__(self, name):
        def method(*args, **kwargs):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(self.server_address)
                identifier, payload = self.create_payload(name, *args, **kwargs)
                send_all(socket=sock, message=payload)
                response = recv_all(socket=sock)
            raw_result = json.loads(response, object_hook=json_datetime_hook)
            try:
                return raw_result['result']
            except KeyError:
                raise RequestError(
                    'Error [{code}]: {msg}, method: {method}, request <{id}>'
                    .format(
                        code=raw_result['error']['code'],
                        msg=raw_result['error']['message'],
                        method=name,
                        id=raw_result['id']
                    )
                )

        return method

    def create_payload(self, name: str, *args: list, **kwargs: dict) -> (int, str):
        if args and kwargs:
            raise ParamsError('Define only args or kwargs, passed both.')
        identifier = str(uuid.uuid1())
        template = {
            "id": identifier,
            "jsonrpc": "2.0",
            "method": name,
            "params": args or kwargs
        }
        return identifier, json.dumps(template, default=json_datetime_default)
