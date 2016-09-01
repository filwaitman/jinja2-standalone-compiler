# -*- coding: utf-8 -*-
import fnmatch
import imp
import os
import re
import sys
import click
from colorama import init, Fore, Style
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from jinja2.defaults import (
    BLOCK_START_STRING, BLOCK_END_STRING, VARIABLE_START_STRING, VARIABLE_END_STRING, COMMENT_START_STRING,
    COMMENT_END_STRING, LINE_STATEMENT_PREFIX, LINE_COMMENT_PREFIX, NEWLINE_SEQUENCE, KEEP_TRAILING_NEWLINE
)

# Globals
global_silent = False
global_verbose = False


def print_log(msg, verbose_msg=False):
    if not global_silent and ((verbose_msg and global_verbose) or not verbose_msg):
        print msg


def render_template(jinja_template, extra_variables, output_options, jinja_environment):
    environment = Environment(
        loader=FileSystemLoader([os.path.dirname(jinja_template)]),
        block_start_string=jinja_environment.get('BLOCK_START_STRING', BLOCK_START_STRING),
        block_end_string=jinja_environment.get('BLOCK_END_STRING', BLOCK_END_STRING),
        variable_start_string=jinja_environment.get('VARIABLE_START_STRING', VARIABLE_START_STRING),
        variable_end_string=jinja_environment.get('VARIABLE_END_STRING', VARIABLE_END_STRING),
        comment_start_string=jinja_environment.get('COMMENT_START_STRING', COMMENT_START_STRING),
        comment_end_string=jinja_environment.get('COMMENT_END_STRING', COMMENT_END_STRING),
        line_statement_prefix=jinja_environment.get('LINE_STATEMENT_PREFIX', LINE_STATEMENT_PREFIX),
        line_comment_prefix=jinja_environment.get('LINE_COMMENT_PREFIX', LINE_COMMENT_PREFIX),
        trim_blocks=jinja_environment.get('TRIM_BLOCKS', True),
        lstrip_blocks=jinja_environment.get('LSTRIP_BLOCKS', True),
        newline_sequence=jinja_environment.get('NEWLINE_SEQUENCE', NEWLINE_SEQUENCE),
        keep_trailing_newline=jinja_environment.get('KEEP_TRAILING_NEWLINE', KEEP_TRAILING_NEWLINE)
    )
    environment.undefined = StrictUndefined
    template = environment.get_template(os.path.basename(jinja_template))
    return template.render(extra_variables)


def main(path, out_path=None, settings=None):
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
        print_log('  Looking for jinja templates in: {}{}'.format(Fore.MAGENTA, path))
        jinja_templates = []
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.jinja*'):
                jinja_templates.append(os.path.join(root, filename))
    else:
        jinja_templates = [path, ]  # path is just a file, actually

    print_log('  Jinja files found: {}{}'.format(Fore.MAGENTA, len(jinja_templates)))

    for jinja_template in jinja_templates:
        print_log('   Processing:' + Fore.MAGENTA + jinja_template)

        skip = False
        for jinja_template_to_be_ignored in ignore_jinja_templates:
            if re.match(jinja_template_to_be_ignored, jinja_template):
                print_log('    Skipping: ' + Fore.YELLOW + Style.BRIGHT + jinja_template)
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
                    raise IOError(u'Cannot create sub output directory: {}'.format(template_dir))

            template_file, _ = os.path.splitext(template_file)
        else:
            template_file, _ = os.path.splitext(jinja_template)

        template_file = os.path.abspath(template_file)

        if output_options.get('remove_double_extension', False):
            template_file, _ = os.path.splitext(template_file)

        template_file = '{}{}'.format(template_file, output_options.get('extension', '.html'))

        print_log('    Creating: ' + Fore.CYAN + template_file)

        try:
            with open(template_file, 'w') as f:
                print_log('     EXTRA_VARIABLES  : {}'.format(extra_variables), True)
                print_log('     OUTPUT_OPTIONS   : {}'.format(output_options), True)
                print_log('     JINJA_ENVIRONMENT: {}'.format(jinja_environment), True)
                f.write(render_template(
                    jinja_template,
                    extra_variables=extra_variables,
                    output_options=output_options,
                    jinja_environment=jinja_environment
                ).encode('utf-8'))
        except:
            os.unlink(template_file)
            raise


@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--settings', '-s', default=None, multiple=True, help='Settings file to use.')
@click.option('--out', '-o', type=click.Path(exists=False, file_okay=False, dir_okay=True), default=None, help='Output path to use.')
@click.option('--verbose', is_flag=True, default=False, help='Detailed command line output')
@click.option('--silent', is_flag=True, default=False, help='Suppress command line output')
def main_command(path, settings=None, out=None, verbose=False, silent=False):
    init(autoreset=True)  # Init colorama
    current_dir = os.getcwd()

    global_silent = silent
    global_verbose = verbose

    if out and not os.path.exists(out):
        out = os.path.normpath(out)
        try:
            os.makedirs(out)
        except:
            raise IOError(u'Cannot create output directory: {}'.format(out))

    if settings:
        if not silent:
            print_log('{}Number of specified settings files: {}'.format(Fore.GREEN, len(settings)))
        for setting in settings:
            settings_file = os.path.normpath(os.path.join(current_dir, setting))
            if not os.path.exists(settings_file):
                raise IOError(u'Settings file not found: {}'.format(settings_file))
            else:
                if not silent:
                    print_log(' Using settings file: ' + Fore.CYAN + settings_file)
            sys.path.insert(0, '')
            setting = imp.load_source(current_dir, setting)
            work_dir = os.path.normpath(os.path.join(current_dir, path))

            main(work_dir, out, setting)

            print_log(Fore.GREEN + ' Done.')
    else:
        work_dir = os.path.join(current_dir, path)

        main(work_dir, out)

    print_log(Fore.GREEN + Style.BRIGHT + 'All done.')
