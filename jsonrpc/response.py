""" JSON-RPC response wrappers """

from jsonrpc.base import JSONSerializable


class JSONRPCError(JSONSerializable):
    """ Error for JSON-RPC communication.

    The error codes from and including -32768 to -32000 are reserved for
    pre-defined errors. Any code within this range, but not defined explicitly
    below is reserved for future use. The error codes are nearly the same as
    those suggested for XML-RPC at the following
    url: http://xmlrpc-epi.sourceforge.net/specs/rfc.fault_codes.php
    """

    def __init__(self, code, message, data=None, serialize_hook=None, deserialize_hook=None):
        """
        When a rpc call encounters an error, the Response Object MUST contain the
        error member with a value that is a Object with the following members in __init__

        :param int code: A Number that indicates the error type that occurred.
            This MUST be an integer.
        :param str message: A String providing a short description of the error.
            The message SHOULD be limited to a concise single sentence.
        :param data: A Primitive or Structured value that contains additional
            information about the error.
            This may be omitted.
            The value of this member is defined by the Server (e.g. detailed error
            information, nested errors etc.).
        :type data: None or int or str or dict or list
        """

        super().__init__(serialize_hook=serialize_hook, deserialize_hook=deserialize_hook)
        self._container = {}
        if not isinstance(code, int):
            raise ValueError("Error code should be integer")
        else:
            self._container['code'] = code

        if not isinstance(message, str):
            raise ValueError("Error message should be string")
        else:
            self._container['message'] = message

        if data is not None:
            self._container['data'] = data

    @property
    def code(self):
        return self._container['code']

    @property
    def message(self):
        return self._container['message']

    @property
    def data(self):
        return self._container.get('data')

    @property
    def json(self):
        return self.serialize(self._container)

    def as_response(self):
        return JSONRPCSingleResponse(result=self._container, error=True)


class JSONRPCSingleResponse(JSONSerializable):
    """ JSON-RPC response object to JSONRPCRequest. """
    _error_flag = None

    def __init__(self, request=None, result=None, error=None, serialize_hook=None, deserialize_hook=None):
        """
        :param error: This member is REQUIRED on error.
        :type error: bool
        """
        super().__init__(serialize_hook=serialize_hook, deserialize_hook=deserialize_hook)

        self.result = result
        self.request = request if not error else None
        self.error = result if error else None
        self.id = request.id if not error else None
        self._error_flag = error

    @property
    def data(self):
        data = {"jsonrpc": "2.0", "id": self.id}
        if self._error_flag:
            data["error"] = self.result
        else:
            data["result"] = self.result
        return data

    @property
    def json(self):
        return self.serialize(self.data)


class JSONRPCBatchResponse(JSONSerializable):
    def __init__(self, responses=None, serialize_hook=None):
        """
        :param responses: List of JSONRPCSingleResponse objects
        :type responses: list(JSONRPCSingleResponse)
        :param serialize: serializer json.dumps() by default
        """
        super().__init__(serialize_hook=serialize_hook)
        self.responses = responses

    @property
    def data(self):
        return [r.data for r in self.responses]

    @property
    def json(self):
        return self.serialize(self.data)

    def __iter__(self):
        return iter(self.responses)

