# $Id: MethodArgumentsDefaultsGatherer.py,v 1.3 2003/10/16 17:25:26 adamf Exp $  

import types

from PyUMLGraph.Gatherer import Gatherer

class MethodArgumentsDefaultsGatherer(Gatherer):
   def __init__(self, classesToCollectInfoAbout, classesToIgnore):
      Gatherer.__init__(self, classesToCollectInfoAbout, classesToIgnore)
      self.methodArgumentsDefaults = {} # { methodName : [defaultOne, defaultTwo, ...] }   

   def __repr__(self):
      return repr(self.methodArgumentsDefaults)

   def collectInfo(self, frame, event, arg):
      methodName = self.getMethodName(frame)
      if "self" in frame.f_locals:
         classInstance = frame.f_locals["self"]
         defaultsDescriptions = []
         if self.getClassAttributes(classInstance).has_key(self.demangleName(classInstance, methodName)):
            functionDefaults = self.getClassAttributes(classInstance)[self.demangleName(classInstance, methodName)].func_defaults
            if functionDefaults is not None:
               for item in functionDefaults:
                  defaultsDescriptions.append(self.getObjectDescription(item))
               self.methodArgumentsDefaults[methodName] = defaultsDescriptions

   def getInfo(self):
      return self.methodArgumentsDefaults

   def getObjectDescription(self, object):
      "private"
      description = repr(object)
      if description.find('instance at 0x') > 0:
         description = description[:description.find(' at 0x')] + '>'
      return description



