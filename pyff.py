#!/bin/python
__author__ = 'hfz2597'
import sys
import getopt
import os
import subprocess
import glob
import lib

FFMPEG_BIN = 'ffmpeg.exe -y'


def usage():
    help_msg = '''Usage:pyff.py [option] [value]...
  options:
   -i <string> input file, support pattern globbing
   -e <string> the output file extension
   -C <string> the ffmpeg commands
   -t <int> set thread num
   -Y if execute the program
   -h print the FFMpeg help
   '''
    print help_msg
    return


def get_cmd_line(input_file, ext, output_tmp, prepared_cmd, extra_cmd):
    fname, fext = os.path.splitext(input_file)
    print fname
    print fext
    if len(ext) > 0:  # '':
        if not ext.startswith('.'):
            ext = '.' + ext
    else:
        ext = fext
    output_file = "%s%s%s" % (fname, output_tmp, ext)

    cmd_line = prepared_cmd
    cmd_line += " -i \"%s\"" % input_file
    cmd_line += " %s" % extra_cmd
    cmd_line += " \"%s\"" % output_file
    return cmd_line


def get_default_opt_list():
    opt_list = {}
    # opt_list['input_tmp'] = ''
    opt_list['extra_cmd'] = ''
    opt_list['ext'] = ''
    #opt_list['output_tmp'] = ''
    opt_list['thread_num'] = 0
    opt_list['do_execute'] = 0


if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
        sys.exit()

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:e:t:C:Yh')
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    except Exception, e:
        print e

    #opt_list = get_default_opt_list()
    input_tmp = ''
    output_tmp = ''
    extra_cmd = ''
    ext = ''
    thread_num=0
    do_execute=0
    print opts
    print args

    for opt, arg in opts:
        if opt == "-i":
            input_tmp = arg
        elif opt == "-e":
            ext = arg
        elif opt == "-C":
            extra_cmd = arg
        elif opt == "-t":
            thread_num = int(arg)
        elif opt == "-h":
            cmd_line = FFMPEG_BIN + " -h"
            os.system(cmd_line)
        elif opt == "-Y":
            do_execute = 1
        else:
            assert False, "unknown option"

    print "input_tmp=%s" % input_tmp
    if len(input_tmp) == 0:
        usage()
        sys.exit()

    if os.path.isdir(input_tmp):
        print "'%s' is a directory" % input_tmp
        input_file_list = lib.get_file_list(input_tmp)
    elif os.path.isfile(input_tmp):
        print "'%s' is a file" % input_tmp
        input_file_list = []
        input_file_list.append(input_tmp)
    else:  # globbing is needed
        print "'%s' is glob pattern" % input_tmp
        input_file_list = glob.glob(input_tmp)
    # print type(input_file)
    print "input_file_list=%s" % input_file_list
    if len(input_file_list) == 0:  # '':# or ( ext=='' and output_file==''):
        usage()
        sys.exit()

    if len(args) > 0:  # '':
        if len(args) == 1:
            output_tmp = args
        else:
            output_tmp = args[0]
    if len(output_tmp) == 0:  #=='':
        output_tmp = "_out"
    else:
        if not output_tmp.startswith('_'):
            output_tmp = '_' + output_tmp

    prepared_cmd = FFMPEG_BIN
    if thread_num > 0:
        prepared_cmd += " -threads %s" % thread_num

    cmd_list = []
    for input_file in input_file_list:
        print input_file
        if os.path.isfile(input_file):
            print "'%s' is a file"%input_file
            cmd_line=get_cmd_line(input_file,ext,output_tmp,prepared_cmd,extra_cmd)
            print cmd_line
            cmd_list.append(cmd_line)
        elif os.path.isdir(input_file):
            print "'%s' is a directory"%input_file
            input_file_list2=lib.get_file_list(input_file)
            print "input_file_list2=%s"%input_file_list2
            for input_file2 in input_file_list2:
                cmd_line=get_cmd_line(input_file2,ext,output_tmp,prepared_cmd,extra_cmd)
                print cmd_line
                cmd_list.append(cmd_line)

    if do_execute == 1:
        for cmd in cmd_list:
            #os.system(cmd)
            subprocess.call(cmd, stdout=None, stderr=None, shell=True)



