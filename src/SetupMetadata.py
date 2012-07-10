import sys
from distutils import core

from Version import PROGRAM_VERSION

class SetupMetadata:
    def getMetadata(self):
        metadata = {'name' : "PyUMLGraph",
                    'version' : PROGRAM_VERSION,
                    'author' : "Adam Feuer",
                    'author_email' : "adamf@pobox.com",
                    'url' : "http://www.pobox.com/~adamf/software/PyUMLGraph/",
                    'license' :  "http://www.pobox.com/~adamf/software/PyUMLGraph/COPYING.txt",
                    'platforms' :  ["any"],
                    'description' :  self.getDocLines()[0],
                    'long_description' :  "\n".join(self.getDocLines()[1:]),
                    'package_dir' :  { "PyUMLGraph" : "src" },
                    'packages' :  [ "PyUMLGraph" ],
                    'scripts' :  ['src/pyumlgraph'],
                    }

        if self.platformIsWindowsOrDos():
            metadata['scripts'] = ['src/pyumlgraph.py']

        if (hasattr(core, 'setup_keywords') and
            'classifiers' in core.setup_keywords):
            metadata['classifiers'] = \
                      ['Development Status :: 3 - Alpha',
                       'Intended Audience :: Developers',
                       'License :: OSI Approved :: GNU General Public License (GPL)',
                       'Programming Language :: Python',
                       'Topic :: Software Development :: Documentation',
                       'Topic :: Software Development :: Debuggers',
                       'Topic :: Utilities',
                       'Topic :: Software Development :: Libraries :: Python Modules',
                       'Operating System :: OS Independent',
                       'Operating System :: Microsoft :: Windows',
                       'Operating System :: Unix']
        return metadata

    def platformIsWindowsOrDos(self):
        "@private"
        if sys.platform == 'win32' or \
           sys.platform == 'dos' or \
           sys.platform[0:6] == 'ms-dos':
           return True
        else:
           return False
        
    def getDocLines(self):
       "@private"
       doclines = """Generate UML graphs from running Python programs
PyUMLGraph is a Python debugger that produces UML diagrams by
inspecting running programs. The output is in Graphiz's dot language,
and dot can produce pictures in many popular formats, such as PNG,
PDF, SVG, and others. The UML diagrams can contain information
about class inheritance relationships, references to other classes,
class methods and return types, as well as class attributes and types.
"""
       return doclines.split("\n")

