#!/bin/python
import getopt
import sys
import subprocess
import lib.seq_list
import lib.fun_lib
import os

__author__ = 'hfz2597'

# opts, args = getopt.getopt(sys.argv[1:], 'i:o:s:t:T:hHO:e:yn')
#print opts
#print args
executor = "ffplay.exe "
location = ""
cmd_list = []
for i in sys.argv[1:]:
  name = os.path.basename(i)
  dpath = os.path.dirname(i)
  if location != dpath and dpath != "":
    location = dpath
  if not name.endswith(".yuv"):
    name = lib.seq_list.guess_seqname(name)
    name += ".yuv"
  #reso=name.split('_')[1]
  width, height, fps = lib.fun_lib.get_reso_info(name)
  cmd = executor
  full_path = os.path.join(location, name)
  cmd += " -i %s" % full_path
  cmd += " -f rawvideo"
  cmd += " -video_size %sx%s" % (width, height)
  cmd += " -framerate %s" % fps
  cmd_list.append(cmd)

print cmd_list

for i in cmd_list:
  subprocess.Popen(i, stdout=None, stderr=None, shell=True)



#cmd_line="ffplay.exe -i f:/sequences/Dblowingbubbles_416x240_8_50_500.yuv  -f rawvideo -video_size 416x240"
#subprocess.Popen(cmd_line,stdout=None,stderr=None,shell=True)
#subprocess.Popen(cmd_line,stdout=None,stderr=None,shell=True)
