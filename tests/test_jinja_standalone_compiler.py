from __future__ import unicode_literals
from collections import namedtuple
import fnmatch
import os
import unittest

from jinja2 import UndefinedError

from jinja2_standalone_compiler import main

fixtures_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')


class MainTestCase(unittest.TestCase):
    def tearDown(self):
        for root, dirnames, filenames in os.walk(fixtures_dir):
            for filename in fnmatch.filter(filenames, '*.html'):
                os.unlink(os.path.join(root, filename))

    def test_extends(self):
        self.assertFalse(os.path.exists(os.path.join(fixtures_dir, 'child_base', 'child.html')))
        main(os.path.join(fixtures_dir, 'child_base'))
        self.assertTrue(os.path.exists(os.path.join(fixtures_dir, 'child_base', 'child.html')))

        file_content = open(os.path.join(fixtures_dir, 'child_base', 'child.html')).read()
        self.assertEquals(file_content, 'begin parent\nparent content\n\nchild content\nend parent')

    def test_extends_and_include(self):
        self.assertFalse(os.path.exists(os.path.join(fixtures_dir, 'header_footer', 'child.html')))
        main(os.path.join(fixtures_dir, 'header_footer'))
        self.assertTrue(os.path.exists(os.path.join(fixtures_dir, 'header_footer', 'child.html')))

        file_content = open(os.path.join(fixtures_dir, 'header_footer', 'child.html')).read()
        self.assertEquals(file_content, 'header!\nbegin parent\nparent content\n\nchild content\nend parent\nfooter!')

    def test_extends_and_include_and_custom_vars(self):
        Settings = namedtuple('Settings', ['EXTRA_VARIABLES'])
        settings = Settings(EXTRA_VARIABLES={'number': 42, 'triplicate': lambda x: x * 3})

        self.assertFalse(os.path.exists(os.path.join(fixtures_dir, 'custom_vars', 'child.html')))
        main(os.path.join(fixtures_dir, 'custom_vars'), settings=settings)
        self.assertTrue(os.path.exists(os.path.join(fixtures_dir, 'custom_vars', 'child.html')))

        file_content = open(os.path.join(fixtures_dir, 'custom_vars', 'child.html')).read()
        self.assertEquals(file_content, 'header!\nbegin parent\nparent content\n\nchild content\nworks! works! works! '
                                        '\n42 * 2 = 84\nend parent\nfooter!')

    def test_ignore_jinja_templates(self):
        Settings = namedtuple('Settings', ['IGNORE_JINJA_TEMPLATES'])
        settings = Settings(IGNORE_JINJA_TEMPLATES=['.*base.jinja', ])

        self.assertFalse(os.path.exists(os.path.join(fixtures_dir, 'header_footer', 'child.html')))
        self.assertFalse(os.path.exists(os.path.join(fixtures_dir, 'header_footer', 'base.html')))
        main(os.path.join(fixtures_dir, 'header_footer'), settings=settings)
        self.assertTrue(os.path.exists(os.path.join(fixtures_dir, 'header_footer', 'child.html')))
        self.assertFalse(os.path.exists(os.path.join(fixtures_dir, 'header_footer', 'base.html')))

    def test_undefined_vars_raises_errors(self):
        Settings = namedtuple('Settings', ['EXTRA_VARIABLES'])
        settings = Settings(EXTRA_VARIABLES={'name': 'Filipe Waitman'})

        self.assertFalse(os.path.exists(os.path.join(fixtures_dir, 'undefined_vars', 'child.html')))
        self.assertRaises(UndefinedError, main, path=os.path.join(fixtures_dir, 'undefined_vars'))
        self.assertFalse(os.path.exists(os.path.join(fixtures_dir, 'undefined_vars', 'child.html')))

        self.assertFalse(os.path.exists(os.path.join(fixtures_dir, 'undefined_vars', 'child.html')))
        main(os.path.join(fixtures_dir, 'undefined_vars'), settings=settings)
        self.assertTrue(os.path.exists(os.path.join(fixtures_dir, 'undefined_vars', 'child.html')))
