#!/bin/python
__author__ = 'hfz2597'

import sys
import getopt
import os
import subprocess

h264_name_list=('h264','h.264','avc','264')
h265_name_list=('h265','h.265','hevc','265')

bsf_for_mp4={'h264':'h264_mp4toannexb',
             'hevc':'hevc_mp4toannexb'}


def usage():
  help_msg = '''Usage:ffdec.py [option] <input> [output]
  options:
   -d decode to get reconstructed yuv
   -f format, default h264

   '''
  print help_msg
  return


if __name__ == '__main__':
  if len(sys.argv) == 1:
    usage()
    sys.exit()

  try:
    opts, args = getopt.gnu_getopt(sys.argv[1:], ':df:h')
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
  fmt='hevc'

  for opt, arg in opts:
    if opt == "-d":
      dec_flag = 1
    elif opt == "-h":
      cmd_line = FFMPEG_BIN + " -h"
      os.system(cmd_line)
    elif opt == "-f":
      fmt=arg
    else:
      assert False, "unknown option"

  if len(args) == 0:  #'':
    usage()
    sys.exit()
  if len(fmt)==0:
    print "please give the format of media file"
    usage()
    sys.exit()

  if fmt.lower() in h264_name_list:
    fmt='h264'
  elif fmt.lower() in h265_name_list:
    fmt='hevc'

  input_file = args[0]
  file_name, file_ext = os.path.splitext(input_file)

  if len(args) > 1:
    output_file = args[1]
  if len(output_file) == 0:
    if dec_flag == 0:
      output_file = file_name + "."+fmt
    else:
      output_file = file_name + ".yuv"

  cmd = FFMPEG_BIN
  cmd += " -y -i %s" % input_file
  cmd += " -an "
  if dec_flag == 0:
    cmd += " -c:v copy"
    if file_ext in (".mp4",".MP4"):
      cmd+=" -bsf %s"%bsf_for_mp4[fmt]
    cmd += " -f %s"%fmt
  else:
    cmd += " -f rawvideo"
  cmd += " %s" % output_file

  print cmd
  os.system(cmd)

