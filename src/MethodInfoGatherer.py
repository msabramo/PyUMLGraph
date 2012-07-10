# $Id: MethodInfoGatherer.py,v 1.3 2003/10/16 17:25:26 adamf Exp $

import types

from PyUMLGraph.Gatherer import Gatherer

class MethodInfoGatherer(Gatherer):
   def __init__(self, classesToCollectInfoAbout, classesToIgnore):
      Gatherer.__init__(self, classesToCollectInfoAbout, classesToIgnore)
      self.methodInfo = {}              # { name:  "public" or "private"}
      self.privateIndicator = "private"
      self.publicIndicator = "public"

   def __repr__(self):
      return repr(self.methodInfo)

   def collectInfo(self, frame, event, arg):
      if "self" in frame.f_locals:
         classInstance = frame.f_locals["self"]
         classAttributes = self.getClassAttributes(classInstance)
         for attributeName in classAttributes.keys():
            if type(classAttributes[attributeName]) == types.FunctionType:
               if classAttributes[attributeName].__doc__ == self.privateIndicator:
                  self.methodInfo[attributeName] = self.privateIndicator
               else:
                  self.methodInfo[attributeName] = self.publicIndicator

   def getInfo(self):
      return self.methodInfo


