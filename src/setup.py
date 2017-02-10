#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os
from cx_Freeze import setup, Executable

# -----------------------------------------------------------------------------
# Settings
# -----------------------------------------------------------------------------

# Paths
path = sys.path + ["ui", "graphics"]

# Modules inclusions / exclusions
includes = []

excludes = []

packages = ['os', 'threading','queue',
            'numpy', 'PIL', 'serial',
            'PyQt5', 'pyqtgraph']

# Include files
includefiles = ['rc/imcc.png']

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

target1 = Executable(
    script="main.py",
    base=base,
    icon=bin_icon
)

# -----------------------------------------------------------------------------
# Setup build
# -----------------------------------------------------------------------------

setup(
    name="soft_imcc",
    version="1.00",
    description="IgreBot 's Mission Control Center",
    author="Bebop35",
    options={"build_exe": options},
    executables=[target1]
)
