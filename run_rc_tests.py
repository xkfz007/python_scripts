#!/bin/python
import lib
import os

enc = lib.Encoder_prop()

seq_list = ('BasketballPass_416x240_50',)
br_list = (1000,)# 1500, 2000, 3000)
param_list = lib.get_default_param_list()

param_list['eRcType'] = 3
param_list['frame_num_to_encode'] = -1
param_list['output_path'] = "F:/encoder_test_output/output0"
param_list['nIntraPicInterval'] = 30
param_list['nMaxRefNum'] = 1
param_list['bExistRefB'] = 1
param_list['nBframe'] = 3
param_list['b_open_gop'] = 0
param_list['i_scenecut_threshold'] = 0
param_list['i_bframe_adaptive'] = 0
param_list['preset'] = 5
param_list['frame_threads'] = 1
param_list['wpp_threads'] = 1
param_list['lookahead_threads'] = 1
param_list['rc_i_aq_mode'] = 0
param_list['rc_i_lookahead'] = 10
param_list['rc_b_cutree'] = 0
param_list['rc_i_lowres'] = 1

#encoder_list = ("as265", "x265")
#encoder_list = ("as265", )
encoder_list = ("x265", )

for encoder_id in encoder_list:
  enc.set_encoder_id(encoder_id)
  for seq_name in seq_list:
    for bitrate in br_list:
      lib.set_seq_related_param(param_list, seq_name)
      lib.check_params(param_list)
      lib.set_rc_related_param_manual(param_list, bitrate, bitrate, bitrate)
      cmd = lib.get_full_cmd(enc, param_list)
      print cmd
      os.system(cmd)
