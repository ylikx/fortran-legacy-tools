fortran-legacy-tools

Tools to deal with Fortran code

-------------------------------------------------------------------------------
fixed2free/fixed2free2.py:
-------------------------------------------------------------------------------

Tool to convert from FORTRAN fixed source form files to free source form.
Supports OpenMP and C-preprocessor statements.

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

