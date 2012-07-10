# $Id: Gatherer.py,v 1.2 2003/10/16 17:25:26 adamf Exp $  $

import types

class Gatherer:
   def __init__(self, classesToCollectInfoAbout, classesToIgnore):
      self.classesToCollectInfoAbout = classesToCollectInfoAbout
      self.classesToIgnore = classesToIgnore

   def __repr__(self):
      raise "This method should be overriden."

   def gatherInfo(self, frame, event, arg):
      raise "This method should be overriden."

   def getInfo(self):
      raise "This method should be overriden."

   def getClassName(self, object):
      "private"
      try:
         className = object.__class__.__name__
      except AttributeError:
         return "None"
      if className == "NoneType":
         return "None"
      else:
         return className

   def getClassAttributes(self, object):
      "private"
      return object.__class__.__dict__      

   def getInstanceAttributes(self, object):
      "private"
      return object.__dict__      

   def getMethodName(self, frame):
      "private"
      return frame.f_code.co_name

   def demangleName(self, object, name):
      "private"
      if type(name) != type(""):
         return name
      if len(name) < 3:
         return name
      if name[:2] == "__" and name[-2:] != "__":
         return "_" + object.__class__.__name__ + name
      else:
         return name


   def collectInfoAboutThisClass(self, className):
      "private"
      if className in self.classesToIgnore:
         return False
      elif self.classesToCollectInfoAbout is None:
         return True
      else:
         return className in self.classesToCollectInfoAbout
