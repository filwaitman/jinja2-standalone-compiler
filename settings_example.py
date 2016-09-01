# -*- coding: utf-8 -*-

# Which templates don't you want to generate? (You can use regular expressions here!)
# Use strings (with single or double quotes), and separate each template/regex in a line terminated with a comma.
IGNORE_JINJA_TEMPLATES = [
    '.*base.jinja',
    '.*tests/.*'
]

# Here you can override the default jinja environment setup
JINJA_ENVIRONMENT = {
   # 'BLOCK_START_STRING': '{%',
   # 'BLOCK_END_STRING': '%}',
   # 'VARIABLE_START_STRING': '{{',
   # 'VARIABLE_END_STRING': '}}',
   # 'COMMENT_START_STRING': '{#',
   # 'COMMENT_END_STRING': '#}',
   # 'LINE_STATEMENT_PREFIX': None,
   # 'LINE_COMMENT_PREFIX': None,
   # 'TRIM_BLOCKS': True, # Jinja default is False
   # 'LSTRIP_BLOCKS': True, #Jinja default is False
   # 'NEWLINE_SEQUENCE': '\n',
   # 'KEEP_TRAILING_NEWLINE': False
}

# Do you have any additional variables to the templates? Put 'em here! (use dictionary ('key': value) format)
EXTRA_VARIABLES = {
    'project_name': 'WaitCorp',
    'current_year': 2042,
    'debug': False,
    'triplicate': lambda x: x * 3
}

OUTPUT_OPTIONS = {
    'extension': '.html',  # Including leading '.'
    'remove_double_extension': False  # If you use something like sample.jinja.html
}
