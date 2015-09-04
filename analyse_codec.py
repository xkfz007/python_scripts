#!/bin/python
__author__ = 'hfz2597'
import lib
import lib.global_vars

class Analyzer_t(object):
    def __init__(self,id,pattern,qp_idx,bits_idx,addational_cl):
        self.id=id
        self.pattern=pattern
        self.qp_idx=qp_idx
        self.bits_idx=bits_idx
        self.addational_cl=addational_cl
    def get_cl(self,input_file,idx=0):
        cl_list = []
        cl_list.append('grep -o "' + self.pattern+ '" "' + input_file + '"')
        cl_list.append('awk \'{print $' + str(idx) + '}\'')
        cl_list.extend(self.addational_cl)
        cmd='|'.join(cl_list)
        return cmd

common_cl='tr -t "\\n" " "'
ashevcd_t=Analyzer_t(lib.ashevcd_name_list[0],'Frm.*',20,3,[common_cl])
hmd_t=Analyzer_t(lib.hmd_name_list[0],'',-1,-1,[])
jmd_t=Analyzer_t(lib.jmd_name_list[0],'',-1,-1,[])
as265_t=Analyzer_t(lib.as265_name_list[0],'POC.*bits',   7, 8,['awk -F\( \'{print $1}\'',common_cl])
x265_t =Analyzer_t(lib.x265_name_list[0], 'POC.*bits',   4, 5,['awk -F\( \'{print $1}\'',common_cl])
x264_t =Analyzer_t(lib.x264_name_list[0], 'frame=.*bits',3,10,['awk -F\= \'{print $2}\'',common_cl])
hm_t=Analyzer_t(lib.x264_name_list[0],'',-1,-1,[])
jm_t=Analyzer_t(lib.x264_name_list[0],'',-1,-1,[])


dec_st_list={lib.ashevcd_name_list[0]:ashevcd_t,
             lib.jmd_name_list[0]:jmd_t,
             lib.hmd_name_list[0]:hmd_t,
             lib.as265_name_list[0]:as265_t,
             lib.x265_name_list[0]:x265_t,
             lib.x264_name_list[0]:x264_t,
             lib.hm_name_list[0]:hm_t,
             lib.jm_name_list[0]:jm_t,
             }

def get_analyser_t(id):
    if id in lib.ashevcd_name_list:
        id = lib.ashevcd_name_list[0]
    elif id in lib.hmd_name_list:
        id = lib.hmd_name_list[0]
    elif id in lib.jmd_name_list:
        id = lib.jmd_name_list[0]
    elif id in lib.as265_name_list:
        id = lib.as265_name_list[0]
    elif id in lib.x265_name_list:
        id = lib.x265_name_list[0]
    elif id in lib.x264_name_list:
        id = lib.x264_name_list[0]
    elif id in lib.hm_name_list:
        id = lib.hm_name_list[0]
    elif id in lib.jm_name_list:
        id = lib.jm_name_list[0]
    else:
        id = 'ashevcd'
    return dec_st_list[id]
class ANALYZER(object):

    def __init__(self,id='ashevcd'):
        self.ana_t=get_analyser_t(id)
    def set_id(self,id):
        self.ana_t=get_analyser_t(id)
    def get_qp_cmd(self,input_file):
        return self.ana_t.get_cl(input_file,self.ana_t.qp_idx)
    def get_bits_cmd(self,input_file):
        return self.ana_t.get_cl(input_file,self.ana_t.bits_idx)


def usage():
    msg='''usage:analysis_file.py [options]
    -e <id> set the encoder or decoder
    -i <filename> set input file name
    --bits <filename> output bits of each frame
    --qp <filename> output qp of each frame
  '''
    print msg
    return

import sys
import os
import getopt


if __name__=='__main__':#obtain_data():
    if len(sys.argv) == 1:
        usage()
        sys.exit()

    help=lib.common_lib.HELP(usage)
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'e:i:'+help.get_opt(), ['bits=', 'qps=', 'qp='])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    except Exception, e:
        print e

    cdc = ANALYZER()

    bits_flag = 0
    qp_flag = 0
    qps_flag = 0
    input_file = ''
    bits_output = ''
    qp_output = ''
    qps_output = ''
    for opt, arg in opts:
        if opt in ('--bits',):
            bits_flag = 1
            bits_output = arg
        elif opt in ('--qp',):
            qp_flag = 1
            qp_output = arg
        elif opt in ('--qps',):
            qps_flag = 1
            qps_output = arg
        elif opt in ('-i',):
            input_file = arg
        elif opt in ('-e',):
            cdc.set_id(arg.strip())
        #elif opt[1] in help.get_opt():
        #    help.parse_opt(opt)
        else:
            help.parse_opt(opt)


    if bits_flag == 1:
        cmd = cdc.get_bits_cmd(input_file)
        lib.run_cmd(cmd, bits_output,help.get_do_execute(),0)

    if qp_flag == 1:
        cmd = cdc.get_qp_cmd(input_file)
        lib.run_cmd(cmd, qp_output,help.get_do_execute(),0)
        #if help.get_do_execute()==1:
        #   os.system(cmd)
