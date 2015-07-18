#!/bin/python
import lib
import os


enc = lib.Encoder_prop()

#seq_list = lib.class_std2+lib.class_special#('BasketballPass_416x240_50','BlowingBubbles_416x240_50')
seq_list = lib.class_a
#seq_list +=lib.class_x
#br_list = (1000, 1500, 2000, 3000)
br_list=(0.0193,)#0.0289,0.0386,0.0579)
param_list = lib.get_default_enc_param_list()

param_list['eRcType'] = 8
param_list['frame_num_to_encode'] =100
param_list['output_path'] = "F:/encoder_test_output/output0"
param_list['input_path'] = "f:/sequences/"
param_list['nIntraPicInterval'] = 300
param_list['nMaxRefNum'] = 1
param_list['bExistRefB'] = 1
param_list['nBframe'] = 3
param_list['b_open_gop'] = 1
param_list['i_scenecut_threshold'] = 40
param_list['i_bframe_adaptive'] = 0
param_list['preset'] = 5
param_list['frame_threads'] = 1
param_list['wpp_threads'] = 1
param_list['lookahead_threads'] = 1
param_list['rc_i_aq_mode'] = 1
param_list['rc_i_lookahead'] = 10
param_list['rc_b_cutree'] = 1
param_list['rc_i_lowres'] = 1
param_list['rc_i_pass'] = 1

#encoder_list = ("as265", "x265")
encoder_list = ("as265", )
#encoder_list = ("x265", )
#lib.Encoder_prop.SET_PATH("as265","")
#lib.Encoder_prop.SET_PATH("x265","")

max_task_num=1
tm=lib.TaskManager(max_task_num)

lib.remove_some_tmp_files(param_list['output_path'])

total_task_num=len(encoder_list)*len(seq_list)*len(br_list)
logout=lib.Log()

cnt=0
for encoder_id in encoder_list:
  enc.set_encoder_id(encoder_id)
  for name in seq_list:
    seq_name=lib.guess_seqname(name)
    for bitrate in br_list:
      tag_str="_"+encoder_id+"_bitrate"+str(bitrate)
      lib.configure_seq_param(param_list, seq_name,tags=tag_str)
      lib.check_params(param_list)
      lib.set_rc_related_param_semi_auto(param_list, bitrate)
      cmd = lib.get_full_cdec_cmd(enc, param_list)
      #print "%s\n"%cmd
      regression_file=param_list['output_path']+seq_name+tag_str+"_cons.log"
      #os.system(cmd)
      tm.newTask(cmd,regression_file)
      cnt=cnt+1
      logout.warn("task_progress:%s/%s"%(cnt,total_task_num))

tm.clearAllTask()
