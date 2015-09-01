#!/usr/bin/python
import os
import sys
import lib
import subprocess

encoder_id = "as265"
#enc = lib.Encoder_prop(encoder_id)
enc = lib.ENCODER(encoder_id)
#lib.ENCODER.SET_PATH("as265",
#                           r"D:\workspace\arcvideo_codes\HEVC_Codec\HEVC_Encoder4\bin\x64\Release_WithTrace")
lib.ENCODER.SET_PATH("x265",
                             r"D:\workspace\arcvideo_codes\HEVC_Codec\HEVC_Encoder\tool_X265_stable_2015_04_03_cbeb7d8a4880_modified_for_performance_test\build\vc10-x86_64\Release")
#lib.x265_ver="v1.6"

param_list = lib.get_default_enc_param_list()
# param_list['encder_exe']=lib.get_encoder_exe()
#param_list['output_path']="F:/encoder_test_output/as265_output/"
#param_list['input_path']="E:/sequences/"
#param_list['frame_num_to_encode']=100

#param_list['input_filename']="BlowingBubbles_416x240_50.yuv"
#seq_name="BlowingBubbles_416x240_50"
#param_list['eRcType']=1

cons = "tmp_cons.log"
#if len(sys.argv)> 1:
cons, extra_cls,do_execute = lib.configure_enc_param(enc, param_list)

cmd_line = lib.get_full_cdec_cmd(enc, param_list)
cmd_line += " " + extra_cls

#reg_file = None
#if lib.determin_sys() == "cygwin":
#    cmd_line += (" 2>&1 |tee -a " + cons)
#    pf = open(cons, "w")
#    print >> pf, "%s" % cmd_line
#    pf.close()
#else:
#    reg_file = open(cons, 'w')
#
##os.system(cmd_line)
#print cmd_line
#subprocess.call(cmd_line, shell=True, stdout=reg_file, stderr=reg_file)
lib.run_cmd(cmd_line,cons,do_execute)

