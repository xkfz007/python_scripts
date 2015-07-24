#!/bin/python
import getopt
import sys
import subprocess
import lib.seq_list
import lib.fun_lib
import os
__author__ = 'hfz2597'

#opts, args = getopt.getopt(sys.argv[1:], 'i:o:s:t:T:hHO:e:yn')
#print opts
#print args
executor="ffplay.exe "
location=""
cmd_list=[]
for i in sys.argv[1:]:
  cmd=executor
  cmd+=" -hide_banner -i %s -an -loop 0"%i
  cmd_list.append(cmd)

print cmd_list

for i in cmd_list:
  subprocess.Popen(i,stdout=None,stderr=None,shell=True)



#cmd_line="ffplay.exe -i f:/sequences/Dblowingbubbles_416x240_8_50_500.yuv  -f rawvideo -video_size 416x240"
#subprocess.Popen(cmd_line,stdout=None,stderr=None,shell=True)
#subprocess.Popen(cmd_line,stdout=None,stderr=None,shell=True)
