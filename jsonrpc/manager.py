import logging

from jsonrpc.exceptions import JSONRPCInvalidRequest, JSONRPCInvalidRequestException, JSONRPCParseError
from jsonrpc.request import JSONRPCSingleRequest, JSONRPCBatchRequest
from jsonrpc.response import JSONRPCSingleResponse
from jsonrpc.base import JSONSerializable

logger = logging.getLogger(__name__)


class JSONRPCResponseManager(JSONSerializable):
    """ JSON-RPC response manager. """

    def handle(self, request_str, dispatcher):
        """
        Method brings syntactic sugar into library.
        Given dispatcher it handles request (both single and batch) and handles errors.
        Request could be handled in parallel, it is server responsibility.

        :param request_str: JSON string.
            Will be converted into JSONRPCRequest or JSONRPCBatchRequest
        :type request_str: str
        :type dispatcher: Dispatcher or dict
        :rtype: JSONRPCSingleResponse or JSONRPCBatchResponse
        """

        try:
            request = self.parse(request_string=request_str)
        except (TypeError, ValueError):
            return JSONRPCParseError().as_response()
        except JSONRPCInvalidRequestException:
            return JSONRPCInvalidRequest().as_response()
        else:
            return request.process(dispatcher)

    def parse(self, request_string=None):
        """ Parse json and returns appropriate request object

        :param request_string: String with JSON-encoded request(s)
        :type request_string: str
        :rtype: JSONRPCSingleRequest or JSONRPCBatchRequest
        """
        data = self.deserialize(request_string)

        if isinstance(data, list):
            request = JSONRPCBatchRequest(
                serialize_hook=self.serialize_hook,
                data=[JSONRPCSingleRequest(serialize_hook=self.serialize_hook, data=reqest_dct) for reqest_dct in data]
            )
        elif isinstance(data, dict):
            request = JSONRPCSingleRequest(serialize_hook=self.serialize_hook, data=data)
        else:
            raise JSONRPCInvalidRequestException

        if request:
            return request
        else:
            raise JSONRPCInvalidRequestException
