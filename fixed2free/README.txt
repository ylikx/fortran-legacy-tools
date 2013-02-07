fixed2free2.py
author: Elias Rabel

Tool to convert from FORTRAN fixed source form files to free source form.
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

Usage:

python fixed2free2.py file.f > file.f90
