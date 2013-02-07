#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

mymail = '12345.0$gmail.com'.replace('1','y').replace('2','l')
mymail = mymail.replace('3','i').replace('4','k').replace('5','x').replace('$', '@')

setup(name='fixed2free2',
      version='0.8',
      description='Fortran fixed to free source form converter',
      long_description="""Tool to convert from FORTRAN fixed source form files to free source form.
Supports OpenMP and C-preprocessor statements.

The FORTRAN fixed source format dates back to time when punched cards were
used in programming. Nevertheless it is widespread in the numerical computing
community. Even programs written according to the most recent Fortran 2008
standard can be written in fixed source form, although this is deprecated since
Fortran 2003.

This script converts fixed source form files to the free source form,
introduced with Fortran 90.
In refactoring legacy Fortran codes this is a useful first step.

Some similar tools that I tried, attempt to automatically upgrade 
deprecated language constructs with varying success.
This tool takes a more minimalistic approach and changes only the source form.
""",
      author='Elias Rabel',
      author_email=mymail,
      url='https://github.com/ylikx/fortran-legacy-tools',
      scripts=['fixed2free2.py'],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Fortran',
                   'Topic :: Software Development',
                   'Topic :: Software Development :: Code Generators',
                   'Topic :: Scientific/Engineering',]
     )

#TODO: download_url
