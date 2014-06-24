""" JSON-RPC response wrappers """
import json
from jsonrpc.base import JSONRPCError, JSONSerializable


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
