#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os
from cx_Freeze import setup, Executable

# -----------------------------------------------------------------------------
# Settings
# -----------------------------------------------------------------------------

# Paths
path = sys.path + ["ui", "graphics"]
python_dir = os.path.split(sys.executable)[0]

# Environment
os.environ['TCL_LIBRARY'] = python_dir + "\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = python_dir + "\\tcl\\tk8.6"

# Modules inclusions / exclusions
includes = ['numpy.core._methods', 'numpy.lib.format']
excludes = []
packages = ['numpy', 'PIL', 'serial', 'pyqtgraph']

# Include files
includefiles = [# README.txt CHANGELOG.txt
                'rc/imcc.png',
                ('rc/table_2017.png', 'rc/table_2017.png')
                ]

if sys.platform == "win32":
    pass
    # includefiles += [...] : windows-specific include files
elif sys.platform == "linux2":
    pass
    # includefiles += [...] : linux-specific include files
else:
    pass
    # includefiles += [...] :

# /usr/lib also copied under linux
binpathincludes = []
if sys.platform == "linux2":
    binpathincludes += ["/usr/lib"]

# Optimization level
optimize = 0

# Only displays warnings & errors
silent = True

# Options dictionary
options = {"path": path,
           "includes": includes,
           "excludes": excludes,
           "packages": packages,
           "include_files": includefiles,
           "bin_path_includes": binpathincludes,
           "optimize": optimize,
           "silent": silent
           }

# So that windows system DLLs are also included
if sys.platform == "win32":
    options["include_msvcr"] = True

# -----------------------------------------------------------------------------
# Targets preparation
# -----------------------------------------------------------------------------

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # GUI App
    # base = "Console" # Console App

bin_icon = None
if sys.platform == "win32":
    bin_icon = 'rc/imcc.ico'

# -----------------------------------------------------------------------------
# Targets
# -----------------------------------------------------------------------------

target1 = Executable(
    targetName="IMCC.exe",
    script="main.py",
    base=base,
    icon=bin_icon
)

# -----------------------------------------------------------------------------
# Setup build
# -----------------------------------------------------------------------------

setup(
    name="soft_imcc",
    version="1.0.0",
    description="IgreBot 's Mission Control Center",
    author="Bebop35",
    options={"build_exe": options},
    executables=[target1]
)
