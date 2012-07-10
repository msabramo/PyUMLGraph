# $Id: MethodArgumentsOrderGatherer.py,v 1.3 2003/10/16 17:25:26 adamf Exp $  

import types

from PyUMLGraph.Gatherer import Gatherer

class MethodArgumentsOrderGatherer(Gatherer):
   def __init__(self, classesToCollectInfoAbout, classesToIgnore):
      Gatherer.__init__(self, classesToCollectInfoAbout, classesToIgnore)
      self.methodArgumentsOrder = {}    # { methodName : [argOne, argTwo, ...] }   

   def __repr__(self):
      return repr(self.methodArgumentsOrder)

   def collectInfo(self, frame, event, arg):
      methodName = self.getMethodName(frame)
      self.methodArgumentsOrder[methodName] = frame.f_code.co_varnames[:frame.f_code.co_argcount]

   def getInfo(self):
      return self.methodArgumentsOrder


   
