"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
#http://python.6.x6.nabble.com/distutils-bdist-wininst-failure-on-Linux-td4498729.html
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func) 
    
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='qtrename',
    packages = ['qtrename'],
    version='1.1.1',
    description='feature-rich app to rename files for GNU/Linux and Windows',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/amad3v/QtRename',
    author='Mohamed Jouini',
    author_email='amad3v@gmail.com', 
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],
    python_requires='>=3.7',
    install_requires=['PyQt5>=5.13.2'],
    include_package_data=True,
    # subfolder : relative path
    entry_points={
        'gui_scripts': [
            'qtrename = qtrename.__main__:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/amad3v/QtRename/issues',
        'Releases': 'https://github.com/amad3v/QtRename/releases',
    },
)
