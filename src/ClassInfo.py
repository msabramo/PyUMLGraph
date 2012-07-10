# $Id: ClassInfo.py,v 1.6 2003/11/17 18:48:11 adamf Exp $  

import types

from PyUMLGraph.BaseClassesGatherer import BaseClassesGatherer
from PyUMLGraph.LocalReferencesGatherer import LocalReferencesGatherer
from PyUMLGraph.SelfReferencesGatherer import SelfReferencesGatherer
from PyUMLGraph.AttributeInfoGatherer import AttributeInfoGatherer
from PyUMLGraph.MethodArgumentsOrderGatherer import MethodArgumentsOrderGatherer
from PyUMLGraph.MethodInfoGatherer import MethodInfoGatherer
from PyUMLGraph.MethodArgumentsInfoGatherer import MethodArgumentsInfoGatherer
from PyUMLGraph.MethodArgumentsDefaultsGatherer import MethodArgumentsDefaultsGatherer
from PyUMLGraph.MethodReturnValueClassNamesGatherer import MethodReturnValueClassNamesGatherer

MIN = 0
ATTRIBUTES = 1
METHODS = 2
TYPES = 4
REFERENCES = 8
MAX = ATTRIBUTES | METHODS | TYPES | REFERENCES

typeNames = [item for item in dir(types) if item[-4:] == 'Type']
commonTypes = [types.__dict__[typeName].__name__ for typeName in typeNames]
commonTypes += ["None"]

