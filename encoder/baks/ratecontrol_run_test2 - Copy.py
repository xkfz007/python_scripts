#!/usr/bin/python
import os
import _RateControl


def init_param_list_default():


param_list = dict()  # create a dictinary

param_list['encder_exe'] = "cli_ashevc.exe"
param_list['output_path'] = "f:\\hfz\\_HD-User_D_TEMP\\_Video_data_temp\\_Regression_Temp\\"
param_list['output_filename'] = "cli_ashevc.exe"
param_list['input_path'] = "E:\\_HD-User_H_DATA\\z_Const_Data__TestResource\\_Video_data_const_hd\\"
param_list['input_filename'] = "cli_ashevc.exe"

param_list['trace_file_cabac'] = "cli_ashevc.exe"
param_list['trace_file_general'] = "cli_ashevc.exe"
param_list['dump_file_rec'] = "cli_ashevc.exe"
param_list['trace_file_prd_y'] = "cli_ashevc.exe"
param_list['trace_file_prd_uv'] = "cli_ashevc.exe"
param_list['trace_file_cabacrdo'] = "cli_ashevc.exe"
param_list['trace_file_arch1rdo'] = "cli_ashevc.exe"

# debug related paramters
param_list['printf_flag'] = 1  #225
param_list['trace_flag'] = 1  #7
param_list['measure_quality_flag'] = 1

param_list['i_frame_num_to_encode'] = 100

#cu pu tu
param_list['i_max_cuwidth'] = 64
param_list['i_max_cudepth'] = 4
param_list['i_max_tulog2width'] = 5
param_list['i_min_tulog2width'] = 2
param_list['i_max_intra_tudepth'] = 3
param_list['i_min_inter_tudepth'] = 3

#gop
param_list['i_keyint'] = 30
param_list['i_maxref'] = 1
param_list['b_bframe_pyramid'] = 0
param_list['i_bframe'] = 0
param_list['b_multiple_sublayer'] = 0
param_list['i_decoding_refresh_type'] = 2

param_list['b_open_gop'] = 0
param_list['i_scenecut_threshold'] = 0
param_list['i_bframe_adaptive'] = 0
param_list['b_repeat_headers'] = 0

#feature
param_list['b_amp'] = 0
param_list['b_dbl'] = 1
param_list['b_sao'] = 0

#rc
param_list['e_rctype'] = 1
param_list['i_qp'] = 33
param_list['i_bitrate'] = 0
param_list['i_max_bitrate'] = 0
param_list['i_buffer_size'] = 0
param_list['i_buffer_init_time'] = 0

#i_preset
param_list['i_preset'] = 5

#debug parameters
param_list['i_first_frame'] = 0
param_list['b_random_cost'] = 0
param_list['b_force_tu_split'] = 0
param_list['b_force_one_intra_mode'] = 0
param_list['b_arcvideo'] = 1

#asm
param_list['b_asm'] = 1

#architecture and algorithm
param_list['i_architecture_id'] = 2
param_list['i_algorithm_suit_id'] = 0

param_list['i_frame_threads'] = 1
param_list['i_wpp_threads'] = 1
param_list['i_lookahead_threads'] = 1

param_list['e_rps'] = 1

param_list['i_log2_parallel_merge_level'] = 2
param_list['b_slice_temporal_mvp_enabled'] = 1
param_list['b_constrained_intra_pred'] = 0

param_list['me_method'] = 1
param_list['i_me_range'] = 32
param_list['i_subpel_refine'] = 5
param_list['b_chroma_me'] = 1

param_list['f_rate_tolerance'] = 1.0
param_list['f_rf_constant'] = 23
param_list['i_qp_min'] = 0
param_list['i_qp_max'] = 51
param_list['i_qp_step'] = 4
param_list['f_ip_factor'] = 1.4
param_list['f_pb_factor'] = 1.3
param_list['i_aq_mode'] = 0
param_list['f_aq_strength'] = 1.0
param_list['i_lookahead'] = 10
param_list['b_cutree'] = 0
param_list['i_lowres'] = 1
param_list['i_pass'] = 0

