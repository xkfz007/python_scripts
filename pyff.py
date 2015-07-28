#!/bin/python
__author__ = 'hfz2597'
import sys
import getopt
import os
import subprocess


def usage():
  help_msg = '''Usage:pyff.py [option] [value]...
  options:
   -i <string> input file
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

  FFMPEG_BIN = 'ffmpeg.exe'
  input_file = ''
  extra_cmd = ''
  ext = ''
  output_file = ''

  print opts
  print args

  for opt, arg in opts:
    if opt == "-i":
      input_file = arg
    elif opt == "-e":
      ext = arg
    elif opt == "-C":
      extra_cmd = arg
    elif opt == "-h":
      usage()
      sys.exit()
    elif opt == "-h":
      cmd_line = FFMPEG_BIN + " -h"
      os.system(cmd_line)
    else:
      assert False, "unknown option"

  if len(args) > 0:  # '':
    output_file = args

  if len(input_file) == 0:  # '':# or ( ext=='' and output_file==''):
    usage()
    sys.exit()

  print input_file
  print output_file
  path = os.getcwd()
  print os.getcwd()

  if 1:  # os.path.isfile(input_file):
    print input_file
    file_name, file_ext = os.path.splitext(input_file)
    print file_name
    print file_ext
    if len(output_file) == 0:  #=='':
      if len(ext) > 0:  #'':
        if not ext.startswith('.'):
          ext = '.' + ext
        output_file = file_name + ext
      else:
        output_file = file_name + "_out" + file_ext
    cmd_line = FFMPEG_BIN
    #cmd_line+=" -i %s/%s"%(path,input_file)
    cmd_line += " -i %s" % input_file
    cmd_line += " %s" % extra_cmd
    cmd_line += " %s" % output_file
    print cmd_line
    #os.system(cmd_line)
    #subprocess.call(cmd_line, stdout=None, shell=True)



