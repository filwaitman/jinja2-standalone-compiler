# jinja2-standalone-compiler

This provides a silly way to create HTML templates based on JINJA2 ones without a framework.  
This aims to be stupidly simple - in order to be used to whom have never heard about python before.  

### This is:
* a way to use jinja2 outside python frameworks.
* a way to use jinja2 not knowing anything in python.

### This is not:
* another templating language for python. Jinja2 is good enough.  =)

### Installation:
* `git clone https://github.com/filwaitman/jinja2-standalone-compiler.git`
* `cd jinja2-standalone-compiler`
* `python setup.py install`

### Usage:
* edit `settings.py` file:
  * in `OUTPUT_TEMPLATES` put the jinja templates you want to export. This is the only setting required.
  * (optional) in `INPUT_FOLDER` put the directory path to your jinja files.
  * (optional) in `OUTPUT_FOLDER` put the directory path to your generated html files.
* `python jinja2_standalone_compiler.py`

### Run tests:
* `pip install -r requirements_test.txt`
* `PYTHONPATH=.. py.test`
