# $Id: AttributeInfoGatherer.py,v 1.4 2003/10/16 17:25:26 adamf Exp $  

import types

from PyUMLGraph.Gatherer import Gatherer

class AttributeInfoGatherer(Gatherer):
   def __init__(self, classesToCollectInfoAbout, classesToIgnore):
      Gatherer.__init__(self, classesToCollectInfoAbout, classesToIgnore)
      self.attributeInfo = {}           # { name : [className, className, ..] }

   def __repr__(self):
      return repr(self.attributeInfo)

   def collectInfo(self, frame, event, arg):
      if "self" in frame.f_locals.keys():
         attributes = self.getInstanceAttributes(frame.f_locals["self"])
         for attributeName, attributeValue in attributes.items():
            if type(attributeValue) != types.FunctionType:
               attributeClassName = self.getClassName(attributeValue)
               self.addAttributeInfo(attributeName, attributeClassName)

   def getInfo(self):
      return self.attributeInfo

   def addAttributeInfo(self, attributeName, attributeClassName):
      "private"
      if self.attributeInfo.has_key(attributeName):
         if attributeClassName not in self.attributeInfo[attributeName]:
            self.attributeInfo[attributeName].append(attributeClassName)
      else:
            self.attributeInfo[attributeName] = [attributeClassName]

