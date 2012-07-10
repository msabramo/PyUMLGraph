#!/usr/bin/env python
# $Id: unit.py,v 1.4 2003/10/22 22:25:04 adamf Exp $

import sys, os, re, unittest

def adjustPath():
   # Assumes package dirname is module name
   parentDir = os.path.split(os.getcwd())[0]
   moduleName = os.path.split(parentDir)[1]
   src = os.path.join(parentDir, "src")
   dest = os.path.join(parentDir, moduleName)
   try:
      os.symlink(src, dest)
   except:
      pass
   sys.path.append(parentDir)

def regressionTest():
   path = os.path.abspath(os.getcwd())
   files = os.listdir(path)                   
   test = re.compile("test.py$", re.IGNORECASE)
   files = filter(test.search, files)         
   filenameToModuleName = lambda f: os.path.splitext(f)[0]
   moduleNames = map(filenameToModuleName, files)        
   modules = map(__import__, moduleNames)                
   load = unittest.defaultTestLoader.loadTestsFromModule
   return unittest.TestSuite(map(load, modules))

if __name__ == "__main__":
   adjustPath()
   unittest.main(defaultTest="regressionTest")
