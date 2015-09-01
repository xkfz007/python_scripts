#!/bin/python
# grep wrapper
__author__ = 'hfz2597'
import sys
import getopt
import os
import lib.common_lib
BIN='grep'
def usage():
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
  usage() #usage()
  sys.exit()

help=lib.common_lib.HELP(usage,BIN,'--help')

options='iwxnorIab'
try:
  opts, args = getopt.gnu_getopt(sys.argv[1:], ':'+options+help.get_opt())
except getopt.GetoptError as err:
  print str(err)
  sys.exit(2)
except Exception, e:
  print e


#do_execute=0
opt_list='I'
for opt, arg in opts:
  #if opt == '-i':
  #  opt_list+='i'
  #elif opt == '-w':
  #  opt_list+='w'
  #elif opt == '-x':
  #  opt_list+='x'
  #elif opt == '-n':
  #  opt_list+='n'
  #elif opt == '-o':
  #  opt_list+='o'
  #elif opt == '-r':
  #  opt_list+='r'
  #print opt
  if opt[1] in options :
    if not opt[1] in opt_list:
      opt_list+=opt[1]
  #elif opt == '-h':
  #    usage()
  #    sys.exit()
  #elif opt == '-H':
  #    os.system(BIN+' --help')
  #    sys.exit()
  #elif opt == '-Y':
  #    do_execute=1
  #elif opt[1] in help.get_opt():
  #    help.parse_opt(opt)
  else:
      continue
    #assert False, 'unknown option'

help.parse_opt(opts)
#print 'opts=%s'%opt_list
#for i in args:
#  print 'args=%s'%i

#pattern=args[0]
if len(args)<1:
    help.usage()
    sys.exit()

dir_or_file=''
pattern_list=[]
for i in args:
  if not os.path.isdir(i) and not os.path.isfile(i):
    pattern_list.append(i)
  else:
    dir_or_file=i

if len(pattern_list)==0:
  print 'BAD'
  sys.exit()
else:
  pattern='|'.join(pattern_list)

#if len(args)>1:
#  dir_or_file=args[1]
if len(dir_or_file)==0:
  dir_or_file='.'
if os.path.isdir(dir_or_file):
  if 'r' not in opt_list:
    opt_list+='r'
cmd=BIN+' -E --color'
#cmd='grep --color -'+opt_list+' '+pattern+' '+dir_or_file
cmd+=' -%s'%opt_list
cmd+=' "%s"'%pattern
cmd+=' %s'%dir_or_file
print cmd
if help.get_do_execute()==1:
    os.system(cmd)
