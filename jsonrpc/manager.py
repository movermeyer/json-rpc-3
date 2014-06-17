import logging

from .exceptions import (
    JSONRPCInvalidParams,
    JSONRPCInvalidRequest,
    JSONRPCInvalidRequestException,
    JSONRPCMethodNotFound,
    JSONRPCParseError,
    JSONRPCServerError,
)
from jsonrpc.request import JSONRPCRequest, JSONRPCSingleRequest
from jsonrpc.response import JSONRPCSingleResponse


logger = logging.getLogger(__name__)


class JSONRPCResponseManager:
    """ JSON-RPC response manager. """

    def __init__(self, serialize=None, deserialize=None):
        """
        :param serialize: default for json.dumps()
        :type serialize: callable
        :param deserialize: object_hook for json.loads()
        :type deserialize: callable
        """
        self.serialize = serialize
        self.deserialize = deserialize

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
            request = JSONRPCRequest.parse(
                request_string=request_str,
                serialize=self.serialize,
                deserialize=self.deserialize
            )
        except (TypeError, ValueError):
            return JSONRPCParseError().as_response()
        except JSONRPCInvalidRequestException:
            return JSONRPCInvalidRequest().as_response()
        else:
            return request.process(dispatcher)

    @classmethod
    def _get_results(cls, data, dispatcher):
        """ Response to each single JSON-RPC Request.

        :type dispatcher: Dispatcher
        :type data: JSONRPCSingleRequest or JSONRPCBatchRequest
        :return iterator(JSONRPCResponse):

        """
        if isinstance(data, JSONRPCSingleRequest):
            data = [data.data]

        for request in data:
            try:
                method = dispatcher[request.method]
            except KeyError:
                output = JSONRPCMethodNotFound().as_response(_id=request._id)
            else:
                try:
                    result = method(*request.args, **request.kwargs)
                except TypeError:
                    output = JSONRPCInvalidParams().as_response(_id=request._id)
                except Exception as e:

                    logger.exception("API Exception: {0}".format(data))
                    output = JSONRPCServerError(data=data).as_response(_id=request._id)
                else:
                    output = JSONRPCSingleResponse(request=request, result=result)
            finally:
                if not request.is_notification:
                    yield output
