#!/bin/python
import lib
import os

path = "\\\\172.21.40.64\\h265\\xml"
path = lib.format_path(path)
print path
path = "f:\\tmp"
path = lib.format_path(path)
print path
path = "/cygdrive/d/extendedprogs/"
path = lib.format_path(path)
print path
print os.path.abspath("..")
