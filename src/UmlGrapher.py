# $Id: UmlGrapher.py,v 1.3 2003/10/16 17:25:26 adamf Exp $  $

from PyUMLGraph.FileUtils import FileUtils
from PyUMLGraph.InfoCollector import InfoCollector
from PyUMLGraph.ClassInfo import MIN

class UmlGrapher:
    def __init__(self):
        self.infoCollector = InfoCollector( None )

    def run(self, cmd):
        import __main__
        dict = __main__.__dict__
        self.infoCollector.collectInfoYes()
        try:
            exec cmd in dict, dict
        finally:
            self.infoCollector.collectInfoNo()

    def getDotFormatUml(self, **kwargs):
        return self.infoCollector.getDotFormattedInfo(**kwargs)        

    def outputDotFormatUml(self, outputFile, **kwargs):
        dotFormatUml = self.getDotFormatUml(**kwargs)
        if outputFile == None:
            print dotFormatUml
        else:
            FileUtils().writeEntireTextFile(outputFile, dotFormatUml)
        

