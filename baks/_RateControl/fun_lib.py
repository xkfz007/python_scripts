def get_reso_info(seq_name):
    tmp_list = seq_name.split('_')
    reso = tmp_list[1].split('x')
    width = reso[0]
    height = reso[1]
    fps = tmp_list[-1]
    return (width, height, fps)


def get_reso_info2(seq_name):
    tmp_list = seq_name.split('_')
    reso = tmp_list[1].split('x')
    reso.append(tmp_list[3])
    return reso


def get_bitrate_for_rc(e_rctype, i_src_width, i_src_height, f_framerate, factor=2):
    i_bitrate = 0
    i_max_bitrate = 0
    i_buffer_size = 0
    reso = str(i_src_width) + "x" + str(i_src_height)
    if reso == "2560x1600":
        base_rate = 3200
    elif reso == "1920x1080":
        base_rate = 1500
    elif reso == "1280x720":
        base_rate = 600
    elif reso == "1024x768":
        base_rate = 568
    elif reso == "832x480":
        base_rate = 300
    elif reso == "416x240":
        base_rate = 75
    elif reso == "640x480":
        base_rate = 222
    elif reso == "352x288":
        base_rate = 73
    elif reso == "448x336":
        base_rate = 110
    elif reso == "3840x2160":
        base_rate = 8000
    else:
        base_rate = 5000

    fps = f_framerate
    brate = fps * base_rate / 30
    i_bitrate = brate * factor
    rc_methods = ["CQP", "CBR", "QUALITY_RANK", "VBR", "CONFERENCE", "VBR_TWOPASS_ANALYSE", "VBR_TWOPASS_ENC", "VBR_Q",
                  "ABR"]
    rc_type = rc_methods[e_rctype]
    # CBR
    if rc_type == "CBR":
        i_max_bitrate = i_bitrate
        i_buffer_size = 1 * i_bitrate

    # VBR
    if rc_type == "VBR":
        i_max_bitrate = 3 * i_bitrate
        i_buffer_size = 1 * i_max_bitrate

    return (i_bitrate, i_max_bitrate, i_buffer_size)


def init_param_list_default():
    param_list = dict()  # create a dictinary
    param_list['encder_exe'] = "cli_ashevc.exe"
    param_list['output_path'] = "f:\\hfz\\_HD-User_D_TEMP\\_Video_data_temp\\_Regression_Temp\\"
    param_list['output_filename'] = "as265_str.bin"
    param_list['input_path'] = "E:\\_HD-User_H_DATA\\z_Const_Data__TestResource\\_Video_data_const_hd\\"
    param_list['input_filename'] = "foreman.yuv"

    param_list['trace_file_cabac'] = "trace_file_cabac.log"
    param_list['trace_file_general'] = "trace_file_general.log"
    param_list['dump_file_rec'] = "dump_file_rec.log"
    param_list['trace_file_prd_y'] = "trace_file_prd_y.log"
    param_list['trace_file_prd_uv'] = "trace_file_prd_uv.log"
    param_list['trace_file_cabacrdo'] = "trace_file_cabacrdo.log"
    param_list['trace_file_arch1rdo'] = "trace_file_arch1rdo.log"

    # debug related paramters
    param_list['printf_flag'] = 0  #225
    param_list['trace_flag'] = 0  #7
    param_list['measure_quality_flag'] = 0

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
    param_list['e_rctype'] = 0
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

    return param_list


def get_cmd_line(param_list):
    cmd = param_list['encder_exe']
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

    # i_preset
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

    return cmd


def set_seq_related_param(param_list, seq_name):
    reso_info = get_reso_info(seq_name)
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
    return


def set_rc_related_param_auto(param_list, factor):
    rc_param = get_bitrate_for_rc(param_list['e_rctype'], param_list['i_src_width'], param_list['i_src_height'],
                                  param_list['f_framerate'], factor)
    param_list['i_bitrate'] = rc_param[0]
    param_list['i_max_bitrate'] = rc_param[1]
    param_list['i_buffer_size'] = rc_param[2]
    return;


def set_rc_related_param_manual(param_list, bitrate, vbv_maxrate, i_buffer_size):
    param_list['i_bitrate'] = bitrate
    param_list['i_max_bitrate'] = vbv_maxrate
    param_list['i_buffer_size'] = i_buffer_size
    if bitrate == 0:
        param_list['e_rctype'] = 0
    elif vbv_maxrate == 0 or i_buffer_size == 0:
        param_list['e_rctype'] = 8
    elif vbv_maxrate <= bitrate:
        param_list['e_rctype'] = 1
    else:
        param_list['e_rctype'] = 9

    return;

