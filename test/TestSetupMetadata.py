# $Id: SetupMetadataTest.py,v 1.2 2003/10/20 18:02:13 adamf Exp $

import sys,unittest

from PyUMLGraph.SetupMetadata import SetupMetadata

class SetupMetdataTest(unittest.TestCase):
   def setUp(self):
      pass

   def tearDown(self):
      pass
   
   def testPlatformIsWindowsOrDos(self):
      origPlatform = sys.platform
      
      sys.platform = "win32"
      self.assertEqual(True, SetupMetadata().platformIsWindowsOrDos(), \
                       "Platform should be Windows or DOS now. (win32)")
   
      sys.platform = "dos"
      self.assertEqual(True, SetupMetadata().platformIsWindowsOrDos(), \
                       "Platform should be Windows or DOS now. (dos)")

      sys.platform = "linux2"
      self.assertEqual(False, SetupMetadata().platformIsWindowsOrDos(), \
                       "Platform should not be Windows or DOS now.")

      sys.platform = "ms-dos"
      self.assertEqual(True, SetupMetadata().platformIsWindowsOrDos(), \
                       "Platform should be Windows or DOS now. (ms-dos)")

      sys.platform = origPlatform


   def testGetSetupMetadata(self):
      origPlatform = sys.platform
      
      sys.platform = "win32"
      metadata = SetupMetadata().getMetadata()
      self.assertEqual(['src/pyumlgraph.py'], metadata['scripts'])

      sys.platform = "linux2"
      metadata = SetupMetadata().getMetadata()
      self.assertEqual(['src/pyumlgraph'], metadata['scripts'])

      sys.platform = origPlatform


if __name__ == "__main__":
   unittest.main()
