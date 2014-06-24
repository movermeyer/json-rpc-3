from jsonrpc.response import JSONRPCError


class JSONRPCException(Exception):
    """ JSON-RPC Exception."""
    pass


class JSONRPCParseException(Exception):
    """ Can't parse request from string."""
    pass


class JSONRPCMultipleRequestException(Exception):
    """ Found multiple requests. Try use batch instead"""
    pass


class JSONRPCInvalidRequestException(JSONRPCException):
    """ Request is not valid."""
    pass


class JSONRPCParseError(JSONRPCError):
    """ Parse Error.

    Invalid JSON was received by the server.
    An error occurred on the server while parsing the JSON text.
    """

    CODE = -32700
    MESSAGE = "Parse error"


class JSONRPCInvalidRequest(JSONRPCError):
    """ Invalid Request.

    The JSON sent is not a valid Request object.
    """

    CODE = -32600
    MESSAGE = "Invalid Request"


class JSONRPCMethodNotFound(JSONRPCError):
    """ Method not found.

    The method does not exist / is not available.
    """

    CODE = -32601
    MESSAGE = "Method not found"


class JSONRPCInvalidParams(JSONRPCError):
    """ Invalid params.

    Invalid method parameter(s).
    """

    CODE = -32602
    MESSAGE = "Invalid params"


class JSONRPCInternalError(JSONRPCError):
    """ Internal error.

    Internal JSON-RPC error.
    """

    CODE = -32603
    MESSAGE = "Internal error"


class JSONRPCServerError(JSONRPCError):
    """ Server error.

    Reserved for implementation-defined server-errors.
    """

    CODE = -32000
    MESSAGE = "Server error"
