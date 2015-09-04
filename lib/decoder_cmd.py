#!/bin/python
__author__ = 'hfz2597'
import sys
import getopt
import os
import common_lib
import global_vars
import codec_cmd
import copy

def get_dec_param_cmd_ashevcd(param_list):
    cmd = ""
    cmd += ' -i "%s"' % param_list['input_filename']
    if len(param_list['output_filename']) > 0:
        cmd += ' -o "%s"' % param_list['output_filename']
    return cmd


def get_dec_param_cmd_jmd(param_list):
    cmd = ""
    cmd += " -d null"
    cmd += " -p silent=0"
    cmd += ' -i "%s"' % param_list['input_filename']
    # if len(param_list['output_filename'])>0:
    cmd += ' -o "%s"' % param_list['output_filename']
    return cmd


def get_dec_param_cmd_hmd(param_list):
    cmd = ""
    cmd += ' -b "%s"' % param_list['input_filename']
    if len(param_list['output_filename']) > 0:
        cmd += ' -o "%s"' % param_list['output_filename']
    return cmd

#class Decoder_st:
#    #executor=''
#    #help=''
#    #version=''
#    #cmd_func=''
#    #path=''
#    def __init(self):
#        exe_str=os.path.join(self.path,self.executor)
#        self.exe = common_lib.normalize_path(exe_str)
#        self.help_exe = self.exe + " " + self.help
#        self.version_exe = self.exe + " " + self.version
#    def __init__(self,id,executor,help,version,cmd_func,path):
#        self.id=id
#        self.executor=executor
#        self.help=help
#        self.version=version
#        self.get_param_cmd=cmd_func
#        self.path=common_lib.format_path(path)
#        self.__init()
#    def set_executor(self,executor):
#        self.executor=executor
#        self.__init()
#    def set_path(self,path):
#        self.path=common_lib.format_path(path)
#        self.__init()
#    def __str__(self):
#        return "decoder_st[id=%s,executor=%s,help=%s,version=%s,path=%s,get_para_cmd=%s]"%\
#              (self.id,self.executor,self.help,self.version,self.path,self.get_param_cmd)
class Decoder_st(codec_cmd.Codec_st):
    def __init__(self,id,executor,help,cmd_func,path):
        #codec_cmd.Codec_st.__init__(self,id,executor,help,version,cmd_func,path)
        super(Decoder_st,self).__init__(id,executor,help,cmd_func,path)
    def __str__(self):
        return "Decoder_st[id=%s,executor=%s,help=%s,path=%s,get_para_cmd=%s]"% \
               (self.id,self.executor,self.help,self.path,self.get_param_cmd)

common_path = 'c:/tools/'
ashevcd_st=Decoder_st(global_vars.ashevcd_name_list[0],'ashevcd.exe','',get_dec_param_cmd_ashevcd,common_path)
jmd_st=Decoder_st(global_vars.jmd_name_list[0],'jmd18.5.exe','-h',get_dec_param_cmd_jmd,common_path)
hmd_st=Decoder_st(global_vars.hmd_name_list[0],'hmd.exe','--help',get_dec_param_cmd_hmd,common_path)

dec_st_list={global_vars.ashevcd_name_list[0]:ashevcd_st,
             global_vars.jmd_name_list[0]:jmd_st,
             global_vars.hmd_name_list[0]:hmd_st,
             }
#dec_st_id_list={key:value for key }

def get_dec_st(id):
    if id in global_vars.ashevcd_name_list:
        id = global_vars.ashevcd_name_list[0]
    elif id in global_vars.hmd_name_list:
        id = global_vars.hmd_name_list[0]
    elif id in global_vars.jmd_name_list:
        id = global_vars.jmd_name_list[0]
    else:
        id = 'ashevcd'
    return dec_st_list[id]

#class DECODER:
#    def __init__(self,id):
#        self.dec_st=get_dec_st(id)
#    def set_id(self,id):
#        self.dec_st=get_dec_st(id)
#    def set_path(self,path):
#        self.dec_st.set_path(path)
#    def set_executor(self,executor):
#        self.dec_st.set_executor(executor)
#    def get_id(self):
#        return self.dec_st.id
#    def get_exe(self):
#        return self.dec_st.exe
#    def get_help_exe(self):
#        return self.dec_st.help_exe
#    def get_version_exe(self):
#        return self.dec_st.version_exe
#    def get_param_cmd(self):
#        return self.dec_st.get_param_cmd
#    def __str__(self):
#        return "DECODER:%s"%self.dec_st
class DECODER(codec_cmd.CODEC):
    def __init__(self,id='hmd'):
        #codec_cmd.CODEC.__init__(self,get_dec_st)
        super(DECODER,self).__init__(get_dec_st)
        #codec_cmd.CODEC.set_id(self,id)
        self.set_id(id)
    def __str__(self):
        return "DECODER:%s"%self.cdec_st
    @staticmethod
    def SET_PATH(id,path):
        get_dec_st(id).set_path(path)
    @staticmethod
    def SET_EXECUTOR(id,executor):
        get_dec_st(id).set_executor(executor)


