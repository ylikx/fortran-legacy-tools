# fortran-legacy-tools

**Tools to deal with Fortran code**

**Author:** Elias Rabel

This project includes a suite of tools aimed at facilitating the modernization of Fortran codebases, making them more compatible with contemporary coding standards and practices.

## fixed2free2.py

### Description

`fixed2free2.py` converts Fortran code from fixed source form to free source form. This tool is particularly useful in refactoring legacy Fortran codes, enhancing their readability and maintainability.

### Background

The fixed source format is a legacy from the era of punched cards but remains in use within the numerical computing community. Despite Fortran 2018 allowing for fixed source form, it has been deprecated since Fortran 2003 in favor of the free source form introduced in Fortran 90.

### Functionality

The tool takes a minimalistic approach by changing only the source form without attempting to modify or upgrade deprecated language constructs. It supports OpenMP and C-preprocessor statements, ensuring a smooth transition to free source form.

### Usage

```bash
python fixed2free2.py file.f > file.f90
```

### Limitations

While fixed2free2.py aims to accurately transform fixed form code to free form, it has specific limitations regarding whitespace usage that can affect the conversion:

The script cannot handle certain usages of whitespace characters allowed in fixed form but not in free form. This limitation is crucial when dealing with complex formatting that does not directly translate into free form.

For example, the following fixed form source code:

```Fortran
      WR    IT E(* ,   *) I J K       LM N
```

will not be transformed into correct free form source code, which would be:

```Fortran
WRITE (*,*) IJKLMN
```

[issue2]: https://github.com/ylikx/fortran-legacy-tools/issues/2

## Additional Tools in the Project

### flowercase.py:

A tool to convert free source form Fortran code to lowercase, excluding comments and strings, while leaving mixed case identifiers unchanged.

### fdeclarations.py:

Assists in separating subroutine arguments from local variable declarations, enhancing code clarity and organization.

Legacy Fortran subroutines often have huge argument lists. Fortran allows mixing of argument datatype declarations and declarations of local variables, which can lead to confusion.

This tool generates code for a wrapper of the given subroutine, which groups declarations into 3 sections:

- parameters (might be needed for dimensions of array arguments)
- subroutine arguments
- local variables (commented out)
