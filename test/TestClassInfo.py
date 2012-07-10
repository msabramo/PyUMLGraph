# $Id: ClassInfoTest.py,v 1.3 2003/10/16 17:25:26 adamf Exp $

import unittest

from PyUMLGraph.ClassInfo import ClassInfo, MIN, MAX, ATTRIBUTES, METHODS, TYPES

class ClassInfoTest(unittest.TestCase):
   def setUp(self):
      self.classInfo = ClassInfo("None", None, None)

   def tearDown(self):
      pass
   
   def testDetailLevelMatchesAll(self):
      for detailLevel in (MAX, ATTRIBUTES, METHODS, TYPES):
         self.assertEqual(True,
                          self.classInfo.detailLevelMatches(detailLevel,detailLevel),
                          "Detail levels should match for detailLevel %s." % detailLevel)

      for detailLevel in (MAX, ATTRIBUTES, METHODS, TYPES):
         self.assertEqual(False,
                          self.classInfo.detailLevelMatches(128, detailLevel),
                          "Detail levels should not match for detailLevel %s." % detailLevel)

      self.assertEqual(True,
                       self.classInfo.detailLevelMatches(MIN, MIN),
                       "Detail levels should match for detailLevel MIN (0).")


      self.assertEqual(False,
                       self.classInfo.detailLevelMatches(MAX, MIN),
                       "Detail levels should not match for detailLevel MIN (0).")


if __name__ == "__main__":
   unittest.main()
