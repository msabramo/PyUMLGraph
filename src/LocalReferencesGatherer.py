# $Id: LocalReferencesGatherer.py,v 1.3 2003/10/16 17:25:26 adamf Exp $  $

import types

from PyUMLGraph.Gatherer import Gatherer

class LocalReferencesGatherer(Gatherer):
   def __init__(self, classesToCollectInfoAbout, classesToIgnore):
      Gatherer.__init__(self, classesToCollectInfoAbout, classesToIgnore)
      self.localReferences = []

   def __repr__(self):
      return repr(self.localReferences)

   def collectInfo(self, frame, event, arg):
      self.collectFunctionReturnValueInfo(arg)
      for localVarName, localVarValue in frame.f_locals.items():
         if localVarName != "self":
            localVarClassName = self.getClassName(localVarValue)
            if self.collectInfoAboutThisClass(localVarClassName):
               if localVarClassName not in self.localReferences:
                  self.localReferences.append(localVarClassName)
      
   def getInfo(self):
      return self.localReferences

   def collectFunctionReturnValueInfo(self, returnValue):
      "private"
      if returnValue is None:
         return
      returnValueClassName = self.getClassName(returnValue)
      if self.collectInfoAboutThisClass(returnValueClassName):
         if returnValueClassName not in self.localReferences:
            self.localReferences.append(returnValueClassName)


   
