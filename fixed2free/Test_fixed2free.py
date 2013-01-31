#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from fixed2free2 import *
from StringIO import StringIO


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
"""
]

class Test_fixed2free(unittest.TestCase):

    def streamComp(self, stream1, stream2):
        for s1, s2 in zip(stream1, stream2):
            self.assertEqual(s1, s2)

    def dotest(self,test, sol):
        instream = StringIO(test)
        outstream = StringIO(sol)
        self.streamComp(outstream, convertToFree(instream))
        instream.close
        outstream.close

    def test_00(self):
        self.dotest(teststr[0], solutions[0])
    def test_01(self):
        self.dotest(teststr[1], solutions[1])
    def test_02(self):
        self.dotest(teststr[2], solutions[2])
    def test_03(self):
        self.dotest(teststr[3], solutions[3])
    def test_04(self):
        self.dotest(teststr[4], solutions[4])
    def test_05(self):
        self.dotest(teststr[5], solutions[5])
    def test_06(self):
        self.dotest(teststr[6], solutions[6])   
    def test_07(self):
        self.dotest(teststr[7], solutions[7])
    def test_08(self):
        self.dotest(teststr[8], solutions[8])      
if __name__ == "__main__":
    unittest.main()
