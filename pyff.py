#!/bin/python
__author__ = 'hfz2597'
import sys
import getopt
import os
import subprocess
import glob
import lib


def usage():
  help_msg = '''Usage:pyff.py [option] [value]...
  options:
   -i <string> input file, support pattern globbing
   -e <string> the output file extension
   -C <string> the ffmpeg commands
   '''
  print help_msg
  return


if __name__ == '__main__':
  if len(sys.argv) == 1:
    usage()
    sys.exit()

  try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:e:C:h')
  except getopt.GetoptError as err:
    print str(err)
    sys.exit(2)
  except Exception, e:
    print e

  FFMPEG_BIN = 'ffmpeg.exe -y'
  input_tmp = ''
  extra_cmd = ''
  ext = ''
  output_tmp = ''

  print opts
  print args

  for opt, arg in opts:
    if opt == "-i":
      input_tmp = arg
    elif opt == "-e":
      ext = arg
    elif opt == "-C":
      extra_cmd = arg
    elif opt == "-h":
      cmd_line = FFMPEG_BIN + " -h"
      os.system(cmd_line)
    else:
      assert False, "unknown option"

  print "input_tmp=%s"%input_tmp
  if len(input_tmp)==0:
      usage()
      sys.exit()

  #input_tmp="./%s"%input_tmp

  if os.path.isdir(input_tmp):
      print "'%s' is a directory"%input_tmp
      input_file_list=lib.get_file_list(input_tmp)
  elif os.path.isfile(input_tmp):
      print "'%s' is a file"%input_tmp
      input_file_list=[]
      input_file_list.append(input_tmp)
  else:# globbing is needed
      print "'%s' is glob pattern"%input_tmp
      input_file_list=glob.glob(input_tmp)
  #print type(input_file)
  print "input_file_list=%s"%input_file_list
  if len(input_file_list) == 0:  # '':# or ( ext=='' and output_file==''):
      usage()
      sys.exit()

  if len(args) > 0:  # '':
      if len(args)==1:
          output_tmp = args
      else:
          output_tmp = args[0]

  for input_file in input_file_list:
    print input_file
    fname, fext = os.path.splitext(input_file)
    print fname
    print fext
    if len(ext) > 0:  #'':
        if not ext.startswith('.'):
            ext = '.' + ext
    else:
        ext=fext
    if len(output_tmp) == 0:  #=='':
        output_tmp="_out"
    else:
        if not output_tmp.startswith('_'):
            output_tmp='_'+output_tmp
    output_file = "%s%s%s"%(fname,output_tmp,ext)

    cmd_line = FFMPEG_BIN
    cmd_line += " -i \"%s\"" % input_file
    cmd_line += " %s" % extra_cmd
    cmd_line += " \"%s\"" % output_file
    print cmd_line
    #os.system(cmd_line)
    #subprocess.call(cmd_line, stdout=None, shell=True)



