# -*- coding: utf-8 -*-
import fnmatch
import imp
import os
import re
import sys

import click
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from jinja2.defaults import (
    BLOCK_START_STRING, BLOCK_END_STRING, VARIABLE_START_STRING, VARIABLE_END_STRING, COMMENT_START_STRING,
    COMMENT_END_STRING, LINE_STATEMENT_PREFIX, LINE_COMMENT_PREFIX, NEWLINE_SEQUENCE, KEEP_TRAILING_NEWLINE
)


def render_template(jinja_template, extra_variables, output_options, jinja_environment):
    environment = Environment(
        loader=FileSystemLoader([os.path.dirname(jinja_template)]),
        block_start_string=jinja_environment.get(
            'BLOCK_START_STRING', BLOCK_START_STRING),
        block_end_string=jinja_environment.get(
            'BLOCK_END_STRING', BLOCK_END_STRING),
        variable_start_string=jinja_environment.get(
            'VARIABLE_START_STRING', VARIABLE_START_STRING),
        variable_end_string=jinja_environment.get(
            'VARIABLE_END_STRING', VARIABLE_END_STRING),
        comment_start_string=jinja_environment.get(
            'COMMENT_START_STRING', COMMENT_START_STRING),
        comment_end_string=jinja_environment.get(
            'COMMENT_END_STRING', COMMENT_END_STRING),
        line_statement_prefix=jinja_environment.get(
            'LINE_STATEMENT_PREFIX', LINE_STATEMENT_PREFIX),
        line_comment_prefix=jinja_environment.get(
            'LINE_COMMENT_PREFIX', LINE_COMMENT_PREFIX),
        trim_blocks=jinja_environment.get('TRIM_BLOCKS', True),
        lstrip_blocks=jinja_environment.get('LSTRIP_BLOCKS', True),
        newline_sequence=jinja_environment.get(
            'NEWLINE_SEQUENCE', NEWLINE_SEQUENCE),
        keep_trailing_newline=jinja_environment.get(
            'KEEP_TRAILING_NEWLINE', KEEP_TRAILING_NEWLINE)
    )
    environment.undefined = StrictUndefined
    template = environment.get_template(os.path.basename(jinja_template))
    return template.render(extra_variables)


def main(path, settings=None, out_path=None, verbose=False, silent=False):
    extra_variables = {}
    ignore_jinja_templates = []
    output_options = {}
    jinja_environment = {}
    if settings:
        extra_variables = getattr(settings, 'EXTRA_VARIABLES', {})
        ignore_jinja_templates = getattr(
            settings, 'IGNORE_JINJA_TEMPLATES', [])
        output_options = getattr(settings, 'OUTPUT_OPTIONS', {})
        jinja_environment = getattr(settings, 'JINJA_ENVIRONMENT', {})

    if os.path.isdir(path):
        if not silent:
            print 'Looking for jinja templates in:', path
        jinja_templates = []
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.jinja*'):
                jinja_templates.append(os.path.join(root, filename))
    else:
        jinja_templates = [path, ]  # path is just a file, actually

    if not silent:
        print 'Jinja files found:', len(jinja_templates)
    for jinja_template in jinja_templates:
        if not silent:
            print 'Processing:', jinja_template
        skip = False
        for jinja_template_to_be_ignored in ignore_jinja_templates:
            if re.match(jinja_template_to_be_ignored, jinja_template):
                if not silent:
                    print '  Skipping:', jinja_template
                skip = True
                break

        if skip:
            continue

        if out_path:
            rel_path = os.path.relpath(jinja_template, path)
            template_file = os.path.join(out_path, rel_path)
            template_dir = os.path.dirname(template_file)
            if not os.path.exists(template_dir):
                try:
                    os.makedirs(template_dir)
                except:
                    raise IOError(
                        u'Cannot create sub ouput directory: {}'.format(template_dir))
            template_file, _ = os.path.splitext(template_file)
        else:
            template_file, _ = os.path.splitext(jinja_template)

        if output_options.get('remove_double_extension', False):
            template_file, _ = os.path.splitext(template_file)
        template_file = '{}{}'.format(
            template_file, output_options.get('extension', '.html'))

        if not silent:
            print '  Creating:', template_file
        try:
            with open(template_file, 'w') as f:
                if not silent and verbose:
                    print '    Base template      :', jinja_template
                    print '      EXTRA_VARIABLES  :', extra_variables
                    print '      OUTPUT_OPTIONS   :', output_options
                    print '      JINJA_ENVIRONMENT:', jinja_environment
                f.write(render_template(
                    jinja_template,
                    extra_variables=extra_variables,
                    output_options=output_options,
                    jinja_environment=jinja_environment
                ).encode('utf-8'))
        except:
            os.unlink(template_file)
            raise

    if not silent:
        print 'Done!'


@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--settings', default=None, help='Settings file to use.')
@click.option('--out', type=click.Path(exists=False, file_okay=False, dir_okay=True), default=None, help='Output path to use.')
@click.option('--verbose', is_flag=True, default=False, help='Detailed command line output')
@click.option('--silent', is_flag=True, default=False, help='Suppress command line output')
def main_command(path, settings=None, out=None, verbose=False, silent=False):
    current_dir = os.getcwd()

    if settings:
        settings_file = os.path.join(current_dir, settings)
        if not os.path.exists(settings_file):
            raise IOError(u'Settings file not found: {}'.format(settings_file))

        sys.path.insert(0, '')
        settings = imp.load_source(current_dir, settings)

    current_dir = os.path.join(current_dir, path)

    if out and not os.path.exists(out):
        try:
            os.makedirs(out)
        except:
            raise IOError(u'Cannot create ouput directory: {}'.format(out))

    main(settings=settings, path=current_dir,
         out_path=out, verbose=verbose, silent=silent)
