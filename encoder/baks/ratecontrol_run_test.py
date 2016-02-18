#!/usr/bin/python
import os
import _RateControl

output_path = "f:\\hfz\\_HD-User_D_TEMP\\_Video_data_temp\\_Regression_Temp\\"
input_path = "E:\\_HD-User_H_DATA\\z_Const_Data__TestResource\\_Video_data_const_hd\\"

# debug related paramters
printf_flag = 1  #225
trace_flag = 1  #7
measure_quality_flag = 1

i_frame_num_to_encode = 100

#cu pu tu
i_max_cuwidth = 64
i_max_cudepth = 4
i_max_tulog2width = 5
i_min_tulog2width = 2
i_max_intra_tudepth = 3
i_min_inter_tudepth = 3

#gop
i_keyint = 30
i_maxref = 1
b_bframe_pyramid = 0
i_bframe = 0
b_multiple_sublayer = 0
i_decoding_refresh_type = 2

b_open_gop = 0
i_scenecut_threshold = 0
i_bframe_adaptive = 0
b_repeat_headers = 0

#feature
b_amp = 0
b_dbl = 1
b_sao = 0

#rc
rc_methods = ["CQP", "CBR", "QUALITY_RANK", "VBR", "CONFERENCE", "VBR_TWOPASS_ANALYSE", "VBR_TWOPASS_ENC", "VBR_Q",
              "ABR"]
e_rctype = 1
i_qp = 33
i_bitrate = 0
i_max_bitrate = 0
i_buffer_size = 0
i_buffer_init_time = 0

#i_preset
i_preset = 5

#debug parameters
i_first_frame = 0
b_random_cost = 0
b_force_tu_split = 0
b_force_one_intra_mode = 0
b_arcvideo = 1

#asm
b_asm = 1

#architecture and algorithm
i_architecture_id = 2
i_algorithm_suit_id = 0

i_frame_threads = 1
i_wpp_threads = 1
i_lookahead_threads = 1

e_rps = 1

i_log2_parallel_merge_level = 2
b_slice_temporal_mvp_enabled = 1
b_constrained_intra_pred = 0

me_method = 1
i_me_range = 32
i_subpel_refine = 5
b_chroma_me = 1

f_rate_tolerance = 1.0
f_rf_constant = 23
i_qp_min = 0
i_qp_max = 51
i_qp_step = 4
f_ip_factor = 1.4
f_pb_factor = 1.3
i_aq_mode = 0
f_aq_strength = 1.0
i_lookahead = 10
b_cutree = 0
i_lowres = 1
i_pass = 0

