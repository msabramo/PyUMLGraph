# $Id: MethodArgumentsInfoGatherer.py,v 1.3 2003/10/16 17:25:26 adamf Exp $  

import types

from PyUMLGraph.Gatherer import Gatherer

class MethodArgumentsInfoGatherer(Gatherer):
   def __init__(self, classesToCollectInfoAbout, classesToIgnore):
      Gatherer.__init__(self, classesToCollectInfoAbout, classesToIgnore)
      self.methodArgumentsInfo = {}     # { methodName : {argName : [className, ...]}}

   def __repr__(self):
      return repr(self.methodArgumentsInfo)

   def collectInfo(self, frame, event, arg):
      if event != "call":
         return
      methodArgumentsInfo = frame.f_locals.copy()
      if not methodArgumentsInfo.has_key("self"):
         return
      del(methodArgumentsInfo["self"])
      methodName = frame.f_code.co_name
      for argumentName, argumentValue in methodArgumentsInfo.items():
         argumentClassName = self.getClassName(argumentValue)
         self.addArgumentsInfo(methodName, argumentName, argumentClassName)

   def getInfo(self):
      return self.methodArgumentsInfo

   def addArgumentsInfo(self, methodName, argumentName, argumentClassName):
      "private"
      if not self.methodArgumentsInfo.has_key(methodName):
         self.methodArgumentsInfo[methodName] = {}
      if self.methodArgumentsInfo[methodName].has_key(argumentName):
         if argumentClassName not in self.methodArgumentsInfo[methodName][argumentName]:
            self.methodArgumentsInfo[methodName][argumentName].append(argumentClassName)
      else:
         self.methodArgumentsInfo[methodName][argumentName] = [argumentClassName]


