#!/bin/python
__author__ = 'hfz2597'
import commands
import os
import sys
import lib.common_lib
import getopt
import logging
def usage():
    msg='''USAGE: rep.py [OPTIONS]... PATTERN REPLACEMENT [PATH/FILE]...
   OPTIONS:
     -e <string>  extension of file that will be modified,like ".py", ".c", ".cpp"
   PATTERN:
     strings that will to be replaced
   REPLACEMENT:
     strings we will use to replace PATTERN
   PATH/FILE:
     in which files that we will do the replacement
  '''
    print msg
    return
if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
        sys.exit()
    help=lib.common_lib.HELP(usage)
    #do_execute=0
    options='e:'
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], ':'+options+help.get_opt())
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    except Exception, e:
        print e

    ext=''
    for opt, arg in opts:
        if opt == '-e':
            extension = arg
        else:
            help.parse_opt(opt)

    if len(args) == 0:
        logging.error('No PATTERN is specified, please check')
        sys.exit()
    elif len(args) == 1:
        logging.error('No REPLACEMENT is specified, please check')
        sys.exit()

    print 'args=%s'%args
    pattern=args[0]
    replacement=args[1]

    if len(args)>2:
        input_list=args[2:]
    else:
        input_list=['.',]

    dir_file_list=[]
    for i in input_list:
        lib.get_input_file_or_dir_list(dir_file_list,i)

    print 'dir_file_list=%s'%dir_file_list

    file_modify_list=[]
    for i in dir_file_list:
        cmd='grep -rlI "%s" "%s"'%(pattern,i)
        print cmd
        (status,output)=commands.getstatusoutput(cmd)
        file_modify_list.extend(output.splitlines())

    print 'file_modify_list=%s'%file_modify_list

    cmd_list=[]
    for i in file_modify_list:
       if os.path.isfile(i):
          cmd='sed -i "s/%s/%s/g" "%s"'%(pattern,replacement,i)
          cmd_list.append(cmd)
#
    for cmd in cmd_list:
        lib.run_cmd(cmd,help.get_do_execute())
