#!/bin/python
# find wrapper
__author__ = 'hfz2597'
import sys
import getopt
import os
def help():
  msg='''usage:find.py [options] pattern [path]
         -iname pattern
         -type [df]
         -size [-+]n[cbkMG]
         -empty
  '''
  print msg
  return
#print sys.argv
if len(sys.argv) == 1:
  help()
  sys.exit()

options="ifde:m:"
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
pattern=""
name_pat="-name"
type_pat=""
excl_list=[]
maxdep_pat=""
for opt, arg in opts:
  if opt == "-i":
    name_pat="-iname"
  elif opt == "-f":
    type_pat="-type f"
  elif opt == "-d":
    type_pat="-type d"
  elif opt == "-e":
    excl_list.append("'"+arg+"'")
  elif opt == "-m":
    maxdep_pat="-maxdepth %s"%arg
  #elif opt == "-r":
  #  opt_list+="r"
  #if opt[1] in options:
  #  opt_list+=opt[1]
  else:
    assert False, "unknown option"

if len(excl_list)==0:
  excl_pat=""
else:
  excl_pat="\( -path "
  excl_pat+=" -o -path ".join(excl_list)
  excl_pat+=" \)"
  excl_pat+=" -prune -o"

dir_or_file=""
name_list=[]
for i in args:
  if not os.path.isdir(i):
    name_list.append("'"+i+"'")
  else:
    dir_or_file=i

if len(name_list)==0:
  print "BAD"
  sys.exit()
else:
  name_pat2="\( "+name_pat+" "
  name_pat2+=(" -o "+name_pat+" ").join(name_list)
  name_pat2+=" \)"

if len(dir_or_file)==0:
  dir_or_file="."

BIN="find"
cmd=BIN
cmd+=" %s"%dir_or_file
cmd+=" %s"%maxdep_pat
cmd+=" %s"%excl_pat
cmd+=" %s"%name_pat2
cmd+=" -print"
print cmd
os.system(cmd)
