# -*- coding: utf-8 -*-

# fdeclarations.py: Tool to separate subroutine arguments from
#                   declarations of local variables
#
# Copyright (C) 2012    Elias Rabel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Tool to separate subroutine arguments from declarations of local variables.

Legacy Fortran subroutines often have huge argument lists. Fortran allows
mixing of argument datatype declarations and declarations of local variables, 
which can lead to confusion.

This tool generates code for a wrapper of the given subroutine, which
separates declarations into 3 sections:
-) parameters (might be needed for dimensions of array arguments)
-) subroutine arguments
-) local variables (commented out)

Furthermore a conversion to the Fortran 90 declaration style is performed.

Usage: python fdeclarations.py file.f90 > output.f90

Restrictions:

*) Assumes free source format
*) Assumes 'implicit none'
*) Only one subroutine per file allowed

*) There might be problems when working with Fortran functions
Workaround: replace 'function' keyword temporarily with 'subroutine'

*) Warning: does not deal with attributes in different lines:
*) e.g.:
*) double complex :: CONE
*) parameter (CONE = (1.0d0, 0.0d0))

*) does not deal with constructs like real * 8 or real (8) 
*) in F77 declaration style if not written without spaces


author: Elias Rabel
Let me know when you find this script useful:
ylikx.0 at gmail
https://www.github.com/ylikx/

