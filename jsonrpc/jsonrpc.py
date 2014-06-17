""" JSON-RPC wrappers for version 1.0 and 2.0.

Objects diring init operation try to choose JSON-RPC 2.0 and in case of error
JSON-RPC 1.0.
from_json methods could decide what format is it by presence of 'jsonrpc'
attribute.

"""
from .utils import JSONSerializable
from .jsonrpc2 import JSONRPC20Request


class JSONRPCRequest(JSONSerializable):

    """ JSONRPC Request."""

    @classmethod
    def from_json(cls, json_str):
        return JSONRPC20Request.from_json(json_str)
