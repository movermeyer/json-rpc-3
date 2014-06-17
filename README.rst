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

.. include:: examples/server.py
    :code: python

Client (uses `requests <http://www.python-requests.org/en/latest/>`_)

.. code-block:: python

    import requests
    import json


    def main():
        url = "http://localhost:4000/jsonrpc"
        headers = {'content-type': 'application/json'}

        # Example echo method
        payload = {
            "method": "echo",
            "params": ["echome!"],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(
            url, data=json.dumps(payload), headers=headers).json()

        assert response["result"] == "echome!"
        assert response["jsonrpc"]
        assert response["id"] == 0

    if __name__ == "__main__":
        main()

Competitors
-----------
There are `several libraries <http://en.wikipedia.org/wiki/JSON-RPC#Implementations>`_ implementing JSON-RPC protocol.
List below represents python libraries, none of the supports python3. tinyrpc looks better than others.
