Jinja2 Standalone Compiler
===========================

This provides a silly way to create HTML templates based on Jinja2 ones without a framework.

This aims to be stupidly simple - in order to be used to whom have never heard about python before.

The least you should do to work with this is learn a bit of `Jinja2 <http://jinja.pocoo.org/>`_. Do it now, you won't regret. =)

Ah! This project works well on both Python2 and Python3.

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

* For a more intense usage, you can also use a settings file to define a bunch of things. To use settings file:

    .. code:: bash

        jinja2_standalone_compiler <path-to-jinja-files> --settings=path/to/settings.py

  * You can also use -s instead of --settings
  * Please note that settings file is a Python file, so Python syntax applies. =P
  * It's also possible to use multiple settings files, so that a template will be rendered multiple times with a different setup: -s <settings-1> -s <settings-2> ...
  * In order to see what can be done with this settings file, please refer to `this example <https://github.com/filwaitman/jinja2-standalone-compiler/blob/master/settings_example.py>`_

* To turn off console ouput you can use the following option:

    .. code:: bash

        jinja2_standalone_compiler <path-to-jinja-files> --silent

* Or if you want to get more console ouput:

    .. code:: bash

        jinja2_standalone_compiler <path-to-jinja-files> --verbose

* You can also specify an alternative output directory instead putting the rendered templates into the same directory as the jinja files. The relative directory structure (if present) will be reconstructed inside the new ouput. The ouput directory will be created if it doesn't exist:

    .. code:: bash

        jinja2_standalone_compiler <path-to-jinja-files> --out=<path-to-output-dir>

  * You can also use -o instead of --out

Contribute
----------
Did you think in some interesting feature, or have you found a bug? Please let me know!

Of course you can also download the project and send me some `pull requests <https://github.com/filwaitman/jinja2-standalone-compiler/pulls>`_.


You can send your suggestions by `opening issues <https://github.com/filwaitman/jinja2-standalone-compiler/issues>`_.

You can contact me directly as well. Take a look at my contact information at `http://filwaitman.github.io/ <http://filwaitman.github.io/>`_ (email is preferred rather than mobile phone).