#class Decoder_prop:
#    #id = 'hm'
#    #exe = ''
#    #help_exe = ''
#    #version_exe = ''
#    #get_param_cmd = ""
#    #dec_st=dec_st_list[id]
#    #dec_executors = {'ashevcd': 'ashevcd.exe',
#    #               'jmd': 'jmd18.5.exe',
#    #               'hmd': 'hmd.exe',
#    #}
#    #dec_helps = {'ashevcd': '',
#    #           'jmd': '-h',
#    #           'hmd': '--help',
#    #}
#    #dec_versions = {'ashevcd': '',
#    #              'jmd': '-V',
#    #              'hmd': '--version',
#    #}
#    #dec_cmd_func_list = {
#    #    "ashevcd": get_dec_param_cmd_ashevcd,
#    #    "hmd": get_dec_param_cmd_hmd,
#    #    "jmd": get_dec_param_cmd_jmd,
#    #}
#    #__common_path = 'c:/tools/'
#    #dec_paths = {'ashevcd': os.path.join(__common_path),
#    #           'hmd': os.path.join(__common_path),
#    #           'jmd': os.path.join(__common_path),
#    #}
#
#    def __set_encoder_prop(self):
#        #Decoder_prop.dec_paths[self.id] = common_lib.format_path(Decoder_prop.dec_paths[self.id])
#        #exe_str = os.path.join(Decoder_prop.dec_paths[self.id], Decoder_prop.dec_executors[self.id])
#        exe_str=os.path.join(self.dec_st.path,self.dec_st.executor)
#        self.exe = common_lib.normalize_path(exe_str)
#        self.help_exe = self.exe + " " + Decoder_prop.dec_helps[self.id]
#        self.version_exe = self.exe + " " + Decoder_prop.dec_versions[self.id]
#        self.get_param_cmd = Decoder_prop.dec_cmd_func_list[self.id]
#
#    def __set_id(self, id):
#        if id in global_vars.ashevcd_name_list:
#            self.id = global_vars.ashevcd_name_list[0]
#        elif id in global_vars.hmd_name_list:
#            self.id = global_vars.hmd_name_list[0]
#        elif id in global_vars.jmd_name_list:
#            self.id = global_vars.jmd_name_list[0]
#        else:
#            self.id = 'ashevcd'
#
#
#    def __init__(self, id="ashevcd"):
#        self.__set_id(id)
#        self.__set_encoder_prop()
#
#
#    def set_encoder_id(self, id):
#        self.__set_id(id)
#        self.__set_encoder_prop()
#
#    def set_encoder_path(self, path):
#        Decoder_prop.dec_paths[self.id] = path
#        self.__set_encoder_prop()
#
#    @staticmethod
#    def SET_PATH(id, path):
#        Decoder_prop.dec_paths[id] = path


def get_default_dec_param_list():
    param_list = {}  # dict()  # create a dictinary
    param_list['input_filename'] = ''
    param_list['output_filename'] = ''
    # param_list['cons_filename']='cons.log'
    return param_list

def usage():
    help_msg = '''Usage:cl_run_dec.py [option] [value] ...
  options:
   -e <string> encoder name:ashevcd,hmd,jmd
   -i <string> input file name
   -o output the reconstruct file
   -h print this help
   -H print the decoder help
   -V print the decoder version info
   '''
    print help_msg
    return

def parse_dec_cl(dec, opt_list):
    if len(sys.argv) == 1:
        usage()
        sys.exit()

    help=common_lib.HELP(usage,dec.get_exe())
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'e:i:ohHV'+help.get_opt())
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    except Exception, e:
        print e

    #Help_flag = 0
    #Version_flag = 0
    Output_flag = 0

    for opt, arg in opts:
        if opt == "-i":
            opt_list["input_filename"] = arg
        elif opt == "-o":
            Output_flag = 1
            # opt_list["output_filename"] = arg
        #elif opt == "-h":
        #    usage()
        #    sys.exit()
        #elif opt == "-H":
        #    Help_flag = 1
        elif opt == "-e":
            dec.set_id(arg.strip())
        #elif opt == "-v":
        #    Version_flag = 1
        else:
            continue
            #assert False, "unknown option"

    help.parse_opt(opts)

    #if Help_flag == 1:
    #    os.system(dec.get_help_exe())
    #    sys.exit()

    #if Version_flag == 1:
    #    os.system(dec.get_version_exe())
    #    sys.exit()

    if len(opt_list['input_filename']) == 0:
        print "input isn't set"
        sys.exit()

    if len(args) > 0:
        opt_list['output_filename'] = args[0]

    dir_path, filename = os.path.split(opt_list['input_filename'])
    fname, fext = os.path.splitext(filename)
    if fext in global_vars.h264_extension and dec.get_id() not in global_vars.h264_decoder_list:
        dec.set_id(global_vars.jmd_name_list[0])
    if fext in global_vars.h265_extension and dec.get_id() not in global_vars.h265_decoder_list:
        dec.set_id(global_vars.ashevcd_name_list[0])

    cons_filename = fname + "_" + dec.get_id() + "_cons.log"
    cons_full = os.path.join(dir_path, cons_filename)
    if Output_flag == 1 and len(opt_list['output_filename']) == 0:
        output_filename = fname + "_rec.yuv"
        opt_list['output_filename'] = os.path.join(dir_path, output_filename)

    return cons_full,help.get_do_execute()

# def configure_dec_param(dec,param_list):
# cons_log=parse_dec_cl(dec,param_list)
#  return (cons_log,tmp_list['extra_cls'])
