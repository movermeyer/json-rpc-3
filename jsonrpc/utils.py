""" Utility functions for package."""
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta, tzinfo
import json
from jsonrpc.exceptions import JSONRPCMethodNotFound, JSONRPCInvalidParams, JSONRPCServerError
from jsonrpc.response import JSONRPCSingleResponse


class FixedOffset(tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, offset):
        self.__offset = timedelta(seconds=offset)

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return 'TZ offset: {secs} hours'.format(secs=self.__offset)

    def dst(self, dt):
        return timedelta(0)


def json_datetime_default(dt):
    """ Encoder for datetime objects.
    Usage: json.dumps(object, cls=DatetimeEncoder)
    """
    if isinstance(dt, datetime):
        dt_dct = {"__datetime__": [
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond
        ]}
        if dt.tzinfo is not None:
            dt_dct["__tzshift__"] = dt.utcoffset().seconds
        return dt_dct
    raise TypeError


def json_datetime_hook(dictionary):
    """
    JSON object_hook function for decoding datetime objects.
    Used in pair with
    :return: Datetime object
    :rtype: datetime
    """
    if "__datetime__" not in dictionary:
        return dictionary

    dt = datetime(*dictionary["__datetime__"])

    if "__tzshift__" in dictionary:
        dt = dt.replace(tzinfo=FixedOffset(dictionary["__tzshift__"]))

    return dt


def process_single_request(request, dispatcher):
    try:
        method = dispatcher[request.method]
        result = method(*request.args, **request.kwargs)
    except KeyError:
        output = JSONRPCMethodNotFound().as_response(_id=request.id)
    except TypeError:
        output = JSONRPCInvalidParams().as_response(_id=request.id)
    except Exception as e:
        data = {'type': e.__class__.__name__, 'args': e.args, 'message': str(e)}
        output = JSONRPCServerError(data=data).as_response(_id=request.id)
    else:
        output = JSONRPCSingleResponse(request=request, result=result)
    finally:
        if not request.is_notification:
            return output


