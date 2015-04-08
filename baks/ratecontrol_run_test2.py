#!/usr/bin/python
import os
import _RateControl

param_list=_RateControl.init_param_list_default()

g_as265_EncoderExeName = "cli_ashevc.exe"
g_as265_x64ReleaseWithTraceEncoderExePath = "..\\bin\\x64\\Release_WithTrace\\"
param_list['encder_exe']=g_as265_x64ReleaseWithTraceEncoderExePath+g_as265_EncoderExeName

param_list['output_path']="f:\\hfz\\_HD-User_D_TEMP\\_Video_data_temp\\_Regression_Temp\\"
param_list['input_path']="E:\\_HD-User_H_DATA\\z_Const_Data__TestResource\\_Video_data_const_hd\\"
param_list['frame_num_to_encode']=1000
rc_test_list=[1,3,8]
#all_seq_list=[_RateControl.classB,_RateControl.classC,_RateControl.classD,_RateControl.classE]
#print all_seq_list
seq_list=_RateControl.classB+_RateControl.classC
print seq_list

#for item in all_seq_list:
#  print "==========%s=============" % item
for seq_name in seq_list:
  print "==========%s=============" % seq_name
  for eRcType in rc_test_list:
    print "==========eRcType=%s=============" % eRcType
    param_list['eRcType']=eRcType
    for factor in range(1,3):
      print "==========factor=%s=============" % factor
      _RateControl.set_seq_related_param(param_list,seq_name)
      _RateControl.set_rc_related_param_auto(param_list,factor)
      cmd=_RateControl.get_cmd_line(param_list)
      print cmd
      #os.system(cmd)
  
