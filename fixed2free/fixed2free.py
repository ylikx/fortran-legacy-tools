# fixed2free.py: Conversion of Fortran code from fixed to free
#                source form.
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
Script that converts fixed form Fortran code to free form
Usage: file name as first command line parameter

python fixed2free.py file.f > file.f90
"""

# author: Elias Rabel, 2012
# Let me know when you find this script useful:
# ylikx.0 at gmail
# https://www.github.com/ylikx/

# TODO:
# *) Does not handle multi-line strings
# *) problems with comments between continued lines - could be easily fixed
# *) Improve command line usage

import sys

line_new_upper = ''
line_new = ''

infile = open(sys.argv[1], 'r')

for line in infile:
  done = False

  if not done and (len(line) == 0):
    done = True

  # check for comment
  if not done:
    if line[0] in "cC*!":
      if len(line.rstrip()) > 1:
        line_new = '!' + line[1:]
      else:
        line_new = '\n' #remove zero character comments
      done = True

  # ignore C preprocessor statements
  if not done:
    if line[0] == '#':
      line_new = line
      done = True


  if not done and len(line) < 7:
    line_new = '\n'
    done = True


  # check for line continuation
  if not done:
    if not line[5].isspace():
      if line_new_upper <> '':
        line_new_upper = line_new_upper.rstrip() + " &\n"

  # extract label
  if not done:
    label = line[0:5]
    if label <> "     ":
      line_new = label.strip() + " " + line[6:]
    else:
      line_new = line[6:]
  
  if line_new_upper <> '':
    print line_new_upper,

  line_new_upper = line_new
  
#end for

# don't forget the last line
print line_new,


infile.close()
