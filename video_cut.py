#!/bin/python
import sys
import getopt
import os
import subprocess
import lib.common_lib
import re

class codec_t:
  name=''
  ext=''
  codec=''
  def __init__(self,name,ext,codec):
    self.name=name
    self.ext=ext
    self.codec=codec

audio_codecs={'mp3':codec_t('mp3','.mp3','libmp3lame'),
              'aac':codec_t('aac','.aac','libvo_aacenc'),
              'vorbis':codec_t('vorbis','.ogg','libvorbis')
              }

def get_audio_codec(opt_list):
  cmd_line = "%s" % opt_list['ffmpeg.exe']
  cmd_line += " -i %s " % opt_list['input_file']
  p = subprocess.Popen(cmd_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
  p.wait()
  datalines = []
  for a in p.stdout.readlines():
    if a.find('Stream #') >= 0 and a.find('Audio:') >= 0:
      datalines.append(a)
  for a in p.stderr.readlines():
    #print a
    if a.find('Stream #') >= 0 and a.find('Audio:') >= 0:
      datalines.append(a)
  p.stdout.close()
  p.stderr.close()

  assert len(datalines) == 1
  str_list = datalines[0].strip().replace(',', ' ').split(' ')
  idx = 0
  for i in str_list:
    if i == "Audio:":
      break
    idx += 1
  audio_c = str_list[idx + 1].lower()
  return audio_c

def usage():
  help_msg = '''Usage:./test.py [option] [value]...
  options:
   -i <string> input_path
   -o <string> output_path
   -s 00:00:00 start time offset
   -t <int>or<hh:mm:ss> duration be a number in seconds, or in hh:mm:ss[.xxx] form.
   -T <int>or<hh:mm:ss> duration be a number in seconds, or in hh:mm:ss[.xxx] form.
   -h show this help
   -H show the ffmpeg help
   -O 0: cut video
      1: get audio from video
   -y overwrite the exist files
   -n do not overwrite the exist files

   '''
  print help_msg
  return

def get_default_opts():
  opt_list={}
  opt_list['ffmpeg.exe']='ffmpeg.exe'
  opt_list['input_file']='a.mp4'
  opt_list['output_file']=''
  opt_list['start_time']='-1'
  opt_list['duration']='-1'
  opt_list['position']='-1'
  opt_list['help']=0
  opt_list['operation']=-1
  opt_list['overwrite']='u'
  return opt_list

def parse_cl(opt_list):
  if len(sys.argv) == 1:
    usage()
    sys.exit()

  try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:o:s:t:T:hHO:yn')
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
    elif opt == "-T":
      opt_list["position"] = arg
    elif opt == "-O":
      opt_list["operation"] = int(arg)
    elif opt == "-y":
      opt_list["overwrite"] = 'y'
    elif opt == "-n":
      opt_list["overwrite"] = 'n'
    elif opt == "-h":
      usage()
      sys.exit()
    elif opt == "-H":
      opt_list['help']=1
    else:
      assert False, "unknown option"

def get_cmd_line(opt_list):
  cmd_line=""
  if opt_list['start_time']!='-1':
    cmd_line += " -ss %s" % opt_list['start_time']
  if opt_list['duration']!='-1':
    cmd_line += " -t %s" % opt_list['duration']
  if opt_list['duration']=='-1' and opt_list['position']!='-1':
    cmd_line += " -T %s" % opt_list['position']

  if opt_list['operation']==0:#video cut
    if opt_list['output_file']=='':
      file_name,ext=os.path.splitext(opt_list['input_file'])
      opt_list['output_file']=file_name+"_out"+ext
    cmd_line += " -i %s -vcodec copy -acodec copy" % opt_list['input_file']
    cmd_line += " %s" % opt_list['output_file']
  elif opt_list['operation']==1:#get audio from video
    if opt_list['output_file']=='':
      file_name,ext=os.path.splitext(opt_list['input_file'])
      ac=get_audio_codec(opt_list)
      ext=audio_codecs[ac].ext
      opt_list['output_file']=file_name+"_audio"+ext
    cmd_line += " -i %s" % opt_list['input_file']
    cmd_line += " -vn"#disable video output
    cmd_line += " -acodec copy"
    #cmd_line += " -acodec %s"% audio_codecs[ac].codec
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
    if opt_list['overwrite']=='y' or opt_list['overwrite']=='n':
      cmd_line+=" -%s "%opt_list['overwrite']
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



