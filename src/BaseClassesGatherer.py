# $Id: BaseClassesGatherer.py,v 1.3 2003/10/16 17:25:26 adamf Exp $  

import types

from PyUMLGraph.Gatherer import Gatherer

class BaseClassesGatherer(Gatherer):
   def __init__(self, classesToCollectInfoAbout, classesToIgnore):
      Gatherer.__init__(self, classesToCollectInfoAbout, classesToIgnore)
      self.baseClasses = []

   def __repr__(self):
      return repr(self.baseClasses)

   def collectInfo(self, frame, event, arg):
      methodName = self.getMethodName(frame)
      if "self" in frame.f_locals:
         classInstance = frame.f_locals["self"]
         baseClasses = classInstance.__class__.__bases__
         self.baseClasses = [baseClass.__name__ for baseClass in baseClasses]

   def getInfo(self):
      return self.baseClasses
