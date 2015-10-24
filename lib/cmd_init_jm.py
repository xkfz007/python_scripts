#!/bin/python
__author__ = 'hfz2597'
import os.path


def get_enc_param_cmd_jm(param_list):
    cmd = ""
    # File Input/Output Related Parameters
    cmd += ' -p InputFile="%s"' % os.path.join(param_list['input_path'], param_list['input_filename'])
    cmd += " -p StartFrame=%s" % param_list['i_first_frame']
    cmd += " -p FramesToBeEncoded=%s" % param_list['i_frame_num_to_encode']
    cmd += " -p FrameRate=%s" % param_list['f_framerate']
    cmd += " -p SourceWidth=%s" % param_list['i_src_width']
    cmd += " -p SourceHeight=%s" % param_list['i_src_height']
    cmd += " -p YUVFormat=%s" % "1"
    cmd += " -p SourceBitDepthLuma=8"
    cmd += " -p SourceBitDepthChroma=8"
    cmd += ' -p OutputFile="%s"' % os.path.join(param_list['output_path'], param_list['output_filename'])
    cmd += ' -p ReconFile="%s"' % os.path.join(param_list['output_path'], param_list['dump_file_rec'])
    cmd += ' -p TraceFile="%s"' % os.path.join(param_list['output_path'], param_list['trace_file_general'])
    cmd += ' -p StatsFile="%s"' % os.path.join(param_list['output_path'], param_list['trace_file_cabac'])
    cmd += " -p ReportFrameStats=1"
    cmd += " -p DisplayEncParams=1"
    cmd += " -p Verbose=2"

    # Primary Control Parameters
    cmd += " -p ProfileIDC=100"
    cmd += " -p LevelIDC=40"
    cmd += " -p IntraPeriod=%s" % param_list['i_keyint']
    cmd += " -p EnableOpenGOP=%s" % param_list['b_open_gop']
    cmd += " -p NumberBFrames=%s" % param_list['i_bframe']
    cmd += " -p QPISlice=%s" % param_list['i_qp']
    cmd += " -p QPPSlice=%s" % param_list['i_qp']
    cmd += " -p QPBSlice=%s" % param_list['i_qp']

    cmd += " -p DisableSubpelME=0"
    cmd += " -p SearchRange=%s" % param_list['i_me_range']
    cmd += " -p NumberReferenceFrames=%s" % param_list['i_maxref']
    cmd += " -p HierarchicalCoding=%s" % param_list['b_bframe_pyramid']
    cmd += " -p SendAUD=%s" % param_list['b_enable_access_unit_delimiters']

    #cmd += " -p PSliceSkip=1"
    #cmd += " -p PSliceSearch16x16=1"
    #cmd += " -p PSliceSearch16x8=1"
    #cmd += " -p PSliceSearch8x16=1"
    #cmd += " -p PSliceSearch8x8=1"
    #cmd += " -p PSliceSearch8x4=1"
    #cmd += " -p PSliceSearch4x8=1"
    #cmd += " -p PSliceSearch4x4=1"
    #cmd += " -p BSliceDirect=1"
    #cmd += " -p BSliceSearch16x16=1"
    #cmd += " -p BSliceSearch16x8=1"
    #cmd += " -p BSliceSearch8x16=1"
    #cmd += " -p BSliceSearch8x8=1"
    #cmd += " -p BSliceSearch8x4=1"
    #cmd += " -p BSliceSearch4x8=1"
    #cmd += " -p BSliceSearch4x4=1"
    #cmd += " -p BiPredSearch16x16=1"
    #cmd += " -p BiPredSearch16x8=1"
    #cmd += " -p BiPredSearch8x16=1"
    #cmd += " -p BiPredSearch8x8=0"
    #cmd += " -p DisableIntra4x4=0"
    #cmd += " -p DisableIntra16x16=0"
    #cmd += " -p DisableIntraInInter=0"
    #cmd += " -p IntraDisableInterOnly=0"
    #cmd += " -p Intra4x4ParDisable=0"
    #cmd += " -p Intra4x4DiagDisable=0"
    #cmd += " -p Intra4x4DirDisable=0"
    #cmd += " -p Intra16x16ParDisable=0"
    #cmd += " -p Intra16x16PlaneDisable=0"
    #cmd += " -p ChromaIntraDisable=0"
    cmd += " -p EnableIPCM=1"
    cmd += " -p DFParametersFlag=0"

    cmd += " -p RDOptimization=0"
    cmd += " -p DistortionSSIM=0"
    cmd += " -p SSIMOverlapSize=8"
    cmd += " -p CtxAdptLagrangeMult=0"
    cmd += " -p UseRDOQuant=0"

    cmd += " -p SearchMode=%s" % param_list['me_method']
    # -1 = Full Search 0 = Fast Full Search (default) 1 = UMHexagon Search
    #  2 = Simplified UMHexagon Search   3 = Enhanced Predictive Zonal Search (EPZS)
    cmd += " -p WeightedPrediction=%s" % param_list['b_weightp']
    cmd += " -p WeightedBiprediction=%s" % param_list['b_weightb']

    cmd += " -p RateControlEnable=%s" % int(param_list['e_rctype'] != 0 and param_list['e_rctype'] != 9)
    cmd += " -p Bitrate=%s" % param_list['i_bitrate']
    cmd += " -p InitialQP=%s" % 0
    cmd += " -p BasicUnit=%s" % 0
    cmd += " -p ChannelType=%s" % 0
    cmd += " -p RCUpdateMode=%s" % 2
    # 0 = original JM rate control,
    # 1 = rate control that is applied to all frames regardless of the slice type,
    # 2 = original plus intelligent QP selection for I and B slices (including Hierarchical),
    # 3 = original + hybrid quadratic rate control for I and B slice using bit rate statistics
    cmd += " -p EnableVUISupport=%s" % 0
    cmd += " -p VUI_aspect_ratio_info_present_flag=%s" % 0
    cmd += " -p VUI_aspect_ratio_idc=%s" % 1
    cmd += " -p VUI_sar_width=%s" % 0
    cmd += " -p VUI_sar_height=%s" % 0

    return cmd






