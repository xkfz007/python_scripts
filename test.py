#!/usr/bin/python
import platform
import os
import sys
import getopt
#abr=[(1,2), (0,3,4), (0.10,0.25,0.33), (1.0,1.1), (1.0,), (0.9,0.8,0.7,0.6,0.3)]
#length=len(abr)
#print abr
#print length
#num=1
#len_list=[]
#idx_list=[]
#for i in range(0,length):
#  length=len(abr[i])
#  len_list.append(length)
#  idx_list.append(0)
#  num*=len(abr[i])
#  print "len=%s,num=%s" % (length,num)
#print num
#print len_list
#print idx_list


print platform.architecture()
print platform.platform()
print platform.system()
print platform.python_version()
print platform.uname()
print sys.platform
#os.system("pause")
str="cygwin\\"
print str
a=str.replace(":","")
print str
print a

print sys.argv

str="hello"
print str
str+="world"
print str

def update_str(str,str2):
  str+=str2
  return str

print update_str(str,"OK")

a="-12.7"
print a
b=float(a)
print b

#tmp_dict={'a':1,'b':2,'c':3}
#if tmp_dict.has_key('d') and tmp_dict['d']==4:
#  print 'OK'
#elif tmp_dict['d']==4:
#  print 'invalid'
#else:
#  print 'BAD'
#

#def get_total_frame_num(filename,width,height):
#  size=os.path.getsize(filename)
#  filesize=width*height*3/2
#  num_frames=size/filesize
#  return num_frames
#
#print "num_frames=%s" % get_total_frame_num("e:/sequences/navyflight_1920x1080_30_2973.yuv",1920,1080)
#
#a=100
#for a in range(10):
#  print a
#
#print a
#
#path="c:/aa/kk"
#for i in [ "  c://a//kk","c:\\dfa\\asf\\   ","c://adfa\\adsf   \\","c:/fasdf\\fasdf/  "]:
#  print "%s@@@@%s"%(i,os.path.normpath(i))
#
#path="c:/aa/kkk"
#path=os.path.normpath(path)
#filename="a.txt"
#fullname=os.path.join(path,filename)
#print fullname


#path="F:\\tmp"
#for root,dirs,files in os.walk(path):
#  #print "[root=%s dirs=%s files=%s]"%(root,dirs,files)
#  for i in files:
#    print "FILE=%s"%os.path.join(root,i)

#import lib.fun_lib
#seq_name=( 'Apeopleonstreet_2560x1600_8_30_150','Atraffic_2560x1600_8_30_150','Bbasketballdrive_1920x1080_8_50_500',
#'Bbqterrace_1920x1080_8_60_600','Bcactus_1920x1080_8_50_500','Bkimono_1920x1080_8_24_240','RaceHorses_416x240_30',
#'RaceHorses_832x480_30','SlideEditing_1280x720_30','SlideShow_1280x720_20','Tennis_1920x1080_24',
#'Traffic_2560x1600_30_crop','vidyo1_1280x720_60','vidyo3_1280x720_60','vidyo4_1280x720_60','walk_640x480_30',
#'xtslf_1920x1080_25_1854',  )
#for i in seq_name:
#  width,height,fps=lib.fun_lib.get_reso_info(i)
#  print "%s:%d %d %d"%(i,width,height,fps)

#import subprocess
#p=subprocess.Popen('ls')
#print p.stdout

path="F:\\encoder_test_output\\x265_output"
print os.path.abspath(path)
print os.path.normpath(path)
print os.path.normpath(os.path.abspath(path))
print os.path.relpath(".")
print os.path.splitdrive(path)