for seq_name in _RateControl.classC:
    reso_info = _RateControl.get_reso_info(seq_name)
    i_src_width = int(reso_info[0])
    i_src_height = int(reso_info[1])
    f_framerate = int(reso_info[2])

    output_filename = seq_name + "_str.bin"
    input_filename = seq_name + ".yuv"
    trace_file_cabac = seq_name + "_cabac.log"
    trace_file_general = seq_name + "_general.log"
    dump_file_rec = seq_name + "_rec.yuv"
    trace_file_prd_y = seq_name + "_prdy.log"
    trace_file_prd_uv = seq_name + "_prduv.log"
    trace_file_cabacrdo = seq_name + "_cabacrdo.log"
    trace_file_arch1rdo = seq_name + "_arch1rdo.log"

    rc_param = _RateControl.get_bitrate_for_rc(rc_methods[e_rctype], i_src_width, i_src_height, f_framerate)
    i_bitrate = rc_param[0]
    i_max_bitrate = rc_param[1]
    i_buffer_size = rc_param[2]
    g_as265_EncoderExeName = "cli_ashevc.exe"
    g_as265_x64ReleaseWithTraceEncoderExePath = "..\\bin\\x64\\Release_WithTrace\\"

    #cmd="/cygdrive/d/workspace/arcsoft_codes/HEVC_Codec/HEVC_Encoder/bin/x64/Release_WithTrace/cli_ashevc.exe"
    cmd = g_as265_x64ReleaseWithTraceEncoderExePath + g_as265_EncoderExeName

    cmd += " %s" % output_path
    cmd += " %s" % output_filename
    cmd += " %s" % input_path
    cmd += " %s" % input_filename

    cmd += " %s" % trace_file_cabac
    cmd += " %s" % trace_file_general
    cmd += " %s" % dump_file_rec
    cmd += " %s" % trace_file_prd_y
    cmd += " %s" % trace_file_prd_uv
    cmd += " %s" % trace_file_cabacrdo
    cmd += " %s" % trace_file_arch1rdo

    cmd += " %s" % printf_flag
    cmd += " %s" % trace_flag
    cmd += " %s" % measure_quality_flag

    cmd += " %s" % i_src_width
    cmd += " %s" % i_src_height
    cmd += " %s" % f_framerate
    cmd += " %s" % i_frame_num_to_encode

    # cu pu tu
    cmd += " %s" % i_max_cuwidth
    cmd += " %s" % i_max_cudepth
    cmd += " %s" % i_max_tulog2width
    cmd += " %s" % i_min_tulog2width
    cmd += " %s" % i_max_intra_tudepth
    cmd += " %s" % i_min_inter_tudepth

    # gop
    cmd += " %s" % i_keyint
    cmd += " %s" % i_maxref
    cmd += " %s" % b_bframe_pyramid
    cmd += " %s" % i_bframe
    cmd += " %s" % b_multiple_sublayer
    cmd += " %s" % i_decoding_refresh_type

    cmd += " %s" % b_open_gop
    cmd += " %s" % i_scenecut_threshold
    cmd += " %s" % i_bframe_adaptive

    # feature
    cmd += " %s" % b_amp
    cmd += " %s" % b_dbl
    cmd += " %s" % b_sao

    # rc
    cmd += " %s" % e_rctype
    cmd += " %s" % i_qp
    cmd += " %s" % i_bitrate
    cmd += " %s" % i_max_bitrate
    cmd += " %s" % i_buffer_size
    cmd += " %s" % i_buffer_init_time

    #i_preset
    cmd += " %s" % i_preset

    # debug ters
    cmd += " %s" % i_first_frame
    cmd += " %s" % b_random_cost
    cmd += " %s" % b_force_tu_split
    cmd += " %s" % b_force_one_intra_mode

    cmd += " %s" % b_arcvideo

    # asm
    cmd += " %s" % b_asm

    # architecture and algorithm
    cmd += " %s" % i_architecture_id
    cmd += " %s" % i_algorithm_suit_id

    # threading
    cmd += " %s" % i_frame_threads
    cmd += " %s" % i_wpp_threads
    cmd += " %s" % i_lookahead_threads

    # rps
    cmd += " %s" % e_rps

    # pred
    cmd += " %s" % i_log2_parallel_merge_level
    cmd += " %s" % b_slice_temporal_mvp_enabled
    cmd += " %s" % b_constrained_intra_pred

    # analyze
    cmd += " %s" % me_method
    cmd += " %s" % i_me_range
    cmd += " %s" % i_subpel_refine
    cmd += " %s" % b_chroma_me

    # rc
    cmd += " %s" % f_rate_tolerance
    cmd += " %s" % f_rf_constant
    cmd += " %s" % i_qp_min
    cmd += " %s" % i_qp_max
    cmd += " %s" % i_qp_step
    cmd += " %s" % f_ip_factor
    cmd += " %s" % f_pb_factor
    cmd += " %s" % i_aq_mode
    cmd += " %s" % f_aq_strength
    cmd += " %s" % i_lookahead
    cmd += " %s" % b_cutree
    cmd += " %s" % i_lowres
    cmd += " %s" % i_pass

    print cmd
    os.system(cmd)
  
