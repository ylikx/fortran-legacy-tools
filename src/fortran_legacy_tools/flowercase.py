# flowercase.py: Conversion of Fortran code from traditional all
#                uppercase source to more readable lowercase.
#
# Copyright (C) 2012-2021    Elias Rabel
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
Converts free form Fortran code to lower case without altering comments, strings,
or mixed case words.

Usage:
  flowercase <file.f90>

Options:
  -h --help     Show this screen.
  <file.f90>   Input file name with free form Fortran code.

Notes:
  - This script is designed to work only with free source form. Use fixed2free.py first if you need to convert from fixed to free source form.
  - The script lowers the case of all Fortran keywords and variables that are entirely in uppercase, while preserving the case of mixed case identifiers, strings, and comments.

Example:
  flowercase my_program.f90 > updated_program.f90
"""

# author: Elias Rabel, 2012
# Let me know when you find this script useful:
# ylikx.0 at gmail
# https://www.github.com/ylikx/

from __future__ import print_function

import sys

from docopt import docopt


def main():
    args = docopt(__doc__)
    infile = open(sys.argv[1], "r")

    commentmode = False
    stringmode = False
    stringchar = ""

    with open(args["<file.f90>"], "r") as infile:
        for line in infile:
            line_new = ""
            word = ""
            commentmode = False

            for character in line:
                if not character.isalnum() and character != "_":
                    if not stringmode and not commentmode:
                        if word.isupper():  # means: do not convert mixed case words
                            word = word.lower()

                    line_new += word
                    line_new += character
                    word = ""

                    if (character == '"' or character == "'") and not commentmode:
                        if not stringmode:
                            stringchar = character
                            stringmode = True
                        else:
                            stringmode = not (character == stringchar)

                    if character == "!" and not stringmode:
                        commentmode = True  # treat rest of line as comment

                else:
                    word += character

            print(line_new, end="")


if __name__ == "__main__":
    main()
