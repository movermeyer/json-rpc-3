json-rpc-3
==========

.. image:: https://travis-ci.org/Orhideous/json-rpc-3.png
    :target: https://travis-ci.org/Orhideous/json-rpc-3
    :alt: Build Status

.. image:: https://coveralls.io/repos/Orhideous/json-rpc-3/badge.png?branch=master
    :target: https://coveralls.io/r/Orhideous/json-rpc-3?branch=master
    :alt: Coverage Status

.. image:: https://pypip.in/v/json-rpc-3/badge.png
    :target: https://crate.io/packages/json-rpc-3
    :alt: Version

.. image:: https://pypip.in/d/json-rpc-3/badge.png
    :target: https://crate.io/packages/json-rpc-3
    :alt: Downloads

.. image:: https://pypip.in/format/json-rpc-3/badge.png
    :target: https://pypi.python.org/pypi/json-rpc-3/
    :alt: Download format

.. image:: https://pypip.in/license/json-rpc-3/badge.png
    :target: https://pypi.python.org/pypi/json-rpc-3/
    :alt: License


Pure Python 3 `JSON-RPC 2.0 <http://www.jsonrpc.org/specification>`_ transport specification implementation. Supports python3.2+.
Fork of `json-rpc <https://github.com/pavlov99/json-rpc>`_.

Documentation: http://json-rpc-3.readthedocs.org

This implementation does not have any transport functionality realization, only protocol.
Any client or server realization is easy based on current code, but requires transport libraries, such as requests, gevent or zmq, see `examples <https://github.com/Orhideous/json-rpc/tree/master/examples>`_.

Install
-------

.. code-block:: python

    pip install json-rpc-3

Tests
-----

.. code-block:: python

    nosetests

Quickstart
----------
Server (uses `Werkzeug <http://werkzeug.pocoo.org/>`_)

.. code-block:: python

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

Client (uses `requests <http://www.python-requests.org/en/latest/>`_)

.. code-block:: python

    import json

    import requests


    url = "http://localhost:4000/jsonrpc"
    headers = {'content-type': 'application/json'}


    def print_result(payload):
        response = requests.post(
            url,
            data=json.dumps(payload),
            headers=headers
        ).json()

        print(
            r"""
            {0}
            {1}
            """.format(payload, response))


    def main():
        payloads = [
            {
                "method": "simple_add",
                "params": {"first": 17, "second": 39},
                "jsonrpc": "2.0",
                "id": 0,
            },
            {
                "method": "echo",
                "params": ["Hello!"],
                "jsonrpc": "2.0",
                "id": 1
            },
            {
                "method": "time_ping",
                "jsonrpc": "2.0",
                "id": 2
            },
            {
                "method": "dict_to_list",
                "jsonrpc": "2.0",
                "params": [{1: 3, 'two': 'string', 3: [5, 'list', {'c': 0.3}]}],
                "id": 3
            },
            # Exception!
            {
                "method": "subtract",
                "jsonrpc": "2.0",
                "params": [1, 2, 3],
                "id": 2
            }
        ]
        for payload in payloads:
            print_result(payload)


    if __name__ == "__main__":
        main()


Competitors
-----------
There are `several libraries <http://en.wikipedia.org/wiki/JSON-RPC#Implementations>`_ implementing JSON-RPC protocol.
List below represents python libraries, none of the supports python3. tinyrpc looks better than others.
