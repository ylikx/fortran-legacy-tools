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

