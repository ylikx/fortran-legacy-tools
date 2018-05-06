#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from fixed2free2 import *
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

teststr = [
"""
C This is a Fortran Comment
* this also.
""",

"""
      A = B * C + D +
     +EF**2
""",

"""
      WRITE(*,*) "Just a regular F77 line."
""",

"""
C$OMP PARALLEL DO PRIVATE(X1, X2,
C$OMP&                    X3, X4)
C some code...
C$OMP END PARALLEL DO
C$OMP 
""",
"""
#define NDEBUG
""",
"""
      CALL FOO(A, B, C,
C a comment
* another comment
     +D, E, F)
""",
"""
! Comment1
 ! Comment2
  ! Comment3
   ! Comment4
    ! Comment5
 10   WRITE(*,*) A + B +
     !C + D
     0WRITE(*,*) "Regular line."
""",
"""
c
""",
"""
Csho
""",
"""
C An empty line and an ! continuation character
      X = SIN(A) * COS(B) +

     & SIN(B) * COS(A) +
     ! X
""",
"""
10    CONTINUE
""",
"""
C Test with code that uses text after 72nd column as comments           ENDOFLINE
      E = M * C**2                                                      COMMENT
      CALL FUNC(A, B, C,                                                COMMENT
     +          D, E, F,                                                THEEND
C comment inbetween                                                     WHY
     $          G, H, I)                                                SOMETHING
""",

"""
 1000 E =  ! an inline comment in a continued line
     +    2 * 3
""",

# do not rip apart inline comments
"""
      E = 42                        ! inline comment extending beyond column 72
""",

"""
      E = 42  ! just a short inline comment
""",

"""
      C = "!" //
     &    '!' //                                                        ABC
     &    "!'!" //
     &    "A"
""",
# exclamation mark after column 72
"""
      E = LI                                                            ABC!DEF
""",
# line with exactly 72 cols + newline
"""
      E =                                                             72
""",

# lines with ! at col 72/73
"""
      E = LI                                                           !Comment
      E = 72                                                            !Comment
""",

# inline comment after col 72
"""
      E = LI                                                                !Comment
"""
]

solutions = [
"""
! This is a Fortran Comment
! this also.
""",

"""
A = B * C + D + &
EF**2
""",

"""
WRITE(*,*) "Just a regular F77 line."
""",

"""
!$OMP PARALLEL DO PRIVATE(X1, X2, &
!$OMP                     X3, X4)
! some code...
!$OMP END PARALLEL DO
!$OMP 
""",
"""
#define NDEBUG
""",
"""
CALL FOO(A, B, C, &
! a comment
! another comment
D, E, F)
""",
"""
! Comment1
 ! Comment2
  ! Comment3
   ! Comment4
    ! Comment5
10 WRITE(*,*) A + B + &
C + D
WRITE(*,*) "Regular line."
""",
"""
!
""",
"""
!sho
""",
"""
! An empty line and an ! continuation character
X = SIN(A) * COS(B) + &

 SIN(B) * COS(A) + &
 X
""",
"""
10 CONTINUE
""",
"""
! Test with code that uses text after 72nd column as comments           ENDOFLINE
E = M * C**2                                                            !COMMENT
CALL FUNC(A, B, C, &                                                    !COMMENT
          D, E, F, &                                                    !THEEND
! comment inbetween                                                     WHY
          G, H, I)                                                      !SOMETHING
""",

"""
1000 E = & ! an inline comment in a continued line
    2 * 3
""",

"""
E = 42                        ! inline comment extending beyond column 72
""",

"""
E = 42  ! just a short inline comment
""",

"""
C = "!" // &
    '!' // &                                                            !ABC
    "!'!" // &
    "A"
""",

"""
E = LI                                                                  !ABC!DEF
""",

"""
E =                                                             72
""",

"""
E = LI                                                           !Comment
E = 72                                                                  !Comment
""",

"""
E = LI                                                                      !Comment
"""
]

class Test_CompareStr(unittest.TestCase):

    def streamComp(self, stream1, stream2):
        for s1, s2 in zip(stream1, stream2):
            self.assertEqual(s1, s2)

def dotest(self, instr, solution):
    instream = StringIO(instr)
    outstream = StringIO(solution)
    self.streamComp(outstream, convertToFree(instream))
    instream.close()
    outstream.close()

def makeTest(instr, solution):
    return lambda self: dotest(self, instr, solution)
   
if __name__ == "__main__":
    num = 0
    for instr, solution in zip(teststr, solutions):
        testfun = makeTest(instr, solution)
        testfun.__name__ = "test_" + str(num)
        setattr(Test_CompareStr, testfun.__name__, testfun)
        num += 1
    unittest.main()

