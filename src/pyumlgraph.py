#!/usr/bin/env python

# Copyright 2003, Adam Feuer, all rights reserved. 

"""Produce dot language UML diagrams of a Python program or function execution.

Sample use, command line:
  $pyumlgraph -o program.dot program.py
  $dot -Tpng -o program.png program.dot

Note: You will need to use Graphviz's dot program to transform the dot files to pictures.
  
"""

# $Id: pyumlgraph,v 1.10 2003/10/18 04:53:26 adamf Exp $

# hack to make my testing work
try:
    import config 
except:
    pass

import sys, os
from PyUMLGraph.UmlGrapher import UmlGrapher
from PyUMLGraph.ClassInfo import MIN, MAX, ATTRIBUTES, METHODS, REFERENCES, TYPES

from PyUMLGraph.Version import PROGRAM_VERSION

def usage(outfile):
    outfile.write("""Usage: %s [OPTIONS] <Python program> [ARGS]

-o <outputfile>         write dot language UML output to this file

--help                  Display this help then exit.
--version               Output version information then exit.

--types                 Include common types (str, int, dict, etc.)
--methods               Show class methods
--attributes            Show class attributes
--references            Distinguish between self and local references
--all                   Equivalent to --types --methods --attributes --references

--nodefillcolor=<color> Set the node fill color to this string.
                        <color> can be Unix color name or a hex 3-tuple.

--bgcolor=<color>       Set the diagram's background color to this string.
                        <color> can be Unix color name or a hex 3-tuple.
""" % sys.argv[0])

def errorExit(message):
    sys.stderr.write("%s: %s\n" % (sys.argv[0], message))
    sys.exit(1)

def main(argv=None):
    import getopt

    if argv is None:
        argv = sys.argv
    try:
        opts, prog_argv = getopt.getopt(argv[1:], "hvo:",
                                        ["help", "version",
                                         "nodefillcolor=",
                                         "bgcolor=",
                                         "all",
                                         "attributes",
                                         "methods",
                                         "references",
                                         "types"])

    except getopt.error, msg:
        sys.stderr.write("%s: %s\n" % (sys.argv[0], msg))
        sys.stderr.write("Try `%s --help' for more information\n" % sys.argv[0])
        sys.exit(1)

    # set option variables here
    outputFile = None
    detailLevel = MIN
    nodeFillColor = ""
    backgroundColor = "white"

    for opt, val in opts:
        if opt == "--help" or opt == "-h":
            usage(sys.stdout)
            sys.exit(0)

        if opt == "--version":
            sys.stdout.write("%s %s\n" %("PyUMLGraph", PROGRAM_VERSION))
            sys.exit(0)

        if opt == "-o":
            outputFile = val
            continue

        if opt == "--all":
            detailLevel = MAX

        if opt == "--attributes":
            detailLevel = detailLevel | ATTRIBUTES

        if opt == "--methods":
            detailLevel = detailLevel | METHODS

        if opt == "--references":
            detailLevel = detailLevel | REFERENCES

        if opt == "--types":
            detailLevel = detailLevel | TYPES

        if opt == "--nodefillcolor":
            nodeFillColor = val
            
        if opt == "--bgcolor":
            backgroundColor = val
            

    if len(prog_argv) == 0:
        errorExit("missing name of Python program to run.")
            
    sys.argv = prog_argv
    progname = prog_argv[0]
    sys.path[0] = os.path.split(progname)[0]

    umlGrapher = UmlGrapher()

    try:
        umlGrapher.run('execfile(' + `progname` + ')')
    except IOError, err:
        errorExit("Cannot run file %s because: %s" % (`sys.argv[0]`, err))
    except SystemExit:
        pass

    umlGrapher.outputDotFormatUml(outputFile,
                                  detailLevel=detailLevel,
                                  nodeFillColor=nodeFillColor,
                                  backgroundColor=backgroundColor,
                                  )

if __name__=='__main__':
    main()
