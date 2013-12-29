from setuptools import setup

setup(
    name='jinja2_standalone_compiler',
    version='0.1',
    long_description=open('README.md').read(),
    install_requires=open('requirements.txt').readlines(),
)
