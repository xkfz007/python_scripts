import common_lib


def get_default_enc_param_list():
    param_list = {}  # dict()  # create a dictinary
    # param_list['encder_exe'] = "cli_ashevc.exe"
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

    param_list['nSrcWidth'] = 416
    param_list['nSrcHeight'] = 240
    param_list['fFrameRate'] = 50

    # debug related paramters
    param_list['printf_flag'] = 1  # 225
    param_list['trace_flag'] = 0  # 7
    param_list['measure_quality_flag'] = 1

    param_list['frame_num_to_encode'] = -1

    # cu pu tu
    param_list['nMaxCUSize'] = 64
    param_list['nMaxCUDepth'] = 4
    param_list['nQuadtreeTULog2MaxSize'] = 5
    param_list['nQuadtreeTULog2MinSize'] = 2
    param_list['nQuadtreeTUMaxDepthIntra'] = 1
    param_list['nQuadtreeTUMaxDepthInter'] = 1

    # gop
    param_list['nIntraPicInterval'] = 350
    param_list['nMaxRefNum'] = 1
    param_list['bExistRefB'] = 0
    param_list['nBframe'] = 0
    param_list['bEnableMultipleSubLayer'] = 0
    param_list['DecodingRefreshType'] = 2

    param_list['b_open_gop'] = 0
    param_list['i_scenecut_threshold'] = 0
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
    param_list['eRcType'] = 0
    param_list['nQp'] = 33
    param_list['nBitrate'] = 0
    param_list['nMaxBitrate'] = 0
    param_list['vbv_buffer_size'] = 0
    param_list['vbv_buffer_init_time'] = 0

    #preset
    param_list['preset'] = 5

    #debug parameters
    param_list['first_frame'] = 0
    param_list['random_cost'] = 0
    param_list['force_tu_split'] = 0
    param_list['force_one_intra_mode'] = 0
    param_list['b_enable_cfg'] = 0

    #asm
    param_list['b_asm'] = 0

    #architecture and algorithm
    param_list['architecture_id'] = 2
    param_list['algorithm_suit_id'] = 0

    param_list['frame_threads'] = 1
    param_list['wpp_threads'] = 1
    param_list['lookahead_threads'] = 1

    param_list['rps_method'] = 1

    param_list['log2_parallel_merge_level'] = 2
    param_list['slice_temporal_mvp_enabled_flag'] = 1
    param_list['constrained_intra_pred_flag'] = 0

    param_list['me_method'] = 1
    param_list['i_me_range'] = 32
    param_list['i_subpel_refine'] = 5
    param_list['b_chroma_me'] = 1

    # stream
    param_list['iInterlaceMode'] = 0
    param_list['b_repeat_headers'] = 0
    param_list['bEnableAccessUnitDelimiters'] = 0
    param_list['bEmitHRDSEI'] = 1
    param_list['bEmitInfoSEI'] = 1
    param_list['iDecodedPictureHashSEI'] = 0

    param_list['rc_f_rate_tolerance'] = 1.0
    param_list['rc_f_rf_constant'] = 23
    param_list['rc_i_qp_min'] = 0
    param_list['rc_i_qp_max'] = 51
    param_list['rc_i_qp_step'] = 4
    param_list['rc_f_ip_factor'] = 1.4
    param_list['rc_f_pb_factor'] = 1.3
    param_list['rc_i_aq_mode'] = 0
    param_list['rc_f_aq_strength'] = 1.0
    param_list['rc_i_lookahead'] = 10
    param_list['rc_b_cutree'] = 0
    param_list['rc_i_lowres'] = 1
    param_list['rc_i_pass'] = 0
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

    cmd += " %s" % param_list['printf_flag']
    cmd += " %s" % param_list['trace_flag']
    cmd += " %s" % param_list['measure_quality_flag']

    cmd += " %s" % param_list['nSrcWidth']
    cmd += " %s" % param_list['nSrcHeight']
    cmd += " %s" % param_list['fFrameRate']
    cmd += " %s" % param_list['frame_num_to_encode']

    # cu pu tu
    tmp_power = {64: 6, 32: 5, 16: 4, 8: 3, 4: 2}
    cmd += " %s" % tmp_power[param_list['nMaxCUSize']]
    cmd += " %s" % param_list['nMaxCUDepth']
    cmd += " %s" % param_list['nQuadtreeTULog2MaxSize']
    cmd += " %s" % param_list['nQuadtreeTULog2MinSize']
    cmd += " %s" % param_list['nQuadtreeTUMaxDepthIntra']
    cmd += " %s" % param_list['nQuadtreeTUMaxDepthInter']

    # gop
    cmd += " %s" % param_list['nIntraPicInterval']
    cmd += " %s" % param_list['nMaxRefNum']
    cmd += " %s" % param_list['bExistRefB']
    cmd += " %s" % param_list['nBframe']
    cmd += " %s" % param_list['bEnableMultipleSubLayer']
    cmd += " %s" % param_list['DecodingRefreshType']

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
    cmd += " %s" % param_list['eRcType']
    cmd += " %s" % param_list['nQp']
    cmd += " %s" % param_list['nBitrate']
    cmd += " %s" % param_list['nMaxBitrate']
    cmd += " %s" % param_list['vbv_buffer_size']
    cmd += " %s" % param_list['vbv_buffer_init_time']

    # preset
    cmd += " %s" % param_list['preset']

    # debug ters
    cmd += " %s" % param_list['first_frame']
    cmd += " %s" % param_list['random_cost']
    cmd += " %s" % param_list['force_tu_split']
    cmd += " %s" % param_list['force_one_intra_mode']

    cmd += " %s" % param_list['b_enable_cfg']

    # asm
    cmd += " %s" % param_list['b_asm']

    # architecture and algorithm
    cmd += " %s" % param_list['architecture_id']
    cmd += " %s" % param_list['algorithm_suit_id']

    # threading
    cmd += " %s" % param_list['frame_threads']
    cmd += " %s" % param_list['wpp_threads']
    cmd += " %s" % param_list['lookahead_threads']

    # rps
    cmd += " %s" % param_list['rps_method']

    # pred
    cmd += " %s" % param_list['log2_parallel_merge_level']
    cmd += " %s" % param_list['slice_temporal_mvp_enabled_flag']
    cmd += " %s" % param_list['constrained_intra_pred_flag']

    # analyze
    cmd += " %s" % param_list['me_method']  # 0:dia 1:hex 2:umh(not yet) 9:full
    cmd += " %s" % param_list['i_me_range']
    cmd += " %s" % param_list['i_subpel_refine']
    cmd += " %s" % param_list['b_chroma_me']

    # stream
    cmd += " %s" % param_list['iInterlaceMode']
    cmd += " %s" % param_list['b_repeat_headers']
    cmd += " %s" % param_list['bEnableAccessUnitDelimiters']
    cmd += " %s" % param_list['bEmitHRDSEI']
    cmd += " %s" % param_list['bEmitInfoSEI']
    cmd += " %s" % param_list['iDecodedPictureHashSEI']

    # rc
    cmd += " %s" % param_list['rc_f_rate_tolerance']
    cmd += " %s" % param_list['rc_f_rf_constant']
    cmd += " %s" % param_list['rc_i_qp_min']
    cmd += " %s" % param_list['rc_i_qp_max']
    cmd += " %s" % param_list['rc_i_qp_step']
    cmd += " %s" % param_list['rc_f_ip_factor']
    cmd += " %s" % param_list['rc_f_pb_factor']
    cmd += " %s" % param_list['rc_i_aq_mode']
    cmd += " %s" % param_list['rc_f_aq_strength']
    cmd += " %s" % param_list['rc_i_lookahead']
    cmd += " %s" % param_list['rc_b_cutree']
    cmd += " %s" % param_list['rc_i_lowres']
    cmd += " %s" % param_list['rc_i_pass']
    # cmd += " %s" % param_list['rc_s_stats']

    return cmd

