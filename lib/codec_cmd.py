#!/bin/python
__author__ = 'hfz2597'

import common_lib
import os
class Codec_st:
    def __init(self):
        exe_str = os.path.join(self.path, self.executor)
        self.exe = common_lib.normalize_path(exe_str)
        self.help_exe = self.exe + " " + self.help
        self.version_exe = self.exe + " " + self.version

    def __init__(self,id,executor,help,version,cmd_func,path):
        self.id=id
        self.executor=executor
        self.help=help
        self.version=version
        self.get_param_cmd=cmd_func
        self.path=common_lib.format_path(path)
        self.__init()
    def set_executor(self,executor):
        self.executor=executor
        self.__init()
    def set_path(self,path):
        self.path=path
        self.__init()

class CODEC:
    def __init__(self,get_cdec_st):
        #self.cdec_list=cdec_list
        self.get_cdec_st=get_cdec_st
        CODEC.get_cdec_st=get_cdec_st
    #def get_cdec_st(self,id):
    #    print "Warning: this function should not be called"
    #    return None
    def set_id(self,id):
        self.cdec_st=self.get_cdec_st(id)
    def set_path(self,path):
        self.cdec_st.set_path(path)
    def set_executor(self,executor):
        self.cdec_st.set_executor(executor)
    def get_id(self):
        return self.cdec_st.id
    def get_exe(self):
        return self.cdec_st.exe
    def get_help_exe(self):
        return self.cdec_st.help_exe
    def get_version_exe(self):
        return self.cdec_st.version_exe
    def get_param_cmd(self):
        return self.cdec_st.get_param_cmd
    @staticmethod
    def SET_CDEC_PATH(id,path):
        CODEC.get_cdec_st(id).set_path(path)
    @staticmethod
    def SET_CDEC_EXECUTOR(id,executor):
        CODEC.get_cdec_st(id).set_executor(executor)

def get_full_cdec_cmd(enc, param_list):
    #param_cmd=""
    #if enc.id=="as265":
    #  param_cmd=as265_cmd_init.get_param_cmd_as265(param_list)
    #elif enc.id=="x265":
    #  param_cmd=x26x_cmd_init.get_param_cmd_x265(param_list)
    #elif enc.id=="x264":
    #  param_cmd=x26x_cmd_init.get_param_cmd_x264(param_list)
    param_cmd = enc.get_param_cmd()(param_list)
    exe = enc.get_exe()
    full_cmd_line = exe + " " + param_cmd
    return full_cmd_line


