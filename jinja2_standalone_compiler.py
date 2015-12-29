#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from settings import INPUT_FOLDER, OUTPUT_FOLDER, OUTPUT_TEMPLATES, EXTRA_VARIABLES


def compile_template(skeleton_path):
    '''Returns a string with its generated content.

    :param skeleton_path: template basis to be used to render final template.  Use relative path, (from INPUT_FOLDER on)
    :type skeleton_path: str or unicode
    :returns: formatted string
    :rtype: str or unicode
    '''
    environment = Environment(loader=FileSystemLoader([INPUT_FOLDER]), trim_blocks=True, lstrip_blocks=True)
    environment.undefined = StrictUndefined
    template = environment.get_template(skeleton_path)
    return template.render(EXTRA_VARIABLES)


def main():
    for jinja_template in OUTPUT_TEMPLATES:
        template_name, _ = os.path.splitext(jinja_template)
        template_name = os.path.join(OUTPUT_FOLDER, '%s.html' % template_name)

        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)

        with open(template_name, 'w') as f:
            f.write(compile_template(jinja_template).encode('utf-8'))


if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print 'ERROR: %s' % str(e)
    else:
        print 'Done!'
    raw_input('Press any key to continue...')