class ClassInfo:
   def __init__(self, className, classesToCollectInfoAbout, classesToIgnore):
      self.className = className
      self.classesToCollectInfoAbout = classesToCollectInfoAbout
      self.classesToIgnore = classesToIgnore
      self.baseClasses = BaseClassesGatherer(self.classesToCollectInfoAbout,
                                             self.classesToIgnore)
      self.attributeInfo = AttributeInfoGatherer(self.classesToCollectInfoAbout, 
                                                 self.classesToIgnore)
      self.selfReferences = SelfReferencesGatherer(self.classesToCollectInfoAbout, 
                                                   self.classesToIgnore)
      self.localReferences = LocalReferencesGatherer(self.classesToCollectInfoAbout, 
                                                     self.classesToIgnore)
      self.methodArgumentsOrder = MethodArgumentsOrderGatherer(self.classesToCollectInfoAbout, 
                                                               self.classesToIgnore)
      self.methodArgumentsDefaults = MethodArgumentsDefaultsGatherer(self.classesToCollectInfoAbout, 
                                                                     self.classesToIgnore)
      self.methodArgumentsInfo = MethodArgumentsInfoGatherer(self.classesToCollectInfoAbout, 
                                                             self.classesToIgnore)      
      self.methodInfo = MethodInfoGatherer(self.classesToCollectInfoAbout, 
                                           self.classesToIgnore)
      self.methodReturnValueClassNames = MethodReturnValueClassNamesGatherer(self.classesToCollectInfoAbout, 
                                                                             self.classesToIgnore)

   def collectInfo(self, frame, event, arg):
      self.baseClasses.collectInfo(frame, event, arg)
      self.localReferences.collectInfo(frame, event, arg)
      self.selfReferences.collectInfo(frame, event, arg)
      self.attributeInfo.collectInfo(frame, event, arg)
      self.methodArgumentsOrder.collectInfo(frame, event, arg)
      self.methodArgumentsDefaults.collectInfo(frame, event, arg)
      self.methodArgumentsInfo.collectInfo(frame, event, arg)
      self.methodInfo.collectInfo(frame, event, arg)
      self.methodReturnValueClassNames.collectInfo(frame, event, arg)

   def getInfo(self):
      info = self.__dict__.copy()
      for key in info.keys():
         if key[0] == "_":
            del info[key]
      return info

   def getFormattedInfo(self):
      return self.getInfo().__repr__()

   def getYamlInfo(self):
      info = self.getInfo()
      for key, value in info.items():
         if type(value) == types.InstanceType:
            info[key] = info[key].getInfo()
      return info

   def getDotRepresentation(self, **options):
      detailLevel = options["detailLevel"]
      if self.className in commonTypes:
         if not self.detailLevelMatches(detailLevel, TYPES):
            return ""
      dotRepr = ""
      dotRepr += "    // class %s \n" % self.className 
      dotRepr += "    %s %s\n" % (self.className, self.getDotNodeAttributes(detailLevel, options))
      dotRepr += self.getDotEdgesForNode(detailLevel)
      dotRepr += "\n"
      return dotRepr
   
   def detailLevelMatches(self, detailLevel, detailLevelDesired):
      "private"
      if detailLevel == detailLevelDesired:
         return True
      if detailLevel == 0 or detailLevelDesired == 0:
         return False
      elif detailLevel & detailLevelDesired == detailLevelDesired:
         return True
      else:
         return False

   def getDotNodeAttributes(self, detailLevel, options):
      "private"
      
      #return '[color=black, shape=record, label="%s"];' % self.getDotNodeLabel(detailLevel)
      newOptions = options.copy()
      newOptions["nodeLabel"] = self.getDotNodeLabel(detailLevel)
      return '[fillcolor="%(nodeFillColor)s", shape="%(nodeShape)s", style="%(nodeStyle)s", label="%(nodeLabel)s"];' % newOptions

   def getDotNodeLabel(self, detailLevel):
      "private"
      if self.detailLevelMatches(detailLevel, MIN):
         return self.className
      dotNodeLabel = '{%s\\n' % self.className
      if self.detailLevelMatches(detailLevel, ATTRIBUTES):
         dotNodeLabel += '|%s' % self.getDotNodeClassAttributeInfo()
      if self.detailLevelMatches(detailLevel, METHODS):
         dotNodeLabel += '|%s' % self.getDotNodeClassMethodInfo()
      dotNodeLabel += '}'
      return dotNodeLabel

   def getDotNodeClassAttributeInfo(self):
      dotClassAttributeInfo = ""
      attributeList = self.attributeInfo.getInfo().keys()
      attributeList.sort()
      for attribute in attributeList:
         attributeClassNames = self.attributeInfo.getInfo()[attribute]
         attributeClassNames.sort()
         dotClassAttributeInfo += "%s: " % attribute
         for className in attributeClassNames:
            dotClassAttributeInfo += "%s," % className
         if dotClassAttributeInfo[-1] == ",":
            dotClassAttributeInfo = dotClassAttributeInfo[:-1]
         dotClassAttributeInfo += "\l"
      return dotClassAttributeInfo

   def getDotNodeClassMethodInfo(self):
      dotClassMethodInfo = ""
      methodNameList = self.methodReturnValueClassNames.getInfo().keys()
      for methodName in methodNameList:
         methodReturnValueClassNames = self.methodReturnValueClassNames.getInfo()[methodName]
         methodReturnValueClassNames.sort()
         dotClassMethodInfo += "%s: " % methodName
         for className in methodReturnValueClassNames:
            dotClassMethodInfo += "%s," % className
         if dotClassMethodInfo[-1] == ",":
            dotClassMethodInfo = dotClassMethodInfo[:-1]
         dotClassMethodInfo += "\l"
      return dotClassMethodInfo

   def canDisplayClass(self, classToDisplay, detailLevel):
      "private"
      if classToDisplay in commonTypes:
         if not self.detailLevelMatches(detailLevel, TYPES):
            return False
      return True


   def getBaseClassEdges(self, detailLevel):
      "private"
      dotEdges = ""
      for baseClass in self.baseClasses.baseClasses:
         if self.canDisplayClass(baseClass, detailLevel):
            dotEdges += "      %s -- %s [arrowhead=empty];\n" % (self.className, baseClass)
      return dotEdges

   def getTemporarilyReferencedEdges(self, detailLevel):
      "private"
      dotEdges = ""
      for temporarilyReferencedClass in self.localReferences.localReferences:
         if self.canDisplayClass(temporarilyReferencedClass, detailLevel):
            dotEdges += "      %s -- %s [arrowtail=odiamond];\n" % \
                        (self.className, temporarilyReferencedClass)
      return dotEdges

   def getSelfReferencedEdges(self, detailLevel):
      "private"
      dotEdges = ""
      for selfReferencedClass in self.selfReferences.selfReferences:
         if self.canDisplayClass(selfReferencedClass, detailLevel):
            dotEdges += "       %s -- %s [arrowtail=diamond];\n" % \
                        (self.className, selfReferencedClass)
      return dotEdges


   def getAllReferencedEdges(self, detailLevel):
      "private"
      dotEdges = ""
      referencedClasses = self.localReferences.localReferences + \
                          self.selfReferences.selfReferences
      referencedClasses = self.uniqueList(referencedClasses)
      referencedClasses.sort()
      for referencedClass in referencedClasses:
         if self.canDisplayClass(referencedClass, detailLevel):
            dotEdges += "      %s -- %s [arrowtail=odiamond];\n" % \
                        (self.className, referencedClass)
      return dotEdges


   def getReferenceEdges(self, detailLevel):
      "private"
      dotEdges = ""
      if self.detailLevelMatches(detailLevel, REFERENCES):
         dotEdges = self.getTemporarilyReferencedEdges(detailLevel) + \
                    self.getSelfReferencedEdges(detailLevel)
      else:
         dotEdges = self.getAllReferencedEdges(detailLevel)
      return dotEdges

   def getDotEdgesForNode(self, detailLevel):
      "private"
      dotEdges = ""
      dotEdges += self.getBaseClassEdges(detailLevel)
      dotEdges += self.getReferenceEdges(detailLevel)
      return dotEdges

   def uniqueList(self, list):
      "private"
      u = {}
      for item in list:
         u[item] = 1
      return u.keys()

