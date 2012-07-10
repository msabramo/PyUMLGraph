#!/usr/bin/env python

# $Id: setup.py,v 1.14 2003/10/20 17:42:33 adamf Exp $

from distutils import core
from src.SetupMetadata import SetupMetadata

core.setup(**SetupMetadata().getMetadata())
