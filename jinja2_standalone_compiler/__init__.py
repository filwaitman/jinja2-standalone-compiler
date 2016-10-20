from __future__ import unicode_literals, print_function
import argparse
import fnmatch
import imp
import os
import re
import sys

from jinja2 import Environment, FileSystemLoader, StrictUndefined, defaults

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    using_colorama = True

    style_JINJA_FILE = Fore.MAGENTA
    style_WARNING = Fore.YELLOW + Style.BRIGHT
    style_SETTING = Fore.CYAN
    style_RENDERED_FILE = Fore.CYAN
    style_SUCCESS = Fore.GREEN
    style_ALL_DONE = Fore.GREEN + Style.BRIGHT

except:
    using_colorama = False

    style_JINJA_FILE = ''
    style_WARNING = ''
    style_SETTING = ''
    style_RENDERED_FILE = ''
    style_SUCCESS = ''
    style_ALL_DONE = ''


def print_log(msg, verbose_msg=False, verbose=False, silent=False):
    if silent:
        return

    if not verbose and verbose_msg:
        return

    print(msg)


def render_template(jinja_template, extra_variables, output_options, jinja_environment):
    environment = Environment(
        loader=FileSystemLoader([os.path.dirname(jinja_template)]),
        block_start_string=jinja_environment.get('BLOCK_START_STRING', defaults.BLOCK_START_STRING),
        block_end_string=jinja_environment.get('BLOCK_END_STRING', defaults.BLOCK_END_STRING),
        variable_start_string=jinja_environment.get('VARIABLE_START_STRING', defaults.VARIABLE_START_STRING),
        variable_end_string=jinja_environment.get('VARIABLE_END_STRING', defaults.VARIABLE_END_STRING),
        comment_start_string=jinja_environment.get('COMMENT_START_STRING', defaults.COMMENT_START_STRING),
        comment_end_string=jinja_environment.get('COMMENT_END_STRING', defaults.COMMENT_END_STRING),
        line_statement_prefix=jinja_environment.get('LINE_STATEMENT_PREFIX', defaults.LINE_STATEMENT_PREFIX),
        line_comment_prefix=jinja_environment.get('LINE_COMMENT_PREFIX', defaults.LINE_COMMENT_PREFIX),
        trim_blocks=jinja_environment.get('TRIM_BLOCKS', True),
        lstrip_blocks=jinja_environment.get('LSTRIP_BLOCKS', True),
        newline_sequence=jinja_environment.get('NEWLINE_SEQUENCE', defaults.NEWLINE_SEQUENCE),
        keep_trailing_newline=jinja_environment.get('KEEP_TRAILING_NEWLINE', defaults.KEEP_TRAILING_NEWLINE)
    )
    environment.undefined = StrictUndefined
    template = environment.get_template(os.path.basename(jinja_template))
    return template.render(extra_variables)


