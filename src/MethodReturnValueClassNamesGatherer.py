# $Id: MethodReturnValueClassNamesGatherer.py,v 1.4 2003/10/16 17:25:26 adamf Exp $

import types

from PyUMLGraph.Gatherer import Gatherer

class MethodReturnValueClassNamesGatherer(Gatherer):
   def __init__(self, classesToCollectInfoAbout, classesToIgnore):
      Gatherer.__init__(self, classesToCollectInfoAbout, classesToIgnore)
      self.methodReturnValueClassNames = {} # { name:  [className, className] }

   def __repr__(self):
      return repr(self.methodReturnValueClassNames)

   def collectInfo(self, frame, event, arg):
      if event != "return":
         return
      methodName = self.getMethodName(frame)
      returnValueClassName = self.getClassName(arg)
      if self.methodReturnValueClassNames.has_key(methodName):
         if returnValueClassName not in self.methodReturnValueClassNames[methodName]:
             self.methodReturnValueClassNames[methodName].append(returnValueClassName)
      else:
         self.methodReturnValueClassNames[methodName] = [returnValueClassName]

   def getInfo(self):
      return self.methodReturnValueClassNames
         
