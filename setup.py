from setuptools import setup, find_packages
from os.path import expanduser, join
from os import environ
import fastentrypoints

try:
    HOME=expanduser('~'+environ['SUDO_USER'])
except KeyError:
    HOME=environ['HOME']

with open("README.md", "r") as f:
    long_desc = f.read()

setup(
    name='emojimenu',
    version='0.1.1',
    description='Select and type emoji with dmenu',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url='https://github.com/clarkb7/emojimenu',
    license='MIT',

    author='Branden Clark',
    author_email='clark@rpis.ec',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
    keywords='emoji dmenu',

    packages=['emojimenu'],
    install_requires=['emoji', 'argparse', 'configparser'],
    data_files=[(join(HOME, '.config/emojimenu'), ['emojimenu/emoji.cfg'])],

    entry_points={
        'console_scripts': [
            'emojimenu=emojimenu.emojimenu:main',
        ],
    },
)
