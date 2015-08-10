#!/usr/bin/python
import fun_lib
import seq_list
import os

base_rate = {'2560x1600': 3200,
             '1920x1080': 1500,
             '1280x720': 600,
             '1024x768': 568,
             '832x480': 300,
             '416x240': 75,
             '640x480': 222,
             '352x288': 73,
             '448x336': 110
}

output_path = "f:/encoder_test_output/"
input_path = "e:/sequences/"

# debug related paramters
printf_flag = 1  #225
trace_flag = 1  #7
measure_quality_flag = 1

frame_num_to_encode = 100

#cu pu tu
nMaxCUSize = 64
nMaxCUDepth = 4
nQuadtreeTULog2MaxSize = 5
nQuadtreeTULog2MinSize = 2
nQuadtreeTUMaxDepthIntra = 3
nQuadtreeTUMaxDepthInter = 3

#gop
nIntraPicInterval = 30
nMaxRefNum = 1
bExistRefB = 0
nBframe = 0
bEnableMultipleSubLayer = 0
DecodingRefreshType = 2

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
eRcType = 1
nQp = 33
nBitrate = 0
nMaxBitrate = 0
vbv_buffer_size = 0
vbv_buffer_init_time = 0

#preset
preset = 5

#debug parameters
first_frame = 0
random_cost = 0
force_tu_split = 0
force_one_intra_mode = 0
b_enable_cfg = 1

#asm
b_asm = 1

#architecture and algorithm
architecture_id = 2
algorithm_suit_id = 0

frame_threads = 1
wpp_threads = 1
lookahead_threads = 1

rps_method = 1

log2_parallel_merge_level = 2
slice_temporal_mvp_enabled_flag = 1
constrained_intra_pred_flag = 0

me_method = 1
i_me_range = 32
i_subpel_refine = 5
b_chroma_me = 1

rc_f_rate_tolerance = 1.0
rc_f_rf_constant = 23
rc_i_qp_min = 0
rc_i_qp_max = 51
rc_i_qp_step = 4
rc_f_ip_factor = 1.4
rc_f_pb_factor = 1.3
rc_i_aq_mode = 0
rc_f_aq_strength = 1.0
rc_i_lookahead = 10
rc_b_cutree = 0
rc_i_lowres = 1
rc_i_pass = 0

for seq_name in seq_list.classC:
    reso_info = fun_lib.get_reso_info(seq_name)
    nSrcWidth = int(reso_info[0])
    nSrcHeight = int(reso_info[1])
    fFrameRate = int(reso_info[2])

    output_filename = seq_name + "_str.bin"
    input_filename = seq_name + ".yuv"
    trace_file_cabac = seq_name + "_cabac.log"
    trace_file_general = seq_name + "_general.log"
    dump_file_rec = seq_name + "_rec.yuv"
    trace_file_prd_y = seq_name + "_prdy.log"
    trace_file_prd_uv = seq_name + "_prduv.log"
    trace_file_cabacrdo = seq_name + "_cabacrdo.log"
    trace_file_arch1rdo = seq_name + "_arch1rdo.log"

    rc_param = fun_lib.get_bitrate_for_rc(rc_methods[eRcType], nSrcWidth, nSrcHeight, fFrameRate)
    nBitrate = rc_param[0]
    nMaxBitrate = rc_param[1]
    vbv_buffer_size = rc_param[2]

    cmd = "/cygdrive/d/workspace/arcsoft_codes/HEVC_Codec/HEVC_Encoder/bin/x64/Release_WithTrace/cli_ashevc.exe"

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

    cmd += " %s" % nSrcWidth
    cmd += " %s" % nSrcHeight
    cmd += " %s" % fFrameRate
    cmd += " %s" % frame_num_to_encode

    # cu pu tu
    cmd += " %s" % nMaxCUSize
    cmd += " %s" % nMaxCUDepth
    cmd += " %s" % nQuadtreeTULog2MaxSize
    cmd += " %s" % nQuadtreeTULog2MinSize
    cmd += " %s" % nQuadtreeTUMaxDepthIntra
    cmd += " %s" % nQuadtreeTUMaxDepthInter

    # gop
    cmd += " %s" % nIntraPicInterval
    cmd += " %s" % nMaxRefNum
    cmd += " %s" % bExistRefB
    cmd += " %s" % nBframe
    cmd += " %s" % bEnableMultipleSubLayer
    cmd += " %s" % DecodingRefreshType

    cmd += " %s" % b_open_gop
    cmd += " %s" % i_scenecut_threshold
    cmd += " %s" % i_bframe_adaptive

    # feature
    cmd += " %s" % b_amp
    cmd += " %s" % b_dbl
    cmd += " %s" % b_sao

    # rc
    cmd += " %s" % eRcType
    cmd += " %s" % nQp
    cmd += " %s" % nBitrate
    cmd += " %s" % nMaxBitrate
    cmd += " %s" % vbv_buffer_size
    cmd += " %s" % vbv_buffer_init_time

    #preset
    cmd += " %s" % preset

    # debug ters
    cmd += " %s" % first_frame
    cmd += " %s" % random_cost
    cmd += " %s" % force_tu_split
    cmd += " %s" % force_one_intra_mode

    cmd += " %s" % b_enable_cfg

    # asm
    cmd += " %s" % b_asm

    # architecture and algorithm
    cmd += " %s" % architecture_id
    cmd += " %s" % algorithm_suit_id

    # threading
    cmd += " %s" % frame_threads
    cmd += " %s" % wpp_threads
    cmd += " %s" % lookahead_threads

    # rps
    cmd += " %s" % rps_method

    # pred
    cmd += " %s" % log2_parallel_merge_level
    cmd += " %s" % slice_temporal_mvp_enabled_flag
    cmd += " %s" % constrained_intra_pred_flag

    # analyze
    cmd += " %s" % me_method
    cmd += " %s" % i_me_range
    cmd += " %s" % i_subpel_refine
    cmd += " %s" % b_chroma_me

    # rc
    cmd += " %s" % rc_f_rate_tolerance
    cmd += " %s" % rc_f_rf_constant
    cmd += " %s" % rc_i_qp_min
    cmd += " %s" % rc_i_qp_max
    cmd += " %s" % rc_i_qp_step
    cmd += " %s" % rc_f_ip_factor
    cmd += " %s" % rc_f_pb_factor
    cmd += " %s" % rc_i_aq_mode
    cmd += " %s" % rc_f_aq_strength
    cmd += " %s" % rc_i_lookahead
    cmd += " %s" % rc_b_cutree
    cmd += " %s" % rc_i_lowres
    cmd += " %s" % rc_i_pass

    print cmd
    os.system(cmd)
  
