# $Id: InfoCollectorTest.py,v 1.4 2003/10/16 17:25:26 adamf Exp $

import unittest, sys
import yaml

from PyUMLGraph.InfoCollector import InfoCollector
from TestClasses import TestClassOne, TestClassTwo, TestClassThree, TestClassFour

class InfoCollectorTest(unittest.TestCase):
   def setUp(self):
      self.classesToCollectInfoAbout = None
#      self.classesToCollectInfoAbout = ["TestClassOne",
#                                        "TestClassTwo",
#                                        "TestClassThree",
#                                        "TestClassFour"]
      self.infoCollector = InfoCollector(self.classesToCollectInfoAbout)
      self.infoCollector.collectInfoYes()
      self.excerciseTestClasses()
      self.infoCollector.collectInfoNo()
      self.classesInfo = self.infoCollector.getInfo()
#      print self.infoCollector.getFormattedInfo()

   def tearDown(self):
      pass

   def excerciseTestClasses(self):
      testClassOne = TestClassOne()
      testClassOne.methodOne("foo")
      testClassOne.methodTwo(1111, "bar")
      testClassTwo = TestClassTwo()
      testClassTwo.methodOne()
      testClassTwo.methodTwo()
      testClassThree = TestClassThree()
      testClassThree.privateMethod()
      testClassThree.publicMethod()
      testClassFour = TestClassFour()
      testClassFour.methodOne("a", 1, 3.14592)

   def testCollectInfoYesNo(self):
      self.infoCollector = InfoCollector(self.classesToCollectInfoAbout)
      self.timesGlobalTraceWasCalled = 0
      self.infoCollector.globalTrace = self.mockGlobalTrace
      self.infoCollector.collectInfoYes()
      testClassOne = TestClassOne()
      testClassOne.methodOne()
      self.infoCollector.collectInfoNo()
      testClassOne.methodOne()
      self.assertEqual(3, self.timesGlobalTraceWasCalled)

   def mockGlobalTrace(self, frame, event, arg):
      self.timesGlobalTraceWasCalled += 1
      return self.infoCollector.localTrace
      
   def testCollectMethodNameInfo(self):
      testClassOneInfo = self.classesInfo["TestClassOne"]
      expectedMethodNames = ["__init__", "methodOne", "methodTwo"]
      actualMethodNames = testClassOneInfo.methodInfo.getInfo().keys()
      sequencesMatch = self.verifySequencesMatch(expectedMethodNames, actualMethodNames)
      self.assertEqual(True, sequencesMatch, "Method names not correct. (expected: %s actual: %s" % (expectedMethodNames, actualMethodNames))

      testClassThreeInfo = self.classesInfo["TestClassThree"]
      expectedMethodInfo = {"__init__" : "public",
                            "publicMethod": "public",
                            "privateMethod": "private"}
      actualMethodInfo = testClassThreeInfo.methodInfo.getInfo()
      self.assertEqual(expectedMethodInfo, actualMethodInfo)

   def testCollectMethodReturnValueClassNamesInfo(self):
      testClassOneInfo = self.classesInfo["TestClassOne"]
      methodOneReturnValueClassNames = testClassOneInfo.methodReturnValueClassNames.getInfo()['methodOne']
      expectedReturnValueClassNames = ["str"]
      sequencesMatch = self.verifySequencesMatch(expectedReturnValueClassNames, \
                                                 methodOneReturnValueClassNames)
      self.assertEqual(True, sequencesMatch, \
                       "Local references not correct. (expected: %s actual: %s" % \
                       (expectedReturnValueClassNames, methodOneReturnValueClassNames))

   def testCollectLocalReferencesInfo(self):
      testClassFourInfo = self.classesInfo["TestClassFour"]
      expectedLocalReferences = ["TestClassThree"]
      sequencesMatch = self.verifySequencesMatch(expectedLocalReferences, testClassFourInfo.localReferences.getInfo())
      self.assertEqual(True, sequencesMatch, "Local references not correct. (expected: %s actual: %s" % (expectedLocalReferences, testClassFourInfo.localReferences.getInfo()))


   def testCollectSelfReferencesInfo(self):
      testClassFourInfo = self.classesInfo["TestClassFour"]
      expectedSelfReferences = ["TestClassTwo"]
      sequencesMatch = self.verifySequencesMatch(expectedSelfReferences, testClassFourInfo.selfReferences.getInfo())
      self.assertEqual(True, sequencesMatch, "Self references not correct. (expected: %s actual: %s" % (expectedSelfReferences, testClassFourInfo.selfReferences.getInfo()))

      
   def testCollectMethodArgumentsInfo(self):
      testClassOneInfo = self.classesInfo["TestClassOne"]
      expectedMethodArgumentsInfo = { "methodOne" : {"methodOneArgOne" : ["int"]},
                                      "methodTwo" : {"methodTwoArgOne" : ["str"],
                                                     "methodTwoArgTwo" : ["str"]}}
      actualMethodArgumentsInfo = testClassOneInfo.methodArgumentsInfo.getInfo()
      sequencesMatch = self.verifySequencesMatch(expectedMethodArgumentsInfo, actualMethodArgumentsInfo)
      self.assertEqual(True, sequencesMatch, "Arguments info not correct. (expected: %s actual: %s" % (expectedMethodArgumentsInfo, actualMethodArgumentsInfo))


   def testCollectBaseNamesInfo(self):
      testClassTwoInfo = self.classesInfo["TestClassTwo"]
      expectedBases = ["TestClassOne"]
      actualBases = testClassTwoInfo.baseClasses.getInfo()
      sequencesMatch = self.verifySequencesMatch(expectedBases, actualBases)
      self.assertEqual(True, sequencesMatch, "Base class info not correct. (expected: %s actual: %s" % (expectedBases, actualBases))
      
      testClassOneInfo = self.classesInfo["TestClassOne"]
      expectedBases = []
      actualBases = testClassOneInfo.baseClasses.getInfo()      
      sequencesMatch = self.verifySequencesMatch(expectedBases, actualBases)
      self.assertEqual(True, sequencesMatch, "Base class info not correct. (expected: %s actual: %s" % (expectedBases, actualBases))

   def testCollectMethodArgumentOrderInfo(self):
      testClassFourInfo = self.classesInfo["TestClassFour"]
      expectedMethodArgumentsOrder = ["methodOneArgOne", "methodOneArgTwo", "methodOneArgThree"]
      actualMethodArgumentsOrder = testClassFourInfo.methodArgumentsOrder.getInfo()["methodOne"]
      sequencesMatch = self.verifySequencesMatch(expectedMethodArgumentsOrder, actualMethodArgumentsOrder)
      self.assertEqual(True, sequencesMatch, "Method argument order not correct. (expected: %s actual: %s" % (expectedMethodArgumentsOrder, actualMethodArgumentsOrder))
      

   def testCollectMethodArgumentDefaults(self):
      testClassOneInfo = self.classesInfo["TestClassOne"]
      expectedDefaults = [repr(None), repr(1.614)]
      actualDefaults = testClassOneInfo.methodArgumentsDefaults.getInfo()["methodTwo"]
      sequencesMatch = self.verifySequencesMatch(expectedDefaults, actualDefaults)
      self.assertEqual(True, sequencesMatch, "Default arguments info not correct for TestClassOne.methodTwo. (expected: %s actual: %s" % (expectedDefaults, actualDefaults))

      expectedDefaults = [repr("defaultA")]
      actualDefaults = testClassOneInfo.methodArgumentsDefaults.getInfo()["methodOne"]
      sequencesMatch = self.verifySequencesMatch(expectedDefaults, actualDefaults)
      self.assertEqual(True, sequencesMatch, "Default arguments info not correct for TestClassOne.methodOne. (expected: %s actual: %s" % (expectedDefaults, actualDefaults))


   def testCollectAttributeInfo(self):
      testClassOneInfo = self.classesInfo["TestClassOne"]
      expectedAttributeInfo = {
         "one"       : ["str"],
         "two"       : ["str", "list"],
         "three"     : ["int", "str"],
         "pi"        : ["float"],
         "list"      : ["list"],
         "dict"      : ["dict"],
         "vegetable" : ["string"]
         }
      actualAttributeInfo = testClassOneInfo.attributeInfo.getInfo()
      sequencesMatch = self.verifySequencesMatch(expectedAttributeInfo, actualAttributeInfo)
      self.assertEqual(True, sequencesMatch, "Default arguments info not correct for TestClassOne.methodOne. (expected: %s actual: %s" % (expectedAttributeInfo, actualAttributeInfo))


   def testYamlDump(self):
      self.writeTextFile("testClasses.yaml", yaml.dump(self.infoCollector.getYamlInfo()))

   def testGetDotFormattedInfo(self):
      self.writeTextFile("testClasses.dot", self.infoCollector.getDotFormattedInfo())
      
   def verifySequencesMatch(self, sequenceOne, sequenceTwo):
      for item in sequenceOne:
         if item not in sequenceTwo:
            return False
      return True      

   def writeTextFile(self, filePathname, string):
      file = open(filePathname, "w")
      file.write(string)
      file.close()

if __name__ == "__main__":
   unittest.main()
