from abc import ABCMeta, abstractmethod
from functools import partial
from json import loads, dumps


class JSONSerializable(metaclass=ABCMeta):
    """ Common functionality for json serializable objects."""

    def __init__(self, serialize=None, deserialize=None):
        self.serialize = partial(dumps, default=serialize)
        self.deserialize = partial(loads, object_hook=deserialize)

    @property
    @abstractmethod
    def json(self):
        raise NotImplemented


class JSONRPCError(JSONSerializable):
    """ Error for JSON-RPC communication.

    The error codes from and including -32768 to -32000 are reserved for
    pre-defined errors. Any code within this range, but not defined explicitly
    below is reserved for future use. The error codes are nearly the same as
    those suggested for XML-RPC at the following
    url: http://xmlrpc-epi.sourceforge.net/specs/rfc.fault_codes.php
    """

    def __init__(self, json=None, code=None, message=None, data=None, serialize=None, deserialize=None):
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

        super().__init__(serialize=serialize, deserialize=deserialize)
        if json is not None:
            data = self.deserialize(json)
            self.code = data["code"]
            self.message = data["message"]
            self.data = data.get("data")
        else:
            self._data = {}
            self.code = getattr(self.__class__, "CODE", code)
            self.message = getattr(self.__class__, "MESSAGE", message)
            self.data = data

    @property
    def code(self):
        return self._data["code"]

    @code.setter
    def code(self, value):
        if not isinstance(value, int):
            raise ValueError("Error code should be integer")

        self._data["code"] = value

    @property
    def message(self):
        return self._data["message"]

    @message.setter
    def message(self, value):
        if not isinstance(value, str):
            raise ValueError("Error message should be string")
        self._data["message"] = value

    @property
    def data(self):
        return self._data.get("data")

    @data.setter
    def data(self, value):
        if value is not None:
            self._data["data"] = value

    @property
    def json(self):
        return self.serialize(self._data)

    def as_response(self, id=None):
        from jsonrpc.response import JSONRPCSingleResponse
        return JSONRPCSingleResponse(error=self._data, id=id)