# flowercase.py: Conversion of Fortran code from traditional all
#                uppercase source to more readable lowercase.
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
Script that converts free form Fortran code to lower case
without messing with comments or strings. Mixed case words remain
untouched. 

Note: works only in free source form, use fixed2free.py first to
convert.

Usage: file name as first command line parameter
"""

# author: Elias Rabel, 2012
# Let me know when you find this script useful:
# ylikx.0 at gmail
# https://www.github.com/ylikx/

from __future__ import print_function

import sys

infile = open(sys.argv[1], 'r')

commentmode = False
stringmode = False
stringchar = ''


for line in infile:
  line_new = ''
  word = ''
  commentmode = False
  stringmode = False

  for character in line:
    if not character.isalnum() and character != '_':

      if not stringmode and not commentmode:
        if word.isupper(): # means: do not convert mixed case words
          word = word.lower()

      line_new += word
      line_new += character
      word = ''

      if character == '"' or character == "'" and not commentmode:
        if not stringmode:
          stringchar = character
          stringmode = True
        else:
          stringmode = not (character == stringchar)

      if character == '!' and not stringmode:
        commentmode = True # treat rest of line as comment

    else:
      word += character

  print(line_new, end="")

infile.close()
