""" JSON-RPC request wrappers """
from jsonrpc.exceptions import JSONRPCInvalidRequestException
from jsonrpc.base import JSONSerializable
from jsonrpc.response import JSONRPCBatchResponse
from jsonrpc.utils import process_single_request


class JSONRPCRequest:
    REQUIRED_FIELDS = {"jsonrpc", "method"}
    POSSIBLE_FIELDS = {"jsonrpc", "method", "params", "id"}

    @classmethod
    def parse(cls, request_string=None, serialize=None, deserialize=None):
        """ Parse json and returns appropriate request object

        :param request_string: String with JSON-encoded request(s)
        :type request_string: str
        :param serialize: default for json.dumps()
        :type serialize: callable
        :param deserialize: object_hook for json.loads()
        :type deserialize: callable
        :rtype: JSONRPCSingleRequest or JSONRPCBatchRequest
        """
        data = deserialize(request_string)

        if isinstance(data, list):
            cls.response_class = JSONRPCBatchRequest
            cls.validate_requests(data)
        elif isinstance(data, dict):
            cls.validate_requests([data])
            cls.response_class = JSONRPCSingleRequest

        return cls.response_class(serialize=serialize, deserialize=deserialize, data=data)

    @classmethod
    def validate_requests(cls, requests):
        """ Requests validator

        :param requests: Raw requests parsed from JSON
        :type requests: list(dict)
        """

        for request in requests:
            if not isinstance(request, dict):
                raise JSONRPCInvalidRequestException(
                    'Expected type {0} for request {1}. Got {2} instead.'
                    .format(type(dict), str(request), type(request))
                )
            if not cls.REQUIRED_FIELDS <= set(request.keys()) <= cls.POSSIBLE_FIELDS:
                extra = set(request.keys()) - cls.POSSIBLE_FIELDS
                missed = cls.REQUIRED_FIELDS - set(request.keys())
                msg = 'Invalid request. Extra fields: {0}, Missed fields: {1}'
                raise JSONRPCInvalidRequestException(msg.format(extra, missed))


class JSONRPCSingleRequest(JSONSerializable):
    """A rpc call is represented by sending a Request object to a Server."""

    result = None
    _data = {}

    def __init__(self, serialize=None, deserialize=None, data=None):
        super().__init__(serialize=serialize, deserialize=deserialize)
        self.method = data.get('method')
        self.params = data.get('params')
        self.id = data.get('id')
        self.is_notification = 'id' not in data

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
        data = {k: v for k, v in self._data.items()
                if not (k == 'id' and self.is_notification)}
        data['jsonrpc'] = '2.0'
        return data

    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            raise ValueError('data should be dict')

        self._data = value

    @property
    def method(self):
        return self._data.get('method')

    @method.setter
    def method(self, value):
        if not isinstance(value, str):
            raise ValueError('Method should be string')

        if value.startswith('rpc.'):
            raise ValueError(
                'Method names that begin with the word rpc followed by a '
                'period character (U+002E or ASCII 46) are reserved for '
                'rpc-internal methods and extensions and MUST NOT be used '
                'for anything else.')

        self._data['method'] = str(value)

    @property
    def params(self):
        return self._data.get('params')

    @params.setter
    def params(self, value):
        if value is not None and not isinstance(value, (list, tuple, dict)):
            raise ValueError('Incorrect params {0}'.format(value))

        if isinstance(value, tuple):
            value = list(value)

        if value is not None:
            self._data['params'] = value

    @property
    def id(self):
        return self._data.get('id')

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, (str, int)):
            raise ValueError("id should be string or integer")

        self._data["id"] = value

    def process(self, dispatcher):
        return process_single_request(self, dispatcher)


class JSONRPCBatchRequest(JSONSerializable):
    """ Batch JSON-RPC 2.0 Request. """

    def __init__(self, serialize=None, deserialize=None, data=None):
        """
        :param data: requests
        :type data: list(dict)
        """
        super().__init__(serialize=serialize, deserialize=deserialize)
        self.requests = data

    @property
    def json(self):
        return self.serialize([request.data for request in self.requests])

    def __iter__(self):
        return iter(self.requests)

    def process(self, dispatcher):
        responses = [process_single_request(request, dispatcher) for request in self.requests]
        return JSONRPCBatchResponse(responses=responses, serialize=self.serialize, deserialize=self.deserialize)
