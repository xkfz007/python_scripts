#!/bin/python
# grep wrapper
__author__ = 'hfz2597'
import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils
import os
BIN='grep'
logger=utils.Log('GREP','info')
def usage():
  msg='''USAGE: g.py [OPTIONS]... PATTERN [PATH/FILE]...
   OPTIONS:
     -i, --ignore-case    ignore case distinctions
     -w, --word-regexp    force PATTERN to match only whole words
     -x, --line-regexp    force PATTERN to match only whole lines
     -n, --line-number    print line number with output lines
     -o, --only-matching  show only the part of a line matching PATTERN
     -r, --recursive      like --directories=recurse
     -I                   don't search binary files, equivalent to --binary-files=without-match
     -a, --text           equivalent to --binary-files=text
     -b, --byte-offset    print the byte offset with output lines
     -L, --files-without-match
                          print only names of FILEs containing no match
     -l, --files-with-matches
                          print only names of FILEs containing matches
         --include=FILE_PATTERN  search only files that match FILE_PATTERN
         --exclude=FILE_PATTERN  skip files and directories matching FILE_PATTERN
         --exclude-from=FILE     skip files matching any file pattern from FILE
         --exclude-dir=PATTERN   directories that match PATTERN will be skipped.
  '''
  print msg
  return

if __name__ == '__main__':
    #print sys.argv
    if len(sys.argv) == 1:
      usage() #usage()
      sys.exit()

    help=utils.HELP(usage,BIN,'--help',logger)

    options='iwxnorIabLl'
    long_options=['include=','exclude=','exclude-from=','exclude-dir=']

    opts,args=utils.my_getopt_long(sys.argv[1:],options+help.get_opt(),long_options)
    print opts
    print args

    #do_execute=0
    opt_list='In'
    long_opt_list=[]
    for opt, arg in opts:
      if opt[1] in options:
        if not opt[1] in opt_list:
          opt_list+=opt[1]
      elif opt[2:]+'=' in long_options:
          long_opt_list.append((opt,arg))
      #elif opt == '-h':
      #    usage()
      #    sys.exit()
      else:
        help.parse_opt(opt)
    print opt_list
    print long_opt_list

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
        tmp=i.replace('(','\(').replace(')','\)').strip(' ')
#         tmp=tmp.replace('-','\-')
        pattern_list.append(tmp)
      else:
        dir_or_file=i

    if len(pattern_list)==0:
      logger.error('BAD')
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
    for k, v in long_opt_list:
        cmd+=' %s=%s'%(k,v)
    #print cmd
    #if help.get_do_execute()==1:
    #    os.system(cmd)
    #lib.run_cmd(cmd,help.get_do_execute())
    utils.run_cmd(cmd,1)
