import json
import logging

from .exceptions import (
    JSONRPCInvalidParams,
    JSONRPCInvalidRequest,
    JSONRPCInvalidRequestException,
    JSONRPCMethodNotFound,
    JSONRPCParseError,
    JSONRPCServerError,
)
from .jsonrpc2 import (
    JSONRPC20BatchRequest,
    JSONRPC20BatchResponse,
    JSONRPC20Response,
)
from .jsonrpc import JSONRPCRequest


logger = logging.getLogger(__name__)


class JSONRPCResponseManager:
    """ JSON-RPC response manager. """

    RESPONSE_CLASS_MAP = {
        "2.0": JSONRPC20Response,
    }

    json_object_hook = None

    def __init__(self, json_object_hook=None):
        self.json_object_hook = json_object_hook

    def handle(self, request_str, dispatcher):
        """
        Method brings syntactic sugar into library.
        Given dispatcher it handles request (both single and batch) and handles errors.
        Request could be handled in parallel, it is server responsibility.

        :param request_str: JSON string.
            Will be converted into JSONRPC20Request or JSONRPC20BatchRequest
        :type request_str: str
        :type dispatcher: Dispatcher
        :rtype: JSONRPC20Response | JSONRPC20BatchResponse
        """
        try:
            json.loads(request_str, object_hook=self.json_object_hook)
        except (TypeError, ValueError):
            return JSONRPC20Response(error=JSONRPCParseError()._data)

        try:
            request = JSONRPCRequest.from_json(request_str)
        except JSONRPCInvalidRequestException:
            return JSONRPC20Response(error=JSONRPCInvalidRequest()._data)

        rs = request if isinstance(request, JSONRPC20BatchRequest) \
            else [request]
        responses = [r for r in self._get_responses(rs, dispatcher)
                     if r is not None]

        # notifications
        if not responses:
            return

        if isinstance(request, JSONRPC20BatchRequest):
            return JSONRPC20BatchResponse(*responses)
        else:
            return responses[0]

    @classmethod
    def _get_responses(cls, requests, dispatcher):
        """ Response to each single JSON-RPC Request.

        :type dispatcher: Dispatcher
        :type requests: iterator(JSONRPC20Request)
        :return iterator(JSONRPC20Response):

        """
        for request in requests:
            response = lambda **kwargs: cls.RESPONSE_CLASS_MAP[request.JSONRPC_VERSION](_id=request._id, **kwargs)

            try:
                method = dispatcher[request.method]
            except KeyError:
                output = response(error=JSONRPCMethodNotFound()._data)
            else:
                try:
                    result = method(*request.args, **request.kwargs)
                except TypeError:
                    output = response(error=JSONRPCInvalidParams()._data)
                except Exception as e:
                    data = {
                        "type": e.__class__.__name__,
                        "args": e.args,
                        "message": str(e),
                    }
                    logger.exception("API Exception: {0}".format(data))
                    output = response(error=JSONRPCServerError(data=data)._data)
                else:
                    output = response(result=result)
            finally:
                if not request.is_notification:
                    yield output