def main(path, out_path=None, verbose=False, silent=False, settings=None):
    extra_variables = {}
    ignore_jinja_templates = []
    output_options = {}
    jinja_environment = {}
    if settings:
        extra_variables = getattr(settings, 'EXTRA_VARIABLES', {})
        ignore_jinja_templates = getattr(settings, 'IGNORE_JINJA_TEMPLATES', [])
        output_options = getattr(settings, 'OUTPUT_OPTIONS', {})
        jinja_environment = getattr(settings, 'JINJA_ENVIRONMENT', {})

    print_log('Additional context and options:', True, verbose, silent)
    print_log('  EXTRA_VARIABLES  : {}'.format(extra_variables), True, verbose, silent)
    print_log('  OUTPUT_OPTIONS   : {}'.format(output_options), True, verbose, silent)
    print_log('  JINJA_ENVIRONMENT: {}'.format(jinja_environment), True, verbose, silent)

    if os.path.isdir(path):
        print_log('Looking for jinja templates in: {}{}'.format(style_JINJA_FILE, path), False, verbose, silent)
        jinja_templates = []
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.jinja*'):
                jinja_templates.append(os.path.join(root, filename))
    else:
        jinja_templates = [path, ]  # path is just a file, actually

    print_log('  Jinja files found: {}{}'.format(style_JINJA_FILE, len(jinja_templates)), False, verbose, silent)

    for jinja_template in jinja_templates:
        print_log('Processing:' + style_JINJA_FILE + jinja_template, False, verbose, silent)

        skip = False
        for jinja_template_to_be_ignored in ignore_jinja_templates:
            if re.match(jinja_template_to_be_ignored, jinja_template):
                print_log('  Skipping: ' + style_WARNING + jinja_template, False, verbose, silent)
                skip = True
                break

        if skip:
            continue

        if out_path:
            rel_path = os.path.relpath(jinja_template, path)
            if rel_path == '.':
                rel_path = os.path.basename(path)
            template_file = os.path.join(out_path, rel_path)

            template_dir = os.path.dirname(template_file)
            if not os.path.exists(template_dir):
                try:
                    os.makedirs(template_dir)
                except:
                    raise IOError('Cannot create sub output directory: {}'.format(template_dir))

            template_file, _ = os.path.splitext(template_file)
        else:
            template_file, _ = os.path.splitext(jinja_template)

        template_file = os.path.abspath(template_file)

        if output_options.get('remove_double_extension', False):
            template_file, _ = os.path.splitext(template_file)

        template_file = '{}{}'.format(template_file, output_options.get('extension', '.html'))

        print_log('  Creating: ' + style_RENDERED_FILE + template_file, False, verbose, silent)

        try:
            with open(template_file, 'w') as f:
                f.write(render_template(
                    jinja_template,
                    extra_variables=extra_variables,
                    output_options=output_options,
                    jinja_environment=jinja_environment
                ))
        except:
            os.unlink(template_file)
            raise


def _first_set(*values):
    for value in values:
        if value is not None:
            return value


def main_command(path=None, settings=None, out=None, verbose=None, silent=None):
    has_path = bool(path)
    path_help = '{}Path to base files.'.format('' if has_path else '[REQUIRED] ')

    parser = argparse.ArgumentParser(description='jinja2_standalone_compiler')
    parser.add_argument('--path', dest='path', help=path_help, required=not(has_path))
    parser.add_argument('--settings', '-s', dest='settings', action='append', nargs=1, help='Settings file(s) to use.')
    parser.add_argument('--out', '-o', dest='out', help='Output path.')
    parser.add_argument('--verbose', dest='verbose', help='Detailed output.', action='store_true', default=False)
    parser.add_argument('--silent', dest='silent', help='Suppress output.', action='store_true', default=False)
    args = parser.parse_args()

    args_settings = None
    if args.settings:
        args_settings = [x[0] for x in args.settings]

    path = _first_set(path, args.path)
    settings = _first_set(settings, args_settings)
    out = _first_set(out, args.out)
    verbose = _first_set(verbose, args.verbose)
    silent = _first_set(silent, args.silent)

    current_dir = os.getcwd()

    if not using_colorama and not silent:
        print("<optional dependency 'colorama' not found, try 'pip install colorama==0.3.7' to see colored output>")

    if out and not os.path.exists(out):
        out = os.path.normpath(out)
        try:
            os.makedirs(out)
        except:
            raise IOError('Cannot create output directory: {}'.format(out))

    if settings:
        if not silent:
            print_log('{}Number of settings files: {}'.format(style_SUCCESS, len(settings)), False, verbose, silent)

        for setting in settings:
            settings_file = os.path.normpath(os.path.join(current_dir, setting))
            if not os.path.exists(settings_file):
                raise IOError('Settings file not found: {}'.format(settings_file))
            else:
                if not silent:
                    print_log('Using settings file: ' + style_SETTING + settings_file, False, verbose, silent)

            sys.path.insert(0, '')
            setting = imp.load_source(current_dir, setting)
            work_dir = os.path.normpath(os.path.join(current_dir, path))

            main(work_dir, out, verbose, silent, setting)

            print_log(style_SUCCESS + 'Done.', False, verbose, silent)

    else:
        work_dir = os.path.join(current_dir, path)

        main(work_dir, out, verbose, silent)

    print_log(style_ALL_DONE + 'All done.', False, verbose, silent)
