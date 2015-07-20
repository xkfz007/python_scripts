#!/bin/python
__author__ = 'hfz2597'
import sys
import getopt
import os
def help():
  msg='''usage:grep.py [options] pattern [path or file]
  -i, --ignore-case         ignore case distinctions
  -w, --word-regexp         force PATTERN to match only whole words
  -x, --line-regexp         force PATTERN to match only whole lines
  -n, --line-number         print line number with output lines
  -o, --only-matching       show only the part of a line matching PATTERN
  -r, --recursive           like --directories=recurse
  -I                        don't search binary files, equivalent to --binary-files=without-match
  -a, --text                equivalent to --binary-files=text
  -b, --byte-offset         print the byte offset with output lines
  '''
  print msg
  return
#print sys.argv
if len(sys.argv) == 1:
  help()
  sys.exit()

options="iwxnorIab"
try:
  opts, args = getopt.gnu_getopt(sys.argv[1:], ':'+options)
except getopt.GetoptError as err:
  print str(err)
  sys.exit(2)
except Exception, e:
  print e

if len(args)<1:
  help()
  sys.exit()

opt_list=""
for opt, arg in opts:
  #if opt == "-i":
  #  opt_list+="i"
  #elif opt == "-w":
  #  opt_list+="w"
  #elif opt == "-x":
  #  opt_list+="x"
  #elif opt == "-n":
  #  opt_list+="n"
  #elif opt == "-o":
  #  opt_list+="o"
  #elif opt == "-r":
  #  opt_list+="r"
  if opt[1] in options:
    opt_list+=opt[1]
  else:
    assert False, "unknown option"

#print "opts=%s"%opt_list
#for i in args:
#  print "args=%s"%i

pattern=args[0]

dir_or_file=""
if len(args)>1:
  dir_or_file=args[1]
if len(dir_or_file)==0:
  dir_or_file="."
if os.path.isdir(dir_or_file):
  if 'r' not in opt_list:
    opt_list+="r"
BIN="grep --color"
#cmd="grep --color -"+opt_list+" "+pattern+" "+dir_or_file
cmd=BIN
cmd+=" -%s"%opt_list
cmd+=" %s"%pattern
cmd+=" %s"%dir_or_file
print cmd
os.system(cmd)
