""" JSON-RPC response wrappers """
import json
from jsonrpc.base import JSONSerializable


class JSONRPCAbstractResponce(JSONSerializable):
    pass

class JSONRPCError(JSONSerializable):
    """ Error for JSON-RPC communication.

    The error codes from and including -32768 to -32000 are reserved for
    pre-defined errors. Any code within this range, but not defined explicitly
    below is reserved for future use. The error codes are nearly the same as
    those suggested for XML-RPC at the following
    url: http://xmlrpc-epi.sourceforge.net/specs/rfc.fault_codes.php
    """

    def __init__(self, json=None, code=None, message=None, data=None, serialize_hook=None, deserialize_hook=None):
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
        return JSONRPCSingleResponse(error=self._data, id=id)


class JSONRPCSingleResponse:
    """ JSON-RPC response object to JSONRPCRequest. """


    def __init__(self, request=None, result=None, error=None, id=None):
        """
        When a rpc call is made, the Server MUST reply with a Response, except for
        in the case of Notifications. The Response is expressed as a single JSON
        Object, with the following members:

        :param result: This member is REQUIRED on success.
            This member MUST NOT exist if there was an error invoking the method.
            The value of this member is determined by the method invoked on the
            Server.

        :param error: This member is REQUIRED on error.
            This member MUST NOT exist if there was no error triggered during
            invocation. The value for this member MUST be an Object.
        :type error: dict

        :param request: This member is REQUIRED.
            It MUST be the same as the value of the id member in the Request
            Object. If there was an error in detecting the id in the Request
            object (e.g. Parse error/Invalid Request), it MUST be Null.
        :type request: JSONRPCSingleRequest

        Either the result member or error member MUST be included, but both
        members MUST NOT be included.
        """

        self._data = {}
        self.result = result
        self.request = request
        self.error = error
        self.id = request.id if request else id

        if self.result is None and self.error is None:
            raise ValueError("Either result or error should be used")

    @property
    def data(self):
        data = {k: v for k, v in self._data.items()}
        data["jsonrpc"] = "2.0"
        return data

    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            raise ValueError("data should be dict")

        self._data = value

    @property
    def result(self):
        return self._data.get("result")

    @result.setter
    def result(self, value):
        if value is not None:
            if self.error is not None:
                raise ValueError("Either result or error should be used")

            self._data["result"] = value

    @property
    def error(self):
        return self._data.get("error")

    @error.setter
    def error(self, value):
        if value is not None:
            if self.result is not None:
                raise ValueError("Either result or error should be used")
            JSONRPCError(**value)
            self._data["error"] = value

    @property
    def id(self):
        return self._data.get("id")

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, (str, int)):
            raise ValueError("id should be string or integer")
        self._data["id"] = value

    @property
    def json(self):
        if self.error:
            serialize = json.dumps
        else:
            serialize = self.request.serialize
        return serialize(self.data)  # Use serializer from request object


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
