#!/bin/python
__author__ = 'hfz2597'
#this file is degenerated
import lib
import os
import subprocess

enc = lib.ENCODER()

# seq_list = lib.class_std2+lib.class_special#('BasketballPass_416x240_50','BlowingBubbles_416x240_50')
# seq_list = lib.class_a
seq_list = ("blowing", 'basketball')
#seq_list +=lib.class_x
#br_list = (1000, 1500, 2000, 3000)
br_list = (0.0193,)  #0.0289,0.0386,0.0579)
param_list = lib.get_default_enc_param_list()

param_list['e_rctype'] = 1
param_list['i_frame_num_to_encode'] = -1
param_list['output_path'] = "F:/encoder_test_output/output0"
param_list['input_path'] = "f:/sequences/"
param_list['i_keyint'] = 300
param_list['i_maxref'] = 1
param_list['b_bframe_pyramid'] = 1
param_list['i_bframe'] = 3
param_list['b_open_gop'] = 1
param_list['i_scenecut_threshold'] = 40
param_list['i_bframe_adaptive'] = 0
param_list['i_preset'] = 5
param_list['i_frame_threads'] = 1
param_list['i_wpp_threads'] = 1
param_list['i_lookahead_threads'] = 1
param_list['i_aq_mode'] = 1
param_list['i_lookahead'] = 10
param_list['b_cutree'] = 1
param_list['i_lowres'] = 1

#encoder_list = ("as265", "x265")
encoder_list = ("as265", )
#encoder_list = ("x265", )
#lib.Encoder_prop.SET_PATH("as265","")
#lib.Encoder_prop.SET_PATH("x265","")

lib.remove_some_tmp_files(param_list['output_path'])

cnt = 0
for encoder_id in encoder_list:
    enc.set_id(encoder_id)
    for name in seq_list:
        seq_name = lib.guess_seqname(name)
        for bitrate in br_list:
            for p in range(1, 3):
                param_list['i_pass'] = p
                tag_str = "_" + encoder_id + "_bitrate" + str(bitrate) + "_pass" + str(p)
                lib.configure_seq_param(param_list, seq_name, tags=tag_str)
                lib.check_params(param_list)
                lib.set_rc_related_param_semi_auto(param_list, bitrate)
                cmd = lib.get_full_cdec_cmd(enc, param_list)
                print "%s\n" % cmd
                reg_file_name = param_list['output_path'] + seq_name + tag_str + "_cons.log"
                regression_file = open(reg_file_name, 'w')
                #print "%s\n"%regression_file
                #os.system(cmd)
                subprocess.call(cmd, stdout=regression_file, stderr=regression_file, shell=True)

