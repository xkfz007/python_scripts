#!/bin/python
import sys
import getopt
import os
import subprocess
import lib.common_lib


def usage():
  help_msg = '''Usage:./test.py [option] [value]...
  options:
   -i <string> input_path
   -o <string> output_path
   -s 00:00:00 start time offset
   -t 00:00:00 duration
   -h show this help
   -H show the ffmpeg help
   -O 0: cut video
      1: get audio from video
   '''
  print help_msg
  return

def get_default_opts():
  opt_list={}
  opt_list['ffmpeg.exe']='ffmpeg.exe'
  opt_list['input_file']='a.mp4'
  opt_list['output_file']=''
  opt_list['start_time']='00:00:00'
  opt_list['duration']='00:10:00'
  opt_list['help']=0
  opt_list['operation']=-1
  return opt_list

def parse_cl(opt_list):
  if len(sys.argv) == 1:
    usage()
    sys.exit()

  try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:o:s:t:hHO:')
  except getopt.GetoptError as err:
    print str(err)
    sys.exit(2)
  except Exception, e:
    print e

  for opt, arg in opts:
    if opt == "-i":
      opt_list["input_file"] = arg
    elif opt == "-o":
      opt_list["output_file"] = arg
    elif opt == "-s":
      opt_list["start_time"] = arg
    elif opt == "-t":
      opt_list["duration"] = arg
    elif opt == "-O":
      opt_list["operation"] = int(arg)
    elif opt == "-h":
      usage()
      sys.exit()
    elif opt == "-H":
      opt_list['help']=1
    else:
      assert False, "unknown option"

def get_cmd_line(opt_list):
  cmd_line=""
  cmd_line += " -ss %s" % opt_list['start_time']
  cmd_line += " -t %s" % opt_list['duration']
  if opt_list['operation']==0:#video cut
    if opt_list['output_file']=='':
      file_name,ext=os.path.splitext(opt_list['input_file'])
      opt_list['output_file']=file_name+"_out"+ext
    cmd_line += " -i %s -vcodec copy -acodec copy" % opt_list['input_file']
    cmd_line += " %s" % opt_list['output_file']
  elif opt_list['operation']==1:#get audio from video
    if opt_list['output_file']=='':
      file_name,ext=os.path.splitext(opt_list['input_file'])
      opt_list['output_file']=file_name+"_audio"+ext
    cmd_line += " -i %s -acodec copy" % opt_list['input_file']
    #cmd_line += " -i %s -acodec libmp3lame" % opt_list['input_file']
    cmd_line += " -vn"#disable video output
    cmd_line += " %s" % opt_list['output_file']

  return cmd_line

def get_file_list(path_dir):
  path_dir=lib.common_lib.format_path(path_dir)
  file_list=[]
  for root,dirs,files in os.walk(path_dir):
    for i in files:
      file_list.append(os.path.join(root,i))

  return file_list

if __name__=='__main__':
  opt_list=get_default_opts()
  #opt_list['ffmpeg.exe']='d:/tools/ffmpeg.exe'
  parse_cl(opt_list)
  #cmd_line=""
  cmd_line="%s"%opt_list['ffmpeg.exe']
  if opt_list['help']==1 or opt_list['operation']<0:
    cmd_line+=" -h long"
    os.system(cmd_line)
  else:
    if os.path.isfile(opt_list['input_file']):
      cmd_line+=get_cmd_line(opt_list)
      subprocess.call(cmd_line, stdout=None, shell=True)
    elif os.path.isdir(opt_list['input_file']):
      file_list=get_file_list(opt_list['input_file'])
      cmd_list=[]
      for i in file_list:
        cmd_tmp=cmd_line
        opt_list['input_file']=i
        opt_list['output_file']=''
        cmd_tmp+=get_cmd_line(opt_list)
        subprocess.call(cmd_tmp, stdout=None, shell=True)



