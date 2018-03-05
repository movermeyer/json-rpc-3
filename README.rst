json-rpc-3
==========

.. image:: https://travis-ci.org/Orhideous/json-rpc-3.png
    :target: https://travis-ci.org/Orhideous/json-rpc-3
    :alt: Build Status

.. image:: https://coveralls.io/repos/Orhideous/json-rpc-3/badge.png?branch=master
    :target: https://coveralls.io/r/Orhideous/json-rpc-3?branch=master
    :alt: Coverage Status

.. image:: https://img.shields.io/pypi/v/json-rpc-3.svg
    :target: https://crate.io/packages/json-rpc-3
    :alt: Version

.. image:: https://img.shields.io/pypi/dm/json-rpc-3.svg
    :target: https://crate.io/packages/json-rpc-3
    :alt: Downloads

.. image:: https://img.shields.io/pypi/format/json-rpc-3.svg
    :target: https://pypi.python.org/pypi/json-rpc-3/
    :alt: Download format

.. image:: https://img.shields.io/pypi/l/json-rpc-3.svg
    :target: https://pypi.python.org/pypi/json-rpc-3/
    :alt: License


Pure Python 3 `JSON-RPC 2.0 <http://www.jsonrpc.org/specification>`_ transport specification implementation. Supports python3.2+.
Fork of `json-rpc <https://github.com/pavlov99/json-rpc>`_.

Documentation: http://json-rpc-3.readthedocs.org

This implementation does not have any transport functionality realization, only protocol.
Any client or server realization is easy based on current code, but requires transport libraries.

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

See `examples <https://github.com/Orhideous/json-rpc/tree/master/examples>`_.