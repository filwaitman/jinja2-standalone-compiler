# -*- coding: utf-8 -*-
import fnmatch
import imp
import os
import re
import sys

import click
from jinja2 import Environment, FileSystemLoader, StrictUndefined


def render_template(jinja_template, extra_variables):
    print '    TEMPLATE', jinja_template
    print '    EXTRA', extra_variables

    environment = Environment(loader=FileSystemLoader([os.path.dirname(jinja_template)]), trim_blocks=True, lstrip_blocks=True)
    environment.undefined = StrictUndefined
    template = environment.get_template(os.path.basename(jinja_template))
    return template.render(extra_variables)


def main(settings=None, path=None):
    extra_variables = {}
    ignore_jinja_templates = []
    if settings:
        extra_variables = getattr(settings, 'EXTRA_VARIABLES', {})
        ignore_jinja_templates = getattr(settings, 'IGNORE_JINJA_TEMPLATES', [])

    jinja_templates = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*.jinja*'):
            jinja_templates.append(os.path.join(root, filename))

    for jinja_template in jinja_templates:
        skip = False
        for jinja_template_to_be_ignored in ignore_jinja_templates:
            if re.match(jinja_template_to_be_ignored, jinja_template):
                print 'SKIP', jinja_template
                skip = True
                break

        if skip:
            continue

        html_template, _ = os.path.splitext(jinja_template)
        html_template = '{}.html'.format(html_template)

        print 'DOING', html_template
        with open(html_template, 'w') as f:
            f.write(render_template(jinja_template, extra_variables=extra_variables).encode('utf-8'))


@click.command()
@click.option('--settings', default=None, help='Settings file to use')
@click.option('--path', default=None, help='The person to greet.')
def main_command(settings=None, path=None):
    current_dir = os.getcwd()

    if settings:
        settings_file = os.path.join(current_dir, settings)
        if not os.path.exists(settings_file):
            raise IOError(u'Settings file not found: {}'.format(settings_file))

        sys.path.insert(0, '')
        settings = imp.load_source(current_dir, settings)

    if path:
        current_dir = os.path.join(current_dir, path)

    main(settings=settings, path=current_dir)


if __name__ == '__main__':
    main()
