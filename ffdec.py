#!/bin/python
__author__ = 'hfz2597'

import sys
import getopt
import os
import subprocess


def usage():
  help_msg = '''Usage:ffdec.py [option] [value]...
  options:
   -d decode to get reconstructed yuv

   '''
  print help_msg
  return


if __name__ == '__main__':
  if len(sys.argv) == 1:
    usage()
    sys.exit()

  try:
    opts, args = getopt.gnu_getopt(sys.argv[1:], ':dh')
  except getopt.GetoptError as err:
    print str(err)
    sys.exit(2)
  except Exception, e:
    print e

  FFMPEG_BIN = 'ffmpeg.exe'
  input_file = ''
  # extra_cmd=''
  #ext=''
  output_file = ''
  dec_flag = 0

  for opt, arg in opts:
    if opt == "-d":
      dec_flag = 1
    elif opt == "-h":
      cmd_line = FFMPEG_BIN + " -h"
      os.system(cmd_line)
    else:
      assert False, "unknown option"

  if len(args) == 0:  #'':
    usage()
    sys.exit()

  input_file = args[0]

  if len(args) > 1:
    output_file = args[1]
  if len(output_file) == 0:
    file_name, file_ext = os.path.splitext(input_file)
    if dec_flag == 0:
      output_file = file_name + ".bin"
    else:
      output_file = file_name + ".yuv"

  cmd = FFMPEG_BIN
  cmd += " -y -i %s" % input_file
  cmd += " -an "
  if dec_flag == 0:
    cmd += " -c:v copy"
  cmd += " -f rawvideo"
  cmd += " %s" % output_file

  print cmd
  os.system(cmd)

