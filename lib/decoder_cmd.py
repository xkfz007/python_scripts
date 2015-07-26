#!/bin/python
__author__ = 'hfz2597'
import sys
import getopt
import os
import common_lib

def get_dec_param_cmd_ashevc(param_list):
  cmd = ""
  cmd += ' -i "%s"'%param_list['input_filename']
  if len(param_list['output_filename'])>0:
    cmd += ' -o "%s"'%param_list['output_filename']
  return cmd
def get_dec_param_cmd_jm(param_list):
  cmd = ""
  cmd += " -d null"
  cmd += " -p silent=0"
  cmd += ' -i "%s"'%param_list['input_filename']
  #if len(param_list['output_filename'])>0:
  cmd += ' -o "%s"'%param_list['output_filename']
  return cmd
def get_dec_param_cmd_hm(param_list):
  cmd = ""
  cmd += ' -b "%s"'%param_list['input_filename']
  if len(param_list['output_filename'])>0:
    cmd += ' -o "%s"'%param_list['output_filename']
  return cmd

avc_extension=(".264",".avc")
hevc_extension=(".265",".hevc")
class Decoder_prop:
  id=''
  exe=''
  help_exe=''
  version_exe=''
  get_param_cmd=""
  __executors={'ashevc':'ashevcd.exe',
               'jm':'jmd18.5.exe',
               #'jm':'ldecod.exe',
               #'hm': 'hmd14.0.exe',
               'hm': 'hmd.exe',
               }
  __helps={'ashevc': '',
           'jm': '-h',
           'hm':'--help',
           }
  __versions={'ashevc':'',
              'jm':'-V',
              'hm':'--version',
              }
  __cmd_func_list={
    "ashevc": get_dec_param_cmd_ashevc,
    "hm": get_dec_param_cmd_hm,
    "jm": get_dec_param_cmd_jm,
    }
  __common_path = 'c:/tools/'
  __paths={'ashevc':os.path.join(__common_path ),
           'hm':os.path.join(__common_path ),
           'jm':os.path.join(__common_path ),
           }

  def __set_encoder_prop(self):
    Decoder_prop.__paths[self.id]=common_lib.format_path(Decoder_prop.__paths[self.id])
    exe_str=os.path.join(Decoder_prop.__paths[self.id],Decoder_prop.__executors[self.id])
    self.exe=common_lib.normalize_path(exe_str)
    self.help_exe= self.exe + " "+Decoder_prop.__helps[self.id]
    self.version_exe=self.exe+" "+Decoder_prop.__versions[self.id]
    self.get_param_cmd=Decoder_prop.__cmd_func_list[self.id]

  def __set_id(self,id):
    self.id=id


  def __init__(self, id="ashevc"):
    self.__set_id(id)
    self.__set_encoder_prop()


  def set_encoder_id(self,id):
    self.__set_id(id)
    self.__set_encoder_prop()

  def set_encoder_path(self,path):
    Decoder_prop.__paths[self.id]=path
    self.__set_encoder_prop()

  @staticmethod
  def SET_PATH(id,path):
    Decoder_prop.__paths[id]=path


def get_default_dec_param_list():
  param_list = {}#dict()  # create a dictinary
  param_list['input_filename']=''
  param_list['output_filename']=''
  #param_list['cons_filename']='cons.log'
  return param_list

def usage():
  help_msg = '''Usage:./test.py [option] [value] ...
  options:
   -e <string> encoder name:ashevc,hm,jm
   -i <string> input file name
   -o output the reconstruct file
   -h print this help
   -H print the decoder help
   -V print the decoder version info
   '''
  print help_msg
  return

def parse_dec_cl(dec,opt_list):
  if len(sys.argv) == 1:
    usage()
    sys.exit()

  try:
    opts, args = getopt.getopt(sys.argv[1:], 'e:i:hHV')
  except getopt.GetoptError as err:
    print str(err)
    sys.exit(2)
  except Exception, e:
    print e

  Help_flag=0
  Version_flag=0
  Output_flag=0

  for opt, arg in opts:
    if opt == "-i":
      opt_list["input_filename"] = arg
    elif opt == "-o":
      Output_flag=1
      #opt_list["output_filename"] = arg
    elif opt == "-h":
      usage()
      sys.exit()
    elif opt == "-H":
      Help_flag=1
    elif opt == "-e":
      dec.set_encoder_id(arg.strip())
    elif opt == "-v":
      Version_flag=1
    else:
      assert False, "unknown option"


  if Help_flag==1:
    os.system(dec.help_exe)
    sys.exit()

  if Version_flag==1:
    os.system(dec.version_exe)
    sys.exit()

  if len(opt_list['input_filename'])==0:
    print "input isn't set"
    sys.exit()

  if len(args)>0:
    opt_list['output_filename']=args[0]

  dir_path,filename=os.path.split(opt_list['input_filename'])
  name,ext=os.path.splitext(filename)
  if ext in (".264") and dec.id not in ("jm"):
    dec.set_encoder_id("jm")
  if ext in (".265","hevc") and dec.id not in ("ashevc","hm"):
    dec.set_encoder_id("hm")

  cons_filename=name+"_"+dec.id+"_cons.log"
  cons_full=os.path.join(dir_path,cons_filename)
  if Output_flag==1 and len(opt_list['output_filename'])==0:
    output_filename=name+"_rec.yuv"
    opt_list['output_filename']=os.path.join(dir_path,output_filename)

  return cons_full

#def configure_dec_param(dec,param_list):
#  cons_log=parse_dec_cl(dec,param_list)
#  return (cons_log,tmp_list['extra_cls'])
