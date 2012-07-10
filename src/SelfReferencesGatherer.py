# $Id: SelfReferencesGatherer.py,v 1.3 2003/10/16 17:25:26 adamf Exp $  

import types

from PyUMLGraph.Gatherer import Gatherer

class SelfReferencesGatherer(Gatherer):
   def __init__(self, classesToCollectInfoAbout, classesToIgnore):
      Gatherer.__init__(self, classesToCollectInfoAbout, classesToIgnore)
      self.selfReferences = []

   def __repr__(self):
      return repr(self.selfReferences)

   def collectInfo(self, frame, event, arg):
      if "self" in frame.f_locals.keys():
         attributes = self.getInstanceAttributes(frame.f_locals["self"])
         for attributeName, attributeValue in attributes.items():
            if type(attributeValue) != types.FunctionType:
               attributeClassName = self.getClassName(attributeValue)
               #self.addAttributeInfo(attributeName, attributeClassName)
               if self.collectInfoAboutThisClass(attributeClassName) and \
                      attributeClassName not in self.selfReferences:
                  self.selfReferences.append(attributeClassName)
      
   def getInfo(self):
      return self.selfReferences

   def addAttributeInfo(self, attributeName, attributeClassName):
      "private"
      if self.attributeInfo.has_key(attributeName):
         if attributeClassName not in self.attributeInfo[attributeClassName]:
            self.attributeInfo[attributeClassName].append(attributeClassName)
      else:
            self.attributeInfo[attributeClassName] = [attributeClassName]
         

   
