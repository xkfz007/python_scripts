#!/bin/python
__author__ = 'hfz2597'
import lib
import os
import subprocess
def get_file_list(path_dir):
  path_dir=lib.common_lib.format_path(path_dir)
  file_list=[]
  for root,dirs,files in os.walk(path_dir):
    for i in files:
      file_list.append(os.path.join(root,i))

  return file_list

if __name__=="__main__":
  dirt="f:/QQDownload/The.Wire"
  file_list=get_file_list(dirt)
  cmd_line="ffmpeg.exe "
  for i in file_list:
    file_size=os.path.getsize(i)
    basename=os.path.basename(i)
    file_name,ext=os.path.splitext(basename)
    output_name=file_name+"_small"+ext
    output_full_name=os.path.join(dirt,output_name)
    #%print "%s:%sB=%sKB=%sMB"%(i,file_size,file_size/1024,file_size/1024/1024)
    cmd_tmp=cmd_line
    cmd_tmp+=" -i %s"%i
    cmd_tmp+=" -y -fs %sM"%(file_size/1024/1024/4)
    cmd_tmp+=" %s"%output_full_name
    print cmd_tmp
    subprocess.call(cmd_tmp, stdout=None, shell=True)
