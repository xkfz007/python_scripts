#!/usr/bin/python
import platform
import os
import sys
import getopt
import subprocess
# abr=[(1,2), (0,3,4), (0.10,0.25,0.33), (1.0,1.1), (1.0,), (0.9,0.8,0.7,0.6,0.3)]
# length=len(abr)
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


# print platform.architecture()
# print platform.platform()
# print platform.system()
# print platform.python_version()
# print platform.uname()
# print sys.platform
# #os.system("pause")
# str = "cygwin\\"
# print str
# a = str.replace(":", "")
# print str
# print a
#
# print sys.argv
#
# str = "hello"
# print str
# str += "world"
# print str
#
#
# def update_str(str, str2):
#     str += str2
#     return str
#
#
# print update_str(str, "OK")
#
# a = "-12.7"
# print a
# b = float(a)
# print b
#
# #tmp_dict={'a':1,'b':2,'c':3}
# #if tmp_dict.has_key('d') and tmp_dict['d']==4:
# #  print 'OK'
# #elif tmp_dict['d']==4:
# #  print 'invalid'
# #else:
# #  print 'BAD'
# #
#
# #def get_total_frame_num(filename,width,height):
# #  size=os.path.getsize(filename)
# #  filesize=width*height*3/2
# #  num_frames=size/filesize
# #  return num_frames
# #
# #print "num_frames=%s" % get_total_frame_num("e:/sequences/navyflight_1920x1080_30_2973.yuv",1920,1080)
# #
# #a=100
# #for a in range(10):
# #  print a
# #
# #print a
# #
# #path="c:/aa/kk"
# #for i in [ "  c://a//kk","c:\\dfa\\asf\\   ","c://adfa\\adsf   \\","c:/fasdf\\fasdf/  "]:
# #  print "%s@@@@%s"%(i,os.path.normpath(i))
# #
# #path="c:/aa/kkk"
# #path=os.path.normpath(path)
# #filename="a.txt"
# #fullname=os.path.join(path,filename)
# #print fullname
#
#
# #path="F:\\tmp"
# #for root,dirs,files in os.walk(path):
# #  #print "[root=%s dirs=%s files=%s]"%(root,dirs,files)
# #  for i in files:
# #    print "FILE=%s"%os.path.join(root,i)
#
# #import lib.fun_lib
# #seq_name=( 'Apeopleonstreet_2560x1600_8_30_150','Atraffic_2560x1600_8_30_150','Bbasketballdrive_1920x1080_8_50_500',
# #'Bbqterrace_1920x1080_8_60_600','Bcactus_1920x1080_8_50_500','Bkimono_1920x1080_8_24_240','RaceHorses_416x240_30',
# #'RaceHorses_832x480_30','SlideEditing_1280x720_30','SlideShow_1280x720_20','Tennis_1920x1080_24',
# #'Traffic_2560x1600_30_crop','vidyo1_1280x720_60','vidyo3_1280x720_60','vidyo4_1280x720_60','walk_640x480_30',
# #'xtslf_1920x1080_25_1854',  )
# #for i in seq_name:
# #  width,height,fps=lib.fun_lib.get_reso_info(i)
# #  print "%s:%d %d %d"%(i,width,height,fps)
#
# #import subprocess
# #p=subprocess.Popen('ls')
# #print p.stdout
#
# path = "F:\\encoder_test_output\\x265_output"
# #print os.path.abspath(path)
# print os.path.normpath(path)
# #print os.path.normpath(os.path.abspath(path))
# #print os.path.relpath(".")
# #print os.path.splitdrive(path)
# print os.sep
# #
# #dictString = "{'Define1':[[63.3,0.00,0.5,0.3,0.0],[269.3,0.034,1.0,1.0,0.5],[332.2,0.933,0.2,0.99920654296875,1],[935.0,0.990,0.2,0.1,1.0]],'Define2':[[63.3,0.00,0.5,0.2,1.0],[269.3,0.034,1.0,0.3,0.5],[332.2,0.933,0.2, 0.4,0.6],[935.0,0.990,1.0, 0.5,0.0]],}"
# #dict = eval(dictString)
# #print "keys:", dict.keys()
# #print "Define1 value ", dict['Define1']
#
# print os.getcwd()
# print os.curdir
# print os.pardir
# print os.path.abspath('\\\\172.21.40.64\\h265\\xml')
#
# import lib
#
# a = lib.get_total_frame_num("f:/sequences/kldby_1920x1080_25.yuv", 200, 200)
# print a
# print __file__
# print os.path.realpath(__file__)

#def str_func(str,i):
#    str+="test%s"%i
#    print str

#str="good"
#for i in range(5):
#    str_func(str,i)


def parse_arg(arg,delimiter,*LS):
    cnt=arg.count(delimiter)
    N=cnt+1
    print 'cnt=%s'%cnt
    #assert n==len(LS)
    olst=list(LS)
    print olst
    lst=arg.split(delimiter)
    print 'lst=%s'%lst
    for i in range(0,N):
       print lst[i]
       if len(lst[i])>0:
           olst[i]=lst[i]
       
    return olst


#x,y,z,w=parse_arg('500::2:1',':',0,0,0,0)
#print x,y,z,w

#opt=raw_input('Directory "a" does not exist, do you want to create it?(Y/N)')
#print opt


import json
class entry:
    def __init__(self,index,time,frame):
        self.index=index
        self.time=time
        self.frame=frame

data={"filename":"video1.mp4",
      "blackframe":[],
      "staticframe":[],
      "mosaic":[]
}
s = json.dumps(data,indent=4)
print s
a=data["blackframe"]
a.append(entry(1,"ddddd","200"))
s = json.dumps(data,indent=4)

print s


