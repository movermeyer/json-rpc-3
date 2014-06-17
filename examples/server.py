""" Example of json-rpc usage with Wergzeug and requests.

NOTE: there are no Werkzeug and requests in dependencies of json-rpc.
NOTE: server handles all url paths the same way (there are no different urls).
"""

from datetime import datetime

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher


manager = JSONRPCResponseManager()


def dict_to_list(dictionary):
    return list(dictionary.items())


@dispatcher.add_method
def simple_add(first=0, **kwargs):
    return first + kwargs["second"]


def echo_with_long_name(msg):
    return msg


def time_ping():
    return datetime.now().isoformat()


dispatcher.add_method(time_ping)
dispatcher.add_method(echo_with_long_name, name='echo')

dispatcher['subtract'] = lambda a, b: a - b
dispatcher['dict_to_list'] = dict_to_list


@Request.application
def application(request):
    response = manager.handle(request.get_data(cache=False, as_text=True), dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 4000, application)
