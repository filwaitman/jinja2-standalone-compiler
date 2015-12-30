Jinja2 Standalone Compiler
===========================

This provides a silly way to create HTML templates based on Jinja2 ones without a framework.

This aims to be stupidly simple - in order to be used to whom have never heard about python before.

The least you should do to work with this is learn a bit of `Jinja2 <http://jinja.pocoo.org/>`_. Do it now, you won't regret. =)

This is:
-------------
* a way to use Jinja2 outside python frameworks.
* a way to use Jinja2 not knowing anything in python.

This is not:
-------------
* another templating language for python. Jinja2 is good enough.  =)

Installation:
-------------
.. code:: bash

    pip install jinja2-standalone-compiler


Usage:
-------------
.. code:: bash

    jinja2_standalone_compiler <path-to-jinja-files>  # Note that jinja files will be searched recursively

For a more intense usage, you can also use a settings file to define a bunch of things. To use settings file:

.. code:: bash

    jinja2_standalone_compiler <path-to-jinja-files> --settings=path/to/settings.py

Please note that settings file is a Python file, so Python syntax applies. =P

In order to see what can be done with this settings file, please refer to `this example <https://github.com/filwaitman/jinja2-standalone-compiler/blob/master/settings_example.py>`_
