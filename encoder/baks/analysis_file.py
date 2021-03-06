#!/bin/python
import subprocess
import lib


class Codec_analysis:
    id = ""
    fstr = ""
    __format_strs = {}  # dict()
    __format_strs["as265"] = "POC.*bits"
    __format_strs["x265"] = "POC.*bits"
    __format_strs["x264"] = "frame=.*bits"
    __format_strs["hm"] = ""
    __format_strs["jm"] = ""
    __format_strs["ashevcd"] = "Frm.*"
    __format_strs["hmd"] = ""
    __format_strs["jmd"] = ""

    qp_idx = 0
    __qp_idxs = {}
    __qp_idxs["as265"] = 7
    __qp_idxs["x265"] = 4
    __qp_idxs["x264"] = 3
    __qp_idxs["hm"] = -1
    __qp_idxs["jm"] = -1
    __qp_idxs["ashevcd"] = 20
    __qp_idxs["hmd"] = -1
    __qp_idxs["jmd"] = -1

    bits_idx = 0
    __bits_idxs = {}
    __bits_idxs["as265"] = 8
    __bits_idxs["x265"] = 5
    __bits_idxs["x264"] = 10
    __bits_idxs["hm"] = -1
    __bits_idxs["jm"] = -1
    __bits_idxs["ashevcd"] = 3
    __bits_idxs["hmd"] = -1
    __bits_idxs["jmd"] = -1

    def __set_codec_prop(self):
        self.fstr = Codec_analysis.__format_strs[self.id]
        self.qp_idx = Codec_analysis.__qp_idxs[self.id]
        self.bits_idx = Codec_analysis.__bits_idxs[self.id]

    def __init__(self, id="as265"):
        self.id = id
        self.__set_codec_prop()

    def set_codec_id(self, id):
        self.id = id
        self.__set_codec_prop()


    def get_cl_ashevcd(self, input_file, idx=0):
        cl_list = []
        cl_list.append('grep -o "' + self.fstr + '" "' + input_file + '"')
        cl_list.append('awk \'{print $' + str(idx) + '}\'')
        cl_list.append('tr -t "\\n" " "')
        return cl_list

    def get_cl_hmd(self, input_file, idx=0):
        cl_list = []
        return cl_list

    def get_cl_jmd(self, input_file, idx=0):
        cl_list = []
        return cl_list

    def get_cl_as265(self, input_file, idx=0):
        cl_list = []
        cl_list.append('grep -o "' + self.fstr + '" "' + input_file + '"')
        cl_list.append('awk \'{print $' + str(idx) + '}\'')
        cl_list.append('awk -F\( \'{print $1}\'')
        cl_list.append('tr -t "\\n" " "')
        return cl_list

    def get_cl_x265(self, input_file, idx=0):
        cl_list = []
        cl_list.append('grep -o "' + self.fstr + '" "' + input_file + '"')
        cl_list.append('awk \'{print $' + str(idx) + '}\'')
        cl_list.append('awk -F\( \'{print $1}\'')
        cl_list.append('tr -t "\\n" " "')
        return cl_list

    def get_cl_x264(self, input_file, idx=0):
        cl_list = []
        cl_list.append('grep -o "' + self.fstr + '" "' + input_file + '"')
        cl_list.append('awk \'{print $' + str(idx) + '}\'')
        cl_list.append('awk -F\= \'{print $2}\'')
        cl_list.append('tr -t "\\n" " "')
        return cl_list

    def get_cl_hm(self, input_file, idx=0):
        cl_list = []
        return cl_list

    def get_cl_jm(self, input_file, idx=0):
        cl_list = []
        return cl_list

    __func_list = {}  # dict()
    __func_list["ashevcd"] = get_cl_ashevcd
    __func_list["hmd"] = get_cl_hmd
    __func_list["jmd"] = get_cl_jmd
    __func_list["as265"] = get_cl_as265
    __func_list["x265"] = get_cl_x265
    __func_list["x264"] = get_cl_x264
    __func_list["hm"] = get_cl_hm
    __func_list["jm"] = get_cl_jm

    def get_full_cmd(self, input_file, idx=0):
        cl_list = Codec_analysis.__func_list[self.id](self, input_file, idx)
        full_cl = "|".join(cl_list)
        return full_cl

    def get_qp_fcmd(self, input_file):
        return self.get_full_cmd(input_file, self.qp_idx)

    def get_bits_fcmd(self, input_file):
        return self.get_full_cmd(input_file, self.bits_idx)

    # def get_col_vals(self, input_file, idx=0):
    #  # if lib.determin_sys()=="windows":
    #  #  return
    #  cl_list = Codec_analysis.__func_list[self.id](self, input_file, idx)
    #  full_cl = "|".join(cl_list)
    #  print full_cl
    #  output = subprocess.check_output(full_cl, shell=True)
    #  return output

    #def get_qp_vals(self, input_file):
    #  return self.get_col_vals(input_file, self.qp_idx)

    #def get_bits_vals(self, input_file):
    #  return self.get_col_vals(input_file, self.bits_idx)


# def get_qp_ashevcd(input_file,idx):
# if lib.determin_sys()=="windows":
#    return
#  format_string="Frm.*"
#  grep_cl="grep -o '"+format_string+"' "+input_file
#  awk_cl="awk '{print $"+str(idx)+"}'"
#  tr_cl="tr -t '\n' ' '"
#  full_cl=grep_cl+"|"+awk_cl+"|"+tr_cl
#  output=subprocess.check_output(full_cl,shell=True)
#  return output
#def run_cmd(cmd, filename=''):
#    if filename == '':
#        outFile = None
#    else:
#        outFile = open(filename, 'w')
#    subprocess.call(cmd, stdout=outFile, stderr=outFile, shell=True)

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


help=lib.common_lib.HELP(usage,'','--help')
if __name__=='__main__':#obtain_data():
    if len(sys.argv) == 1:
        help.usage()
        sys.exit()

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'e:i:'+help.get_opt(), ['bits=', 'qps=', 'qp='])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    except Exception, e:
        print e

    cdc = Codec_analysis()

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
            cdc.set_codec_id(arg.strip())
        elif opt[1] in help.get_opt():
            help.parse_opt(opt)
        else:
            assert False, "unknown option"

    if bits_flag == 1:
        cmd = cdc.get_bits_fcmd(input_file)
        #print cmd
        lib.run_cmd(cmd, bits_output,help.get_do_execute(),0)

    if qp_flag == 1:
        cmd = cdc.get_qp_fcmd(input_file)
        #print cmd
        lib.run_cmd(cmd, qp_output,help.get_do_execute(),0)
        #if help.get_do_execute()==1:
        #   os.system(cmd)


#obtain_data()
#parse_cl()
#cdc=Codec_analysis("ashevcd")

#input_file="F:\\tmp\\2015.04.13\\cons.log"
#output_str=cdc.get_qp_vals(lib.format_file_path("F:\\tmp\\2015.04.13\\cons.log"))
#output_str=cdc.get_qp_vals()
#print output_str
#full_cmd=cdc.get_qp_fcmd(input_file)
#output_file="f:\\tmp\\2015.04.13\\aaa.txt"
#outFile = open(output_file, 'w')
#subprocess.call(full_cmd,stdout=outFile,shell=True)


