import os.path


def get_enc_param_cmd_hm(param_list):
  SOP_listP = (
    'P 1 3 0.4624 0 0 0 4 4 -1 -5 -9 -13 0',
    'P 2 2 0.4624 0 0 0 4 4 -1 -2 -6 -10 1 -1 5 1 1 1 0 1',
    'P 3 3 0.4624 0 0 0 4 4 -1 -3 -7 -11 1 -1 5 0 1 1 1 1',
    'P 4 1 0.578  0 0 0 4 4 -1 -4 -8 -12 1 -1 5 0 1 1 1 1'
  )
  SOP_listB = (
    'B    1   3        0.4624   0            0               0           4                4         -1 -5 -9 -13       0',
    'B    2   2        0.4624   0            0               0           4                4         -1 -2 -6 -10       1      -1       5         1 1 1 0 1',
    'B    3   3        0.4624   0            0               0           4                4         -1 -3 -7 -11       1      -1       5         0 1 1 1 1 ',
    'B    4   1        0.578    0            0               0           4                4         -1 -4 -8 -12       1      -1       5         0 1 1 1 1'
  )
  SOP_listPB = (
    'P    4   1        0.578    0            0               0           1                1         -4                 0',
    'B    2   2        0.4624   1            0               1           1                2         -2  2              1       2       2         1 1',
    'B    1   3        0.4624   2            0               2           1                3         -1  1  3           1       1       3         1 1 1',
    'B    3   3        0.4624   2            0               2           1                2         -1  1              1      -2       4         0 1 1 0'
  )

  sop_size = 4
  sop_list = SOP_listP
  if param_list['nIntraPicInterval'] <= 1:
    sop_size = 1
  if param_list['nBframe'] >= 1:
    sop_size = 4
    sop_list = SOP_listPB
  if param_list['nBframe'] >= 1 and param_list['bExistRefB'] == 1:
    sop_size = 4
    sop_list = SOP_listB

  if param_list['nIntraPicInterval'] % sop_size != 0:
    param_list['nIntraPicInterval'] = int(param_list['nIntraPicInterval'] / sop_size) * sop_size

  cmd = ""
  cmd += ' --InputFile="%s"' % os.path.join(param_list['input_path'], param_list['input_filename'])
  cmd += " --InputBitDepth=8"
  cmd += " --InputBitDepthC=8"
  cmd += " --FrameRate=%s" % param_list['fFrameRate']
  cmd += " --FrameSkip=%s" % param_list['first_frame']
  cmd += " --SourceWidth=%s" % param_list['nSrcWidth']
  cmd += " --SourceHeight=%s" % param_list['nSrcHeight']
  cmd += " --FramesToBeEncoded=%s" % param_list['frame_num_to_encode']
  # cmd += " --Level=%s"%0
  cmd += ' --BitstreamFile="%s"' % os.path.join(param_list['output_path'], param_list['output_filename'])
  cmd += ' --ReconFile="%s"' % os.path.join(param_list['output_path'], param_list['dump_file_rec'])
  cmd += " --Profile=%s" % "main"

  cmd += " --MaxCUWidth=%s" % param_list['nMaxCUSize']
  cmd += " --MaxCUHeight=%s" % param_list['nMaxCUSize']
  cmd += " --MaxPartitionDepth=%s" % param_list['nMaxCUDepth']
  cmd += " --QuadtreeTULog2MaxSize=%s" % param_list['nQuadtreeTULog2MaxSize']
  cmd += " --QuadtreeTULog2MinSize=%s" % param_list['nQuadtreeTULog2MinSize']
  cmd += " --QuadtreeTUMaxDepthInter=%s" % param_list['nQuadtreeTUMaxDepthInter']
  cmd += " --QuadtreeTUMaxDepthIntra=%s" % param_list['nQuadtreeTUMaxDepthIntra']
  cmd += " --IntraPeriod=%s" % param_list['nIntraPicInterval']
  cmd += " --DecodingRefreshType=%s" % param_list['DecodingRefreshType']
  cmd += " --GOPSize=%s" % sop_size

  me_cl=('1','0')#0:full search 1:TZ search
  cmd += " --FastSearch=%s" % me_cl[param_list['me_method']]
  cmd += " --SearchRange=%s" % param_list['i_me_range']
  cmd += " --BipredSearchRange=%s" % 4
  cmd += " --HadamardME=%s" % 1
  cmd += " --FEN=%s" % 1
  cmd += " --FDM=%s" % 1

  cmd += " --QP=%s" % param_list['nQp']
  #cmd += " --MaxDeltaQP=%s"%0
  #cmd += " --MaxCuDQPDepth=%s"%0
  #cmd += " --DeltaQpRD=%s"%0
  cmd += " --RDOQ=%s" % 0
  cmd += " --RDOQTS=%s" % 0
  cmd += " --TransformSkip=%s" % 0
  cmd += " --TransformSkipFast=%s" % 0

  cmd += " --LoopFilterOffsetInPPS=%s" % 1
  cmd += " --LoopFilterDisable=%s" % int(not param_list['b_dbl'])
  #cmd += " --LoopFilterBetaOffset_div2=%s"%0
  #cmd += " --LoopFilterTcOffset_div2=%s"%0
  #cmd += " --DeblockingFilterMetric=%s"%0

  cmd += " --InternalBitDepth=%s" % 8

  cmd += " --AMP=%s" % param_list['b_amp']
  cmd += " --SAO=%s" % param_list['b_sao']
  cmd += " --SAOLcuBoundary=%s" % 0
  cmd += " --SAOLcuBasedOptimization=%s" % 0

  cmd += " --SliceMode=%s" % 0
  cmd += " --SliceArgument=%s" % 0
  cmd += " --LFCrossSliceBoundaryFlag=%s" % 0

  cmd += " --PCMEnabledFlag=%s" % param_list['b_pcm']
  #cmd += " --PCMLog2MaxSize=%s"%0
  #cmd += " --PCMLog2MinSize=%s"%0
  #cmd += " --PCMInputBitDepthFlag=%s"%0
  #cmd += " --PCMFilterDisableFlag=%s"%0

  cmd += " --WeightedPredP=%s" % param_list['b_weightp']
  cmd += " --TransformSkip=%s" % param_list['b_tskip']
  cmd += " --TransformSkipFast=%s" % param_list['b_tskip_fast']
  cmd += " --SignHideFlag=%s" % param_list['b_signhide']

  #cmd += " --TileUniformSpacing=%s" % 0
  #cmd += " --NumTileColumnsMinus1=%s"%0
  #cmd += " --TileColumnWidthArray=%s"%0
  #cmd += " --NumTileRowsMinus1=%s"%0
  #cmd += " --TileRowHeightArray=%s"%0
  #cmd += " --LFCrossTileBoundaryFlag=%s"%0

  cmd += " --WaveFrontSynchro=%s" % param_list['wpp_threads']

  #cmd += " --ScalingList=%s"%0
  #cmd += " --ScalingListFile=%s"%0

  #cmd += " --TransquantBypassEnableFlag=%s"%0
  #cmd += " --CUTransquantBypassFlagForce=%s"%0

  cmd += " --SEIDecodedPictureHash=%s"%param_list['bEnableAccessUnitDelimiters']

  cmd += " --RateControl=%s" % param_list['eRcType']
  cmd += " --TargetBitrate=%s" % param_list['nBitrate']
  cmd += " --KeepHierarchicalBit=%s" % 1
  cmd += " --LCULevelRateControl=%s" % 1
  cmd += " --RCLCUSeparateModel=%s" % 1
  cmd += " --InitialQP=%s" % 0
  cmd += " --RCForceIntraQP=%s" % 0

  if sop_size > 1:
    for i in range(0, sop_size):
      cmd += " --Frame%s=\"%s\"" % (i+1, sop_list[i])

  return cmd
