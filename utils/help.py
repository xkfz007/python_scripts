#!/bin/python
__author__ = 'Felix'
import sys
import os
import log

class HELP(object):
    default_opt='hHY'
    #m_LogOut = log.Log('HELP')
    def __init__(self,usage,BIN='',help='--help',m_log= log.Log('HELP')):
        self.usage=usage
        self.BIN=BIN
        self.help=help
        self.do_execute=0
        self.m_LogOut=m_log

    def set_BIN(self,BIN):
        self.BIN=BIN

    def set_help(self,help):
        self.help=help

    def set_do_execute(self,do_execute=1):
        self.do_execute=do_execute

    def get_opt(self):
        return HELP.default_opt

    def add_usage(self):
        msg='ADDITIONAL OPTIONS:\n'
        msg+='   -h  print this help\n'
        if len(self.BIN)>0:
            msg+='   -H  print help of "%s"\n'%self.BIN
        msg+='   -Y  whether to execute the program\n'
        print msg

    def parse_opt(self,opt):
        if opt == '-h':
            self.usage()
            self.add_usage()
            sys.exit()
        elif opt == '-H':
            if len(self.BIN)>0:
                os.system(self.BIN+' '+self.help)
            else:
                self.m_LogOut.error('Executor is not set')
            sys.exit()
        elif opt == '-Y':
            self.set_do_execute()
        else:
            self.m_LogOut.warning('unknown option:%s'%opt)

    def get_do_execute(self):
        return self.do_execute

