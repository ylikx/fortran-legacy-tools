fortran-legacy-tools

Tools to deal with Fortran code

-------------------------------------------------------------------------------
fixed2free/fixed2free2.py:
-------------------------------------------------------------------------------

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

-------------------------------------------------------------------------------
flowercase/flowercase.py:
-------------------------------------------------------------------------------

Tool to convert free source form Fortran code to lower-case while
leaving comments and strings unchanged.
Mixed case identifiers and keywords are left unchanged.

-------------------------------------------------------------------------------
fdeclarations/fdeclarations.py:
-------------------------------------------------------------------------------

Tool to separate subroutine arguments from declarations of local variables.

Legacy Fortran subroutines often have huge argument lists. Fortran allows
mixing of argument datatype declarations and declarations of local variables,
which can lead to confusion.

This tool generates code for a wrapper of the given subroutine, which
groups declarations into 3 sections:
-) parameters (might be needed for dimensions of array arguments)
-) subroutine arguments
-) local variables (commented out)

