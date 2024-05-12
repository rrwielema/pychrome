from setuptools import setup, find_packages

import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
    name='pychrome',
    version='0.0.1',
    description='Python package to automate Chrome browser using Selenium ChromeDriver',
    long_description=(here / 'README.md').read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    author='R.R. Wielema',
    author_email='rwielema@gmail.com',
    url='rrwielema',
    packages=find_packages(),
    install_requires=['httpagentparser', 'beautifulsoup4', 'pandas', 'selenium', 'requests', 'lxml', 'numpy']
)