"""

import re
import sys

TYPEKEYS = ['integer', 'logical', 'real', 'complex',
            'double precision', 'double complex']

#m = re.search(r'(subroutine|function)(.*?)\((.*?)\)', s)


#class FortranVariableDict

class FortranVariable:
    def __init__(self, name, decl, dim, initialiser, is_argument=False):
        self.name = name
        self.decl = decl
        self.dim = dim
        self.initialiser = initialiser
        self.is_argument = is_argument

        if 'parameter' in self.decl:
            self.is_parameter = True
        else:
            self.is_parameter = False


    def __repr__(self):
        return str([self.name, self.decl, self.dim, self.initialiser, self.is_argument])

    def getDeclString(self):
        """Returns a F90-declaration string."""
        string = self.decl 
        if self.dim:
           string += ", dimension" + self.dim
        string += " :: " + self.name
        if self.initialiser:
           string += " = " + self.initialiser
        return string

# TODO
class FortranSubroutineHeader:
    def __init__(name, arglist):
        self.name = ''
        self.arglist = []

#------------------------------------------------------------------------------
def gen_removeComments(stream):
    """Remove Fortran comments from stream considering strings"""


    for line in stream:
        string_delim = None
        result_line = ''

        for ch in line:
            if ch in ["'", '"']:
                if not string_delim:
                    string_delim = ch
                elif string_delim == ch:
                    string_delim = None

            if ch == '!' and not string_delim:
                result_line += '\n'
                break

            result_line += ch

        if result_line.isspace():
            continue

        yield result_line
                

#------------------------------------------------------------------------------
def gen_removeLineContinuations(stream):
    result_line = ''

    for line in stream:
        if re.search(r'&\s*$', line):
            result_line = result_line.rstrip() + line.rstrip().rstrip('&').lstrip()
            continue
        else:
            result_line += line

        yield result_line
        result_line = ''

#------------------------------------------------------------------------------
def gen_removeEmptyLines(stream):
    """Creates Generator that returns only non-empty lines of a stream"""
    for line in stream:
        #skip empty lines
        if line.isspace():
            continue
        yield line


#TODO integer function etc... problematic
# Misinterpretes function declaration
#------------------------------------------------------------------------------
def isDeclarationLine(line):

    for ty in TYPEKEYS:
        # search for whole words only
        if re.search(r'\b'+ty+r'\b', line, re.IGNORECASE):
            return True

    return False

#------------------------------------------------------------------------------
def separate_names_and_dims(varstr):
    """Removes dimension list. E.g.: "var (n,m), x(5)" -> ("var, x", "(n,m) (5)") """
    names = []
    dims = []

    namestr = ''
    dimstr = ''

    num_par = 0

    for ch in varstr:

        if not ch in '()':
            if num_par == 0:
                namestr += ch
            else:
                dimstr += ch
        elif ch == '(':
            num_par += 1
            dimstr += ch
        elif ch == ')':
            num_par -= 1
            dimstr += ch

        if ch == ',' and num_par == 0:
            namestr = namestr.replace(',', '')
            # new variable
            names.append(namestr.strip())
            dims.append(dimstr.strip())
            namestr = ''
            dimstr = ''

    names.append(namestr.strip())
    dims.append(dimstr.strip())

    return names, dims

#------------------------------------------------------------------------------
def removeDimension(x):
    """Removes dimension list. E.g.: "var (n,m), x(5)" -> "var, x" """
    result = ''
    num_par = 0
    for ch in x:
        if not ch in '()':
            if num_par == 0:
                result += ch
        elif ch == '(':
            num_par += 1
        elif ch == ')':
            num_par -= 1
    return result

#------------------------------------------------------------------------------
def getVarsF90Style(line):
    ind = line.find('::')
    varstr = line[ind+2:].strip()
    decl = line[:ind].strip()
    return decl, varstr

#------------------------------------------------------------------------------
def getVarsF77Style(line):
    #([*][0-9]+)? is to support stuff like real*8
    #varstr = re.sub('('+'|'.join(TYPEKEYS) + r')([*][0-9]+)?.*?', '', line, re.IGNORECASE).strip()
    # deal also with stuff like real(8)
    #print re.match('('+'|'.join(TYPEKEYS) + r')(([*][0-9]+)|\(.+?\))?.*?', line, re.IGNORECASE).group(0)
    #varstr = re.sub('('+'|'.join(TYPEKEYS) + r')(([*][0-9]+)|\(.+?\))?', '', line, re.IGNORECASE).strip()
    #print varstr
    #ind = line.find(varstr)
    #decl = line[:ind].strip()
    sline = line.split()
    decl = sline.pop(0).strip()
    if decl.lower() == 'double':
        decl += ' ' + sline.pop(0).strip()
    varstr = ' '.join(sline)    

    return decl, varstr

#------------------------------------------------------------------------------
def extractInitialiser(expr):
    split_expr = expr.split('=')
    if len(split_expr) > 1:
        return split_expr[0].strip(), split_expr[1].strip()
    else:
        return split_expr[0].strip(), None
   
#------------------------------------------------------------------------------
def getVariablenames(line):
    """Given a declaration line, returns a list of names of
       variables declared in this line and the declaration part"""

    if '::' in line:
        decl, varstr = getVarsF90Style(line)
    else:
        decl, varstr = getVarsF77Style(line)

    # if initialisation of varible in same line - extract it
    varstr, initialiser = extractInitialiser(varstr)

    #names = [name.strip() for name in removeDimension(varstr).split(',')]

    names, dims = separate_names_and_dims(varstr)
    return decl, names, dims, initialiser


#-----------------------------------------------------------------------------
def getArgumentList(argline):
    """Returns the argument list of a Fortran subroutine"""
    #print line
    re_match = re.search(r'subroutine(.*?)\((.*)\)', argline, re.IGNORECASE)
    
    if re_match == None:
        return None

    #print re_match.group(0)
    
    name = re_match.group(1).strip()
    arglist = [arg.strip() for arg in re_match.group(2).split(',')]

    return name, arglist

#TODO: store declaration line, extract type info, save dimension info

#------------------------------------------------------------------------------
def printWrapperCode(subname, arglist, varlist):
    print("!" + "-"*79)
    print("!> A wrapper for the subroutine " + subname)
    #for entry in arglist:
    #    print "!> @param        " + entry
    print("subroutine " + subname + "_wrapper(" + ','.join(arglist) + ')')
    print
    print("  implicit none")
    print
    # parameters first
    print( "  ! Parameters")
    for entry in varlist:
        if not entry.is_argument and entry.is_parameter:
            print ("  " + entry.getDeclString())
    # print scalar arguments
    print
    print( "  ! Arguments")
    for entry in varlist:
        if entry.is_argument:
            print ("  " + entry.getDeclString())
    # print array arguments
    #print
    #print "  ! Array arguments"
    #for entry in varlist:
    #    if entry.is_argument and entry.dim:
    #        print "  " + entry.getDeclString()
    print
    print "  ! Former local variables of " + subname
    for entry in varlist:
        if not entry.is_argument:
            print "  ! " + entry.getDeclString()
    
    print
    print ("  call " + subname + "(" + ','.join(arglist) + ')')
    print
    print("end subroutine")

if __name__ == "__main__":

    f = open(sys.argv[1], 'r')

    xf = gen_removeEmptyLines(gen_removeLineContinuations(gen_removeComments(f)))

    class NoArgList:
        pass

    # get argument list first:
    args = None

    for line in xf:
        temp = getArgumentList(line)
        if temp != None:
            subname, args = temp
            break

    if not args:
        print "ERROR: no subroutine header found!"
        raise NoArgList

    vardict = {}
    varlist = []

    for line in xf:
        if isDeclarationLine(line):
            decl, names, dims, initstr = getVariablenames(line)
            #print getVariablenames(line)
            for name, dim in zip(names, dims):
                entry = FortranVariable(name, decl, dim, initstr, is_argument=False)
                vardict[name.lower()] = entry
                varlist.append(entry)

        if "end subroutine" in line:
            break

    #print varlist

    # Flag arguments
    for arg in args:
        vardict[arg.lower()].is_argument = True


    f.close()

    printWrapperCode(subname, args, varlist)

