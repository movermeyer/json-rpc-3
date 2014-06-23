""" JSON-RPC request wrappers """
from jsonrpc.base import JSONSerializable
from jsonrpc.response import JSONRPCBatchResponse
from jsonrpc.utils import process_single_request


class JSONRPCSingleRequest(JSONSerializable):
    """A rpc call is represented by sending a Request object to a Server."""

    result = None
    _data = {}

    REQUIRED_FIELDS = {"jsonrpc", "method"}
    POSSIBLE_FIELDS = {"jsonrpc", "method", "params", "id"}

    def __init__(self, serialize_hook=None, data=None):
        super().__init__(serialize_hook=serialize_hook)
        self._data = data

    def __iter__(self):
        yield self

    def __bool__(self):
        return self._validate()

    @property
    def args(self):
        return tuple(self.params) if isinstance(self.params, list) else ()

    @property
    def kwargs(self):
        return self.params if isinstance(self.params, dict) else {}

    @property
    def json(self):
        return self.serialize(self.data)

    @property
    def data(self):
        data = {k: v for k, v in self._data.items() if not (k == 'id' and self.is_notification)}
        data['jsonrpc'] = '2.0'
        return data

    @property
    def method(self):
        return self._data.get('method')

    @property
    def params(self):
        return self._data.get('params')

    @property
    def id(self):
        return self._data.get('id')

    @property
    def is_notification(self):
        return 'id' not in self._data

    def process(self, dispatcher):
        return process_single_request(self, dispatcher)

    def _validate(self):
        if not self._data:
            return False
        if not isinstance(self._data, dict):
            return False
        if not self.REQUIRED_FIELDS <= set(self._data.keys()) <= self.POSSIBLE_FIELDS:
            return False
        if self._data['jsonrpc'] != '2.0':
            return False

        if not isinstance(self._data['method'], str) or self._data['method'].startswith('rpc.'):
            return False

        if 'id' in self._data and not isinstance(self._data['id'], (str, int)):
            return False

        if 'params' in self._data and not isinstance(self._data['params'], (list, dict)):
            return False

        return True


class JSONRPCBatchRequest(JSONSerializable):
    """ Batch JSON-RPC 2.0 Request. """

    def __init__(self, serialize_hook=None, data=()):
        """
        :param data: requests
        :type data: list(JSONRPCSingleRequest)
        """
        super().__init__(serialize_hook=serialize_hook)
        self.requests = data

    def __iter__(self):
        return iter(self.requests)

    def __len__(self):
        return len(self.requests)

    def __bool__(self):
        return all(self) and bool(len(self))

    @property
    def json(self):
        return self.serialize([request.data for request in self.requests])

    def process(self, dispatcher):
        responses = list(filter(None, [process_single_request(request, dispatcher) for request in self]))
        if responses:
            return JSONRPCBatchResponse(responses=responses, serialize=self.serialize)

    @classmethod
    def from_json(cls, json_string):
        return
