.. image:: https://travis-ci.org/yongjhih/enforcer.svg?branch=master
    :target: https://travis-ci.org/yongjhih/enforcer
    :alt: Build Status

Usage
-----

For example:

.. code:: python

    @enforce
    def safe_doubler(x):
        y: int = x * 2
        return y

    def unsafe_doubler(x):
        y: int = x * 2
        return y


Installation
------------

.. code:: sh

    python3 -m venv .venv && . .venv/bin/activate
    pip install git+git://github.com/yongjhih/enforcer.git

Test
-----

.. code:: sh

    pytest

Credit
------

* https://gist.github.com/bheklilr/372dc851ba085c4f943f116e41888fcf
