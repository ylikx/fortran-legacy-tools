# fixed2free2.py
Author: Elias Rabel

Tool to convert from FORTRAN fixed source form files to free source form.
Supports OpenMP and C-preprocessor statements.

The FORTRAN fixed source format dates back to time when punched cards were
used in programming. Nevertheless it is widespread in the numerical computing
community. Even programs written according to the most recent Fortran 2018
standard can be written in fixed source form, although this is deprecated since
Fortran 2003.

This script converts fixed source form files to the free source form,
introduced with Fortran 90.
In refactoring legacy Fortran codes this is a useful first step.

Some similar tools that I tried, attempt to automatically upgrade 
deprecated language constructs with varying success.
This tool takes a more minimalistic approach and changes only the source form.

Usage:

```bash
python fixed2free2.py file.f > file.f90
```

## Limitations

This script can not handle certain usage of whitespace characters that is allowed in fixed
form but not in free form source code (see [#2][issue2]).

For example:

The following fixed form source code

```Fortran
      WR    IT E(* ,   *) I J K       LM N
```

will not be transformed into correct free form source code, which would be:
 
```Fortran
WRITE (*,*) IJKLMN
```

[issue2]: https://github.com/ylikx/fortran-legacy-tools/issues/2
