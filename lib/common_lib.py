import platform
import os


def determin_sys():
  sysinfo = platform.system()
  sysinfo = sysinfo.upper()
  if sysinfo.find("WINDOWS") >= 0:
    str = "windows"
  elif sysinfo.find("LINUX") >= 0:
    str = "linux"
  elif sysinfo.find("CYGWIN") >= 0:
    str = "cygwin"
  else:
    str = "unknown"

  return str

def convert2drivepath(path):
  if path.find("cygdrive")>=0:
    path=path.replace("/cygdrive/","")
    path=path[0]+":"+path[1:]
  return path

def normalize_path(path):
  path=path.strip()
  path=os.path.normpath(path)
  if os.path.sep=="\\" and path.find("/")>=0:
    path=path.replace("/",os.path.sep)
  elif os.path.sep=="/" and path.find("\\")>=0:
    path=path.replace("\\",os.path.sep)
  path=convert2drivepath(path)

  return path


def format_path(path):
  #if path==".":
  #  path=os.getcwd()
  if path==os.curdir or path==os.pardir:# currend dir(.) or parent dir(..)
    path=os.path.abspath(path)
  #if path[-1]!="/" and path[-1]!="\\":
  #  if path.find("/")>=0:
  #    path+="/"
  #  elif path.find("\\")>=0:
  #    path+="\\"
  path=normalize_path(path)
  if path[-1]!=os.path.sep:
    path+=os.path.sep
  return path

#def format_file_path(file_path):
#  file_path=normalize_path(file_path)
#  sys_str = determin_sys()
#  #print file_path
#  if sys_str == "cygwin" and file_path.find("cygdrive") < 0:
#    file_path = "/cygdrive/" + file_path.replace(":", "")
#  elif sys_str=="linux" and len(os.path.splitdrive(file_path)[0])>0:
#    file_path=os.path.expanduser("~")+os.path.splitdrive(file_path)[1]
#
#  return file_path

import sys
def get_file_list(path_dir,ext=''):
  if len(ext)!=0:
    if ext[0]!='.':
      ext='.'+ext
    if len(ext)==1:
      print "invaild extension, please check"
      sys.exit()
  path_dir=format_path(path_dir)
  file_list=[]
  for root,dirs,files in os.walk(path_dir):
    for i in files:
      if len(ext)!=0:
        t1,t2=os.path.splitext(i)
        if t2!=ext:
          continue
      file_list.append(os.path.join(root,i))

  return file_list

def check_path(path):
    path=path.strip()#delete the blankspace before or after the path
    path=path.strip('\\')
    path=path.strip('/')
    #chech whether the path exists or creat it
    if not os.path.exists(path):
      os.makedirs(path)


def delete_files(path,ext_list):
  path=os.path.normpath(path)
  for root,dirs,files in os.walk(path):
    for fname in files:
      full_name=os.path.join(root,fname)
      ext=os.path.splitext(full_name)[1]
      if ext in ext_list:
        os.remove(full_name)
