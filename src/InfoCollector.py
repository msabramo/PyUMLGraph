# $Id: InfoCollector.py,v 1.3 2003/10/16 17:25:26 adamf Exp $  

import sys

from PyUMLGraph.ClassInfo import ClassInfo, MIN, ATTRIBUTES, METHODS, TYPES, MAX
from PyUMLGraph.Gatherer import Gatherer

class InfoCollector:
   def __init__(self, classesToCollectInfoAbout = []):
      self.classesToCollectInfoAbout = classesToCollectInfoAbout
      self.classesToIgnore = [ None, self.__class__.__name__ ]
      self.classesInfo = {}
      self.gatherer = Gatherer(self.classesToCollectInfoAbout, self.classesToIgnore)

   def collectInfoYes(self):
      sys.settrace(self.globalTrace)

   def collectInfoNo(self):
      sys.settrace(None)

   def getInfo(self):
      return self.classesInfo

   def getYamlInfo(self):
      yamlClassesInfo = self.classesInfo.copy()
      for key in yamlClassesInfo.keys():
         yamlClassesInfo[key] = yamlClassesInfo[key].getYamlInfo()
      return yamlClassesInfo

   def getFormattedInfo(self):
      result = ""
      for className, classInfo in self.classesInfo.items() :
         result += "%s: %s\n" % (className, classInfo.getFormattedInfo() )
      return result

   def getDotFormattedInfo(self, **options):
      dotInfo = ""
      options = self.fillOutDefaultOptions(**options)
      dotInfo += self.getDotHeader(**options)
      for className, classInfo in self.classesInfo.items():
         dotInfo += classInfo.getDotRepresentation(**options)
      dotInfo += self.getDotFooter()
      return dotInfo

   def globalTrace(self, frame, event, arg):
      "private"
      if event == "call":
         self.collectInfo(frame, event, arg)
      return self.localTrace

   def localTrace(self, frame, event, arg):
      "private"
      if event == "return":
         className, functionName = self.getClassAndFunctionName(frame)
         locals = frame.f_locals
         globals = frame.f_globals
         self.collectInfo(frame, event, arg)

   def collectInfo(self, frame, event, arg = None):
      "private" 
      className, functionName = self.getClassAndFunctionName(frame)
      if className == ""  and functionName in self.classesToCollectInfoAbout:
         self.collectInfoForClass(functionName, frame, event, arg)
      elif self.gatherer.collectInfoAboutThisClass(className):
         self.collectInfoForClass(className, frame, event, arg)

   def getClassAndFunctionName(self, frame):
      "private"
      className = None
      functionName = frame.f_code.co_name
      if "self" in frame.f_locals:
         className = frame.f_locals["self"].__class__.__name__
      return className, functionName

   def collectInfoForClass(self, className, frame, event, arg):
      "private"
      if not self.classesInfo.has_key(className):
         self.classesInfo[className] = ClassInfo(className,
                                                 self.classesToCollectInfoAbout,
                                                 self.classesToIgnore)
      classInfo = self.classesInfo[className]
      classInfo.collectInfo(frame, event, arg)

   def fillOutDefaultOptions(self, **options):
      options["detailLevel"] = options.get("detailLevel", MIN)      
      options["outlineColor"] = options.get("outlineColor", "black")
      options["backgroundColor"] = options.get("backgroundColor", "white")
      options["nodeFillColor"] = options.get("nodeFillColor", "")
      if options["nodeFillColor"] == "":
         options["nodeStyle"] = options.get("nodeStyle", "")
      else:
         options["nodeStyle"] = options.get("nodeStyle", "filled")
      if options["detailLevel"] == MIN:
         options["nodeShape"] = "record"
      else:
         options["nodeShape"] = "record"
      return options

   def getDotHeader(self, **options):
      "private"
      return """graph UML {
  nodesep=0.3;
  color="%(outlineColor)s"
  bgcolor="%(backgroundColor)s"
  node [fontsize=10];

""" % options

   def getDotFooter(self):
      "private"
      return "\n}\n"

   
