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

def normalize_path(path):
  path=path.strip()
  path=os.path.normpath(path)
  if os.path.sep=="\\" and path.find("/")>=0:
    path=path.replace("/",os.path.sep)
  elif os.path.sep=="/" and path.find("\\")>=0:
    path=path.replace("\\",os.path.sep)

  return path

def format_path(path):
  #if path==".":
  #  path=os.getcwd()
  #path=os.path.abspath(path)
  #if path[-1]!="/" and path[-1]!="\\":
  #  if path.find("/")>=0:
  #    path+="/"
  #  elif path.find("\\")>=0:
  #    path+="\\"
  path=normalize_path(path)
  if path[-1]!=os.path.sep:
    path+=os.path.sep
  return path

def format_file_path(file_path):
  file_path=normalize_path(file_path)
  sys_str = determin_sys()
  print file_path
  if sys_str == "cygwin" and file_path.find("cygdrive") < 0:
    file_path = "/cygdrive/" + file_path.replace(":", "")
  elif sys_str=="linux" and len(os.path.splitdrive(file_path)[0])>0:
    file_path=os.path.expanduser("~")+os.path.splitdrive(file_path)[1]

  return file_path