for seq_name in _RateControl.classC:
    reso_info = _RateControl.get_reso_info(seq_name)
    param_list['i_src_width'] = reso_info[0]
    param_list['i_src_height'] = reso_info[1]
    param_list['f_framerate'] = reso_info[2]

    param_list['output_filename'] = seq_name + "_str.bin"
    param_list['input_filename'] = seq_name + ".yuv"
    param_list['trace_file_cabac'] = seq_name + "_cabac.log"
    param_list['trace_file_general'] = seq_name + "_general.log"
    param_list['dump_file_rec'] = seq_name + "_rec.yuv"
    param_list['trace_file_prd_y'] = seq_name + "_prdy.log"
    param_list['trace_file_prd_uv'] = seq_name + "_prduv.log"
    param_list['trace_file_cabacrdo'] = seq_name + "_cabacrdo.log"
    param_list['trace_file_arch1rdo'] = seq_name + "_arch1rdo.log"

    rc_param = _RateControl.get_bitrate_for_rc(param_list['e_rctype'], param_list['i_src_width'], param_list['i_src_height'],
                                               param_list['f_framerate'], 2)
    param_list['i_bitrate'] = rc_param[0]
    param_list['i_max_bitrate'] = rc_param[1]
    param_list['i_buffer_size'] = rc_param[2]
    g_as265_EncoderExeName = "cli_ashevc.exe"
    g_as265_x64ReleaseWithTraceEncoderExePath = "..\\bin\\x64\\Release_WithTrace\\"

    #cmd="/cygdrive/d/workspace/arcsoft_codes/HEVC_Codec/HEVC_Encoder/bin/x64/Release_WithTrace/cli_ashevc.exe"
    cmd = g_as265_x64ReleaseWithTraceEncoderExePath + g_as265_EncoderExeName

    cmd += " %s" % param_list['output_path']
    cmd += " %s" % param_list['output_filename']
    cmd += " %s" % param_list['input_path']
    cmd += " %s" % param_list['input_filename']

    cmd += " %s" % param_list['trace_file_cabac']
    cmd += " %s" % param_list['trace_file_general']
    cmd += " %s" % param_list['dump_file_rec']
    cmd += " %s" % param_list['trace_file_prd_y']
    cmd += " %s" % param_list['trace_file_prd_uv']
    cmd += " %s" % param_list['trace_file_cabacrdo']
    cmd += " %s" % param_list['trace_file_arch1rdo']

    cmd += " %s" % param_list['printf_flag']
    cmd += " %s" % param_list['trace_flag']
    cmd += " %s" % param_list['measure_quality_flag']

    cmd += " %s" % param_list['i_src_width']
    cmd += " %s" % param_list['i_src_height']
    cmd += " %s" % param_list['f_framerate']
    cmd += " %s" % param_list['i_frame_num_to_encode']

    # cu pu tu
    cmd += " %s" % param_list['i_max_cuwidth']
    cmd += " %s" % param_list['i_max_cudepth']
    cmd += " %s" % param_list['i_max_tulog2width']
    cmd += " %s" % param_list['i_min_tulog2width']
    cmd += " %s" % param_list['i_max_intra_tudepth']
    cmd += " %s" % param_list['i_min_inter_tudepth']

    # gop
    cmd += " %s" % param_list['i_keyint']
    cmd += " %s" % param_list['i_maxref']
    cmd += " %s" % param_list['b_bframe_pyramid']
    cmd += " %s" % param_list['i_bframe']
    cmd += " %s" % param_list['b_multiple_sublayer']
    cmd += " %s" % param_list['i_decoding_refresh_type']

    cmd += " %s" % param_list['b_open_gop']
    cmd += " %s" % param_list['i_scenecut_threshold']
    cmd += " %s" % param_list['i_bframe_adaptive']

    # feature
    cmd += " %s" % param_list['b_amp']
    cmd += " %s" % param_list['b_dbl']
    cmd += " %s" % param_list['b_sao']

    # rc
    cmd += " %s" % param_list['e_rctype']
    cmd += " %s" % param_list['i_qp']
    cmd += " %s" % param_list['i_bitrate']
    cmd += " %s" % param_list['i_max_bitrate']
    cmd += " %s" % param_list['i_buffer_size']
    cmd += " %s" % param_list['i_buffer_init_time']

    #i_preset
    cmd += " %s" % param_list['i_preset']

    # debug ters
    cmd += " %s" % param_list['i_first_frame']
    cmd += " %s" % param_list['b_random_cost']
    cmd += " %s" % param_list['b_force_tu_split']
    cmd += " %s" % param_list['b_force_one_intra_mode']

    cmd += " %s" % param_list['b_arcvideo']

    # asm
    cmd += " %s" % param_list['b_asm']

    # architecture and algorithm
    cmd += " %s" % param_list['i_architecture_id']
    cmd += " %s" % param_list['i_algorithm_suit_id']

    # threading
    cmd += " %s" % param_list['i_frame_threads']
    cmd += " %s" % param_list['i_wpp_threads']
    cmd += " %s" % param_list['i_lookahead_threads']

    # rps
    cmd += " %s" % param_list['e_rps']

    # pred
    cmd += " %s" % param_list['i_log2_parallel_merge_level']
    cmd += " %s" % param_list['b_slice_temporal_mvp_enabled']
    cmd += " %s" % param_list['b_constrained_intra_pred']

    # analyze
    cmd += " %s" % param_list['me_method']
    cmd += " %s" % param_list['i_me_range']
    cmd += " %s" % param_list['i_subpel_refine']
    cmd += " %s" % param_list['b_chroma_me']

    # rc
    cmd += " %s" % param_list['f_rate_tolerance']
    cmd += " %s" % param_list['f_rf_constant']
    cmd += " %s" % param_list['i_qp_min']
    cmd += " %s" % param_list['i_qp_max']
    cmd += " %s" % param_list['i_qp_step']
    cmd += " %s" % param_list['f_ip_factor']
    cmd += " %s" % param_list['f_pb_factor']
    cmd += " %s" % param_list['i_aq_mode']
    cmd += " %s" % param_list['f_aq_strength']
    cmd += " %s" % param_list['i_lookahead']
    cmd += " %s" % param_list['b_cutree']
    cmd += " %s" % param_list['i_lowres']
    cmd += " %s" % param_list['i_pass']

    print cmd
    os.system(cmd)
  
