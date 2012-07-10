PyUMLGraph

by Adam Feuer

http://www.pobox.com/~adamf/software/PyUMLGraph

------------------------------------------------------------------------

PyUMLGraph is a Python debugger that produces UML diagrams by
inspecting running Python programs. The output is in Graphiz's dot
language, and dot can produce pictures in many popular formats, such
as PNG, PDF, SVG, and others. The UML diagrams can contain information
about class inheritance relationships, references to other classes,
class methods and return types, as well as class attributes and types.

Sample use from the command line:
  $pyumlgraph -o simple.dot simple.py
  $dot -Tpng -o simple.png simple.dot

You can find the simple.py file in PyUMLGraph's src/ directory.

Note: You will need to use Graphviz's dot program to transform the dot
files to pictures.

You can find out about Graphviz and dot here: 
http://www.research.att.com/sw/tools/graphviz/

Here are the commandline options:

-o <outputfile>         write dot language UML output to this file

--help                  Display this help then exit.
--version               Output version information then exit.

--types                 Include common types (str, int, dict, etc.)
--methods               Show class methods
--references            Distinguish between self and local references
--attributes            Show class attributes
--all                   Equivalent to --types --methods --attributes --references

--nodefillcolor=<color> Set the node fill color to this string.
                        <color> can be Unix color name or a hex 3-tuple.

--bgcolor=<color>       Set the diagram's background color to this string.
                        <color> can be Unix color name or a hex
                        3-tuple.


License
-------

PyUMLGraph is free software provided under the Gnu Public License.
See the file COPYING.txt or http://www.gnu.org/licenses/gpl.txt


Installation
------------

PyUMLGraph requires Python 2.2 or more recent. Make sure this is
installed, unpack PyUMLGraph to a convenient location and run

python setup.py install


Note that under Windows, you may have to use the --install-scripts 
option to tell setup.py where to put the pyumlgraph.py script:

http://www.python.org/doc/current/inst/alt-install-windows.html#SECTION000330000000000000000


Credits
-------

PyUMLGraph is inspired by Diomidis Spinellis' UMLGraph, which can
generate UML diagrams for Java software. You can see UMLGraph here:
http://www.spinellis.gr/sw/umlgraph/

Thanks to Paul DuPuy for the idea and encouragement, and Troy Frever
for pointing out that it could be done by writing a Python debugger.



If you find PyUMLGraph to be useful, please drop me a note to let me
know.

-Adam Feuer <adamf at pobox dot com>
