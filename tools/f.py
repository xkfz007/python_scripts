#!/bin/python
# find wrapper: search for files in a directory hierarchy
__author__ = 'hfz2597'
import sys
import getopt
import os
import lib.common_lib
BIN='find'
def usage():
  msg='''USAGE: f.py [OPTIONS]... PATTERN [PATH]...
   OPTIONS:
     -i  forked from -iname of find, to match the PATTERN with case insensitive
     -f  forked from -type d of find, to find file of the requested type
     -d  forked from -type d of find, to find file of the requested type
     -e <string>
         paths/directories that will be excluded
     -m <integer>
         forked from -maxdepth of find, to descend at most levels
   PATTERN:
     patterns of files that we want to find
   PATH:
     path in which we want to find files
  '''
  print msg
  return


if __name__ == '__main__':
    #print sys.argv
    if len(sys.argv) == 1:
      usage()
      sys.exit()

    help=lib.common_lib.HELP(usage,BIN,'--help')
    #do_execute=0
    options='ifde:m:'
    try:
      opts, args = getopt.gnu_getopt(sys.argv[1:], ':'+options+help.get_opt())
    except getopt.GetoptError as err:
      print str(err)
      sys.exit(2)
    except Exception, e:
      print e


    opt_list=''
    name_opts='-name'
    type_opts=''
    exclude_path_list=[]
    maxdep_opts=''
    for opt, arg in opts:
      if opt == '-i':
        name_opts='-iname'
      elif opt == '-f':
        type_opts='-type f'
      elif opt == '-d':
        type_opts='-type d'
      elif opt == '-e':
        exclude_path_list.append('"'+arg+'"')
      elif opt == '-m':
        maxdep_opts='-maxdepth %s'%arg
      else:
        help.parse_opt(opt)

    if len(args)<1:
        help.usage()
        sys.exit()

    if len(exclude_path_list)==0:
      excl_pat=''
    else:
      excl_pat='\( -path '
      excl_pat+=' -o -path '.join(exclude_path_list)
      excl_pat+=' \)'
      excl_pat+=' -prune -o'

    dir_or_file=''
    name_pat_list=[]
    for i in args:
      if not os.path.isdir(i):
        name_pat_list.append('"'+i+'"')
      else:
        dir_or_file=i

    if len(name_pat_list)==0:
      print 'BAD'
      sys.exit()
    else:
      name_pat2='\( '+name_opts+' '
      name_pat2+=(' -o '+name_opts+' ').join(name_pat_list)
      name_pat2+=' \)'

    if len(dir_or_file)==0:
      dir_or_file='.'

    cmd=BIN
    cmd+=' %s'%dir_or_file
    cmd+=' %s'%maxdep_opts
    cmd+=' %s'%excl_pat
    cmd+=' %s'%name_pat2
    cmd+=' -print'
    #print cmd
    #if help.get_do_execute()==1:
    #    os.system(cmd)
    lib.run_cmd(cmd,help.get_do_execute())
