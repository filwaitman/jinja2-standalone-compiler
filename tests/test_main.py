# -*- coding: utf-8 -*-
import os
import shutil

import settings, jinja2_standalone_compiler

fixtures_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')


def test_child_base_inheritance(monkeypatch):
    monkeypatch.setattr(jinja2_standalone_compiler, 'INPUT_FOLDER', os.path.join(fixtures_dir, 'child_base'))
    monkeypatch.setattr(jinja2_standalone_compiler, 'OUTPUT_FOLDER', os.path.join(fixtures_dir, 'child_base_generated'))
    monkeypatch.setattr(jinja2_standalone_compiler, 'OUTPUT_TEMPLATES', ['child.jinja'])

    if os.path.exists(os.path.join(fixtures_dir, 'child_base_generated')):
        shutil.rmtree(os.path.join(fixtures_dir, 'child_base_generated'))

    assert not os.path.exists(os.path.join(fixtures_dir, 'child_base_generated'))

    jinja2_standalone_compiler.main()

    assert os.path.exists(os.path.join(fixtures_dir, 'child_base_generated'))
    assert os.path.exists(os.path.join(fixtures_dir, 'child_base_generated', 'child.html'))
    file_content = open(os.path.join(fixtures_dir, 'child_base_generated', 'child.html')).read()
    assert file_content == 'begin parent\nparent content\n\nchild content\nend parent'


def test_child_base_inheritance_with_header_and_footer(monkeypatch):
    monkeypatch.setattr(jinja2_standalone_compiler, 'INPUT_FOLDER', os.path.join(fixtures_dir, 'header_footer'))
    monkeypatch.setattr(jinja2_standalone_compiler, 'OUTPUT_FOLDER', os.path.join(fixtures_dir, 'header_footer_generated'))
    monkeypatch.setattr(jinja2_standalone_compiler, 'OUTPUT_TEMPLATES', ['child.jinja'])

    if os.path.exists(os.path.join(fixtures_dir, 'header_footer_generated')):
        shutil.rmtree(os.path.join(fixtures_dir, 'header_footer_generated'))

    assert not os.path.exists(os.path.join(fixtures_dir, 'header_footer_generated'))

    jinja2_standalone_compiler.main()

    assert os.path.exists(os.path.join(fixtures_dir, 'header_footer_generated'))
    assert os.path.exists(os.path.join(fixtures_dir, 'header_footer_generated', 'child.html'))
    file_content = open(os.path.join(fixtures_dir, 'header_footer_generated', 'child.html')).read()
    assert file_content == 'header!\nbegin parent\nparent content\n\nchild content\nend parent\nfooter!'
