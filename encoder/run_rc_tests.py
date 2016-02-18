#!/bin/python
import lib
import os
import subprocess

#enc = lib.Encoder_prop()
enc = lib.ENCODER()

seq_list = ('BasketballPass_416x240_50', 'BlowingBubbles_416x240_50')
br_list = (1000, 1500, 2000, 3000)
param_list = lib.get_default_enc_param_list()

param_list['e_rctype'] = 1
param_list['i_frame_num_to_encode'] = 100
param_list['output_path'] = "F:/encoder_test_output/output0"
param_list['input_path'] = "f:/sequences/"
param_list['i_keyint'] = 30
param_list['i_maxref'] = 1
param_list['b_bframe_pyramid'] = 1
param_list['i_bframe'] = 3
param_list['b_open_gop'] = 0
param_list['i_scenecut_threshold'] = 0
param_list['i_bframe_adaptive'] = 0
param_list['i_preset'] = 5
param_list['i_frame_threads'] = 1
param_list['i_wpp_threads'] = 1
param_list['i_lookahead_threads'] = 1
param_list['i_aq_mode'] = 0
param_list['i_lookahead'] = 10
param_list['b_cutree'] = 0
param_list['i_lowres'] = 1

encoder_list = ("as265", "x265")
# encoder_list = ("as265", )
# encoder_list = ("x265", )
#lib.Encoder_prop.SET_PATH("as265","")
#lib.Encoder_prop.SET_PATH("x265","")

lib.remove_some_tmp_files(param_list['output_path'])

do_execute=0
for encoder_id in encoder_list:
    enc.set_id(encoder_id)
    for seq_name in seq_list:
        for bitrate in br_list:
            tag_str = "_" + encoder_id + "_bitrate" + str(bitrate)
            lib.configure_seq_param(param_list, seq_name, tags=tag_str)
            lib.check_params(param_list)
            lib.set_rc_full_param(param_list, bitrate)
            cmd = lib.get_full_cdec_cmd(enc, param_list)
            print cmd
            #os.system(cmd)
            reg_file_name = param_list['output_path'] + seq_name + tag_str + "_cons.log"
            #regression_file = open(reg_file_name, 'w')
            #subprocess.call(cmd, stdout=regression_file, shell=True)
            lib.run_cmd(cmd,do_execute,reg_file_name,1)
