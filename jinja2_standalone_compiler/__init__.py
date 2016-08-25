# -*- coding: utf-8 -*-
import fnmatch
import imp
import os
import re
import sys

import click
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from jinja2.defaults import BLOCK_START_STRING, \
     BLOCK_END_STRING, VARIABLE_START_STRING, VARIABLE_END_STRING, \
     COMMENT_START_STRING, COMMENT_END_STRING, LINE_STATEMENT_PREFIX, \
     LINE_COMMENT_PREFIX, NEWLINE_SEQUENCE, KEEP_TRAILING_NEWLINE


def render_template(jinja_template, extra_variables, output_options, jinja_environment):
    print '    BASE TEMPLATE    :', jinja_template
    print '    EXTRA VARS       :', extra_variables
    print '    OUTPUT OPTIONS   :', output_options
    print '    JINJA ENVIRONMENT:', jinja_environment

    environment = Environment(loader=FileSystemLoader([os.path.dirname(jinja_template)]),
                              block_start_string = jinja_environment.get('BLOCK_START_STRING', BLOCK_START_STRING),
                              block_end_string = jinja_environment.get('BLOCK_END_STRING', BLOCK_END_STRING),
                              variable_start_string = jinja_environment.get('VARIABLE_START_STRING', VARIABLE_START_STRING),
                              variable_end_string = jinja_environment.get('VARIABLE_END_STRING', VARIABLE_END_STRING),
                              comment_start_string = jinja_environment.get('COMMENT_START_STRING', COMMENT_START_STRING),
                              comment_end_string = jinja_environment.get('COMMENT_END_STRING', COMMENT_END_STRING),
                              line_statement_prefix = jinja_environment.get('LINE_STATEMENT_PREFIX', LINE_STATEMENT_PREFIX),
                              line_comment_prefix = jinja_environment.get('LINE_COMMENT_PREFIX', LINE_COMMENT_PREFIX),
                              trim_blocks = jinja_environment.get('TRIM_BLOCKS', True),
                              lstrip_blocks = jinja_environment.get('LSTRIP_BLOCKS', True),
                              newline_sequence = jinja_environment.get('NEWLINE_SEQUENCE', NEWLINE_SEQUENCE),
                              keep_trailing_newline = jinja_environment.get('KEEP_TRAILING_NEWLINE', KEEP_TRAILING_NEWLINE))
    environment.undefined = StrictUndefined
    template = environment.get_template(os.path.basename(jinja_template))
    return template.render(extra_variables)


def main(path, settings=None):
    extra_variables = {}
    ignore_jinja_templates = []
    output_options = {}
    jinja_environment = {}
    if settings:
        extra_variables = getattr(settings, 'EXTRA_VARIABLES', {})
        ignore_jinja_templates = getattr(settings, 'IGNORE_JINJA_TEMPLATES', [])
        output_options = getattr(settings, 'OUTPUT_OPTIONS', {})
        jinja_environment = getattr(settings, 'JINJA_ENVIRONMENT', {})

    if os.path.isdir(path):
        jinja_templates = []
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.jinja*'):
                jinja_templates.append(os.path.join(root, filename))
    else:
        jinja_templates = [path, ]  # path is just a file, actually

    for jinja_template in jinja_templates:
        skip = False
        for jinja_template_to_be_ignored in ignore_jinja_templates:
            if re.match(jinja_template_to_be_ignored, jinja_template):
                print 'SKIPPING:', jinja_template
                skip = True
                break

        if skip:
            continue

        html_template, _ = os.path.splitext(jinja_template)
        if output_options.get('remove_double_extension', False):
            html_template, _ = os.path.splitext(html_template)
        html_template = '{}{}'.format(html_template, output_options.get('extension', '.html'))

        print 'CREATING:', html_template
        try:
            with open(html_template, 'w') as f:
                f.write(render_template(jinja_template, extra_variables=extra_variables, output_options=output_options, jinja_environment=jinja_environment).encode('utf-8'))
        except:
            os.unlink(html_template)
            raise

    print 'DONE!  =]'


@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--settings', default=None, help='Settings file to use.')
def main_command(path, settings=None):
    current_dir = os.getcwd()

    if settings:
        settings_file = os.path.join(current_dir, settings)
        if not os.path.exists(settings_file):
            raise IOError(u'Settings file not found: {}'.format(settings_file))

        sys.path.insert(0, '')
        settings = imp.load_source(current_dir, settings)

    current_dir = os.path.join(current_dir, path)
    main(settings=settings, path=current_dir)
