from setuptools import setup

VERSION = '1.3.0'


setup(
    name='jinja2_standalone_compiler',
    packages=['jinja2_standalone_compiler', ],
    version=VERSION,
    author='Filipe Waitman',
    author_email='filwaitman@gmail.com',
    install_requires=[x.strip() for x in open('requirements.txt').readlines()],
    url='https://github.com/filwaitman/jinja2-standalone-compiler',
    download_url='https://github.com/filwaitman/jinja2-standalone-compiler/tarball/{}'.format(VERSION),
    test_suite='tests',
    keywords=['Jinja2', 'Jinja', 'renderer', 'compiler', 'HTML'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
    entry_points="""\
    [console_scripts]
    jinja2_standalone_compiler = jinja2_standalone_compiler:main_command
    """,
)
