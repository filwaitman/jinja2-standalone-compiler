#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fnmatch
import os

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from settings import EXTRA_VARIABLES


def render_template(jinja_template):
    '''Returns a string with its generated content.

    :param jinja_template: template basis to be used to render final template.  Use relative path, (from INPUT_FOLDER on)
    :type jinja_template: str or unicode
    :returns: formatted string
    :rtype: str or unicode
    '''
    environment = Environment(loader=FileSystemLoader([os.path.dirname(jinja_template)]), trim_blocks=True, lstrip_blocks=True)
    environment.undefined = StrictUndefined
    template = environment.get_template(os.path.basename(jinja_template))
    return template.render(EXTRA_VARIABLES)


def main():
    current_dir = os.path.dirname(os.path.realpath(__file__))

    jinja_templates = []
    for root, dirnames, filenames in os.walk(current_dir):
        for filename in fnmatch.filter(filenames, '*.jinja*'):
            jinja_templates.append(os.path.join(root, filename))

    for jinja_template in jinja_templates:
        html_template, _ = os.path.splitext(jinja_template)
        html_template = '{}.html'.format(html_template)

        with open(html_template, 'w') as f:
            f.write(render_template(jinja_template).encode('utf-8'))


if __name__ == '__main__':
    main()
