# $Id: FileUtils.py,v 1.3 2003/10/16 17:25:26 adamf Exp $  

import os
from shutil import copy, rmtree

class FileUtils:
   def writeEntireTextFile(self, filePathName, text):
      file = open(filePathName, 'w')
      file.write(text)
      file.close()

   def readEntireTextFile(self, filePathName):
      file = open(filePathName, 'r')
      contents = file.read()
      file.close()
      return contents

   def replaceTagInFile(self, tag, text, filePathName):
      contents = self.readEntireTextFile(filePathName)
      newContents = contents.replace(tag, text)
      self.writeEntireTextFile(filePathName, newContents)

   def copyFilesToDir(self, filePathNameList, dirPathName):
      for filePathName in filePathNameList:
         copy(filePathName, dirPathName)

   def forceRemoveTree(self, dirPathName):
      try:
         rmtree(dirPathName, True)
      except OSError:
         pass

   def executeShellCommand(self, commandline):
      stdin, stdout = os.popen4(commandline)
      output = stdout.read()
      print output
      return output
      
