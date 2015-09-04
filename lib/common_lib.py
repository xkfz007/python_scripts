import platform
import os
import subprocess
import logging


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
    if path.find("cygdrive") >= 0:
        path = path.replace("/cygdrive/", "")
        path = path[0] + ":" + path[1:]
    return path


def normalize_path(path):
    path = path.strip()
    path = os.path.normpath(path)
    if os.path.sep == "\\" and path.find("/") >= 0:
        path = path.replace("/", os.path.sep)
    elif os.path.sep == "/" and path.find("\\") >= 0:
        path = path.replace("\\", os.path.sep)
    path = convert2drivepath(path)

    return path


def format_path(path):
    # if path==".":
    # path=os.getcwd()
    if path == os.curdir or path == os.pardir:  # currend dir(.) or parent dir(..)
        path = os.path.abspath(path)
    # if path[-1]!="/" and path[-1]!="\\":
    #  if path.find("/")>=0:
    #    path+="/"
    #  elif path.find("\\")>=0:
    #    path+="\\"
    path = normalize_path(path)
    if path[-1] != os.path.sep:
        path += os.path.sep
    return path

# def format_file_path(file_path):
# file_path=normalize_path(file_path)
# sys_str = determin_sys()
#  #print file_path
#  if sys_str == "cygwin" and file_path.find("cygdrive") < 0:
#    file_path = "/cygdrive/" + file_path.replace(":", "")
#  elif sys_str=="linux" and len(os.path.splitdrive(file_path)[0])>0:
#    file_path=os.path.expanduser("~")+os.path.splitdrive(file_path)[1]
#
#  return file_path

import sys


def get_file_list(path_dir, ext=''):
    if len(ext) != 0:
        if ext[0] != '.':
            ext = '.' + ext
        if len(ext) == 1:
            print "invaild extension, please check"
            sys.exit()
    path_dir = format_path(path_dir)
    file_list = []
    for root, dirs, files in os.walk(path_dir):
        for i in files:
            if len(ext) != 0:
                t1, t2 = os.path.splitext(i)
                if t2 != ext:
                    continue
            file_list.append(os.path.join(root, i))

    return file_list


def check_path(path):
    path = path.strip()  #delete the blankspace before or after the path
    path = path.strip('\\')
    path = path.strip('/')
    #chech whether the path exists or creat it
    if not os.path.exists(path):
        os.makedirs(path)


def delete_files(path, ext_list):
    path = os.path.normpath(path)
    for root, dirs, files in os.walk(path):
        for fname in files:
            full_name = os.path.join(root, fname)
            ext = os.path.splitext(full_name)[1]
            if ext in ext_list:
                os.remove(full_name)

def run_cmd(cmd_line,log_file='',do_execute=0,rec_cl=1):
   print cmd_line
   if do_execute==0:
       return
   pfile = None
   #if determin_sys() == "cygwin" and rec_cl==1:
   #    cmd_line += " 2>&1 |tee -a %s"% log_file
   if len(log_file)>0:
      pfile = open(log_file, "w")
      if rec_cl==1:
         print >> pfile, "%s" % cmd_line
         if determin_sys() == "cygwin":
           cmd_line += " 2>&1 |tee -a %s"% log_file
           pfile.close()
           pfile=None

   #os.system(cmd_line)
   subprocess.call(cmd_line, shell=True, stdout=pfile, stderr=pfile)


class HELP(object):
    default_opt='hHY'
    def __init__(self,usage,BIN='',help='--help'):
        self.usage=usage
        self.BIN=BIN
        self.help=help
        self.do_execute=0
    def set_BIN(self,BIN):
        self.BIN=BIN
    def set_help(self,help):
        self.help=help
    def set_do_execute(self,do_execute=1):
        self.do_execute=do_execute
    def get_opt(self):
        return HELP.default_opt
    def add_usage(self):
        msg='additional options:\n'
        msg+='   -h print this help\n'
        if len(self.BIN)>0:
           msg+='   -H print help of "%s"\n'%self.BIN
        msg+='   -Y whether to execute the program\n'
        print msg

    def parse_opt(self,opt):
        if opt == '-h':
            self.usage()
            self.add_usage()
            sys.exit()
        elif opt == '-H':
            if len(self.BIN):
               os.system(self.BIN+' '+self.help)
            else:
                logging.error('Executor is not set')
            sys.exit()
        elif opt == '-Y':
         self.set_do_execute()
        else:
            logging.warning('unknown option:%s'%opt)

    def get_do_execute(self):
        return self.do_execute

