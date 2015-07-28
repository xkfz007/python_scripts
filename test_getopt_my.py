#!/bin/python
__author__ = 'hfz2597'
import sys
import getopt

print sys.argv
if len(sys.argv) == 1:
  sys.exit()

try:
  opts, args = getopt.gnu_getopt(sys.argv[1:], 'ab:cd')
except getopt.GetoptError as err:
  print str(err)
  sys.exit(2)
except Exception, e:
  print e

opt_list = ""
for opt, arg in opts:
  if opt == "-a":
    opt_list += "-a "
  elif opt == "-b":
    opt_list += "-b[%s] " % arg
  elif opt == "-c":
    opt_list += "-c "
  elif opt == "-d":
    opt_list += "-d "
  else:
    assert False, "unknown option"

print "opts=%s" % opt_list
for i in args:
  print "args=%s" % i
