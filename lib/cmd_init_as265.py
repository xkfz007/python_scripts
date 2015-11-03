import common_lib


def get_default_enc_param_list():
    param_list = {}  # dict()  # create a dictinary
    param_list['output_path'] = "."  # "F:/encoder_test_output/as265_output  "
    param_list['output_filename'] = "as265_str.bin"
    param_list['input_path'] = "f:/sequences/"
    param_list['input_filename'] = "BlowingBubbles_416x240_50.yuv"

    param_list['trace_file_cabac'] = "trace_file_cabac.log"
    param_list['trace_file_general'] = "trace_file_general.log"
    param_list['dump_file_rec'] = "dump_file_rec.log"
    param_list['trace_file_prd_y'] = "trace_file_prd_y.log"
    param_list['trace_file_prd_uv'] = "trace_file_prd_uv.log"
    param_list['trace_file_cabacrdo'] = "trace_file_cabacrdo.log"
    param_list['trace_file_arch1rdo'] = "trace_file_arch1rdo.log"

    param_list['i_src_width'] = 416
    param_list['i_src_height'] = 240
    param_list['f_framerate'] = 0

    # debug related paramters
    param_list['i_printf_flag'] = 1  # 225
    param_list['i_trace_flag'] = 0  # 7
    param_list['b_measure_quality'] = 1

    param_list['i_frame_num_to_encode'] = 0

    # cu pu tu
    param_list['i_max_cuwidth'] = 6 #log2width
    param_list['i_max_cudepth'] = 4
    param_list['i_max_tulog2width'] = 5
    param_list['i_min_tulog2width'] = 2
    param_list['i_max_intra_tudepth'] = 1
    param_list['i_min_inter_tudepth'] = 1

    # gop
    param_list['i_keyint'] = 350
    param_list['i_maxref'] = 1
    param_list['b_bframe_pyramid'] = 1
    param_list['i_bframe'] = 3
    param_list['b_multiple_sublayer'] = 0
    param_list['i_decoding_refresh_type'] = 2

    param_list['b_open_gop'] = 1
    param_list['i_scenecut_threshold'] = 40
    param_list['i_bframe_adaptive'] = 0

    #feature
    param_list['i_merge'] = 5
    param_list['b_pintra'] = 1
    param_list['b_bintra'] = 0
    param_list['b_rect'] = 1
    param_list['b_amp'] = 0
    param_list['b_dbl'] = 1
    param_list['b_sao'] = 0

    param_list['b_tskip'] = 0
    param_list['b_tskip_fast'] = 0
    param_list['b_weightp'] = 0
    param_list['b_weightb'] = 0
    param_list['b_signhide'] = 0
    param_list['b_pcm'] = 0

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
    param_list['b_arcvideo'] = 0

    #asm
    param_list['b_asm'] = 0

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

    # stream
    param_list['i_interlace_mode'] = 0
    param_list['b_repeat_headers'] = 0
    param_list['b_enable_access_unit_delimiters'] = 0
    param_list['b_emit_hrd_sei'] = 0
    param_list['b_emit_info_sei'] = 1
    param_list['i_decoded_picture_hash_sei'] = 0

    param_list['f_rate_tolerance'] = 1.0
    param_list['f_rf_constant'] = 28
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
    #param_list['rc_s_stats'] = "as265_2pass.log"

    return param_list


def get_enc_param_cmd_as265(param_list):
    cmd = ""
    cmd += ' "%s"' % param_list['output_path']
    cmd += ' "%s"' % param_list['output_filename']
    cmd += ' "%s"' % param_list['input_path']
    cmd += ' "%s"' % param_list['input_filename']

    cmd += ' "%s"' % param_list['trace_file_cabac']
    cmd += ' "%s"' % param_list['trace_file_general']
    cmd += ' "%s"' % param_list['dump_file_rec']
    cmd += ' "%s"' % param_list['trace_file_prd_y']
    cmd += ' "%s"' % param_list['trace_file_prd_uv']
    cmd += ' "%s"' % param_list['trace_file_cabacrdo']
    cmd += ' "%s"' % param_list['trace_file_arch1rdo']

    cmd += " %s" % param_list['i_printf_flag']
    cmd += " %s" % param_list['i_trace_flag']
    cmd += " %s" % param_list['b_measure_quality']

    cmd += " %s" % param_list['i_src_width']
    cmd += " %s" % param_list['i_src_height']
    cmd += " %s" % param_list['f_framerate']
    cmd += " %s" % param_list['i_frame_num_to_encode']

    # cu pu tu
    #tmp_power = {64: 6, 32: 5, 16: 4, 8: 3, 4: 2}
    #cmd += " %s" % tmp_power[param_list['i_max_cuwidth']]
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
    cmd += " %s" % param_list['i_merge']
    cmd += " %s" % param_list['b_pintra']
    cmd += " %s" % param_list['b_bintra']
    cmd += " %s" % param_list['b_rect']
    cmd += " %s" % param_list['b_amp']
    cmd += " %s" % param_list['b_dbl']
    cmd += " %s" % param_list['b_sao']

    cmd += " %s" % param_list['b_tskip']
    cmd += " %s" % param_list['b_tskip_fast']
    cmd += " %s" % param_list['b_weightp']
    cmd += " %s" % param_list['b_weightb']
    cmd += " %s" % param_list['b_signhide']
    cmd += " %s" % param_list['b_pcm']

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
    cmd += " %s" % param_list['me_method']  # 0:dia 1:hex 2:umh(not yet) 9:full
    cmd += " %s" % param_list['i_me_range']
    cmd += " %s" % param_list['i_subpel_refine']
    cmd += " %s" % param_list['b_chroma_me']

    # stream
    cmd += " %s" % param_list['i_interlace_mode']
    cmd += " %s" % param_list['b_repeat_headers']
    cmd += " %s" % param_list['b_enable_access_unit_delimiters']
    cmd += " %s" % param_list['b_emit_hrd_sei']
    cmd += " %s" % param_list['b_emit_info_sei']
    cmd += " %s" % param_list['i_decoded_picture_hash_sei']

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
    # cmd += " %s" % param_list['rc_s_stats']

    return cmd

