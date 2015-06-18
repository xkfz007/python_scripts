#!/bin/python
import re
import subprocess

cmd_line = 'ffmpeg.exe -i f:/QQDownload/test2/a.rmvb'

subprocess.call(cmd_line,stdout=None,shell=True)
p = subprocess.Popen(cmd_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

datalines=[]
#for a in iter(p.stdout.readline, b''):
for a in p.stdout.readlines():
  if a.find('Stream #')>=0 and a.find('Audio:')>=0:
    datalines.append(a)
for a in p.stderr.readlines():
  if a.find('Stream #')>=0 and a.find('Audio:')>=0:
    datalines.append(a)
p.stdout.close()
p.stderr.close()

assert len(datalines)==1
str_list=datalines[0].strip().replace(',',' ').split(' ')
idx=0
for i in str_list:
  if i=="Audio:":
    break
  idx+=1
audio_c=str_list[idx+1]
print datalines
print str_list
print idx
print audio_c
