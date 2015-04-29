import os.path
def get_param_cmd_x26x(param_list):
  cmd=""

  cmd += " --seek %s"% param_list['first_frame']
  cmd += " --rc-lookahead %s" % param_list['rc_i_lookahead']
  cmd += " -b %s" % param_list['nBframe']
  cmd += " --ref %s" % param_list['nMaxRefNum']
  cmd += " --aq-mode %s" % param_list['rc_i_aq_mode']
  # cmd+=" %s" % param_list['{bpyr_cl[%s" % param_list['bExistRefB]}']
  #cmd+=" %s" % param_list['{mbtree_cl[%s" % param_list['rc_b_cutree]}']

  if param_list['eRcType'] == 0 or param_list['eRcType'] == 9:
    cmd += " --qp %s" % param_list['nQp']
    if param_list['eRcType'] == 0:
      cmd += " --ipratio 1.0"
      cmd += " --pbratio 1.0"
  else:
    cmd += " --bitrate %s" % param_list['nBitrate']
    cmd += " --vbv-maxrate %s" % param_list['nMaxBitrate']
    cmd += " --vbv-bufsize %s" % param_list['vbv_buffer_size']
    if param_list['vbv_buffer_init_time'] > 0:
      vbv_buffer_init = param_list['vbv_buffer_init_time'] / 1000 * param_list['nMaxBitrate'] / param_list['vbv_buffer_size']
    else:
      vbv_buffer_init = 0.9
    cmd += " --vbv-init %s" % vbv_buffer_init

  cmd += " --pass %s" % param_list['rc_i_pass']

  cmd += " -o %s %s" % (os.path.join(param_list['output_path'],param_list['output_filename']), os.path.join(param_list['input_path'], param_list['input_filename']))
  cmd += " --input-res %sx%s" % (param_list['nSrcWidth'], param_list['nSrcHeight'])
  cmd += " --fps %s" % param_list['fFrameRate']
  cmd += " -I %s" % param_list['nIntraPicInterval']
  cmd += " --frames %s" % param_list['frame_num_to_encode']
  cmd += " --scenecut %s" % param_list['i_scenecut_threshold']
  cmd += " --b-adapt %s" % param_list['i_bframe_adaptive']

  asm_cl=("--no-asm","--asm auto")
  cmd += " %s" % asm_cl[param_list['b_asm']]

  me_cl = ("dia", "hex", "umh", "esa", "tesa")
  cmd += " --me %s" % me_cl[param_list['me_method']]
  cmd += " --merange %s" % param_list['i_me_range']
  cmd += " --subme %s" % param_list['i_subpel_refine']

  #cmd+=" --tune psnr"
  cmd += " --psnr"
  cmd += " --ssim"
  cmd += " --no-progress"
  cmd += "  --log-level debug"

  return cmd

def get_param_cmd_x265(param_list):
  cmd=""
  cmd += " --frame-threads %s" % param_list['frame_threads']
  if param_list['wpp_threads'] < param_list['lookahead_threads']:
    param_list['wpp_threads'] = param_list['lookahead_threads']
  cmd += " --pool %s"%param_list['wpp_threads']
  #cmd += " --threads %s"%param_list['wpp_threads']
  if param_list['wpp_threads'] > 1 or param_list['vbv_buffer_size']>0:#VBV requires wave-front parallelism
    cmd += " --wpp"
  else:
    cmd += " --no-wpp"

  cmd += " --lookahead-slices %s" % param_list['lookahead_threads']

  bpyr_cl = ("--no-b-pyramid", "--b-pyramid")
  mbtree_cl = ("--no-cutree", "--cutree")

  cmd += " %s" % bpyr_cl[param_list['bExistRefB']]
  cmd += " %s" % mbtree_cl[param_list['rc_b_cutree']]

  cmd += " --no-weightp"
  cmd += " --info"

  tmp_flag = param_list['trace_flag'] & 2
  if tmp_flag == 2:
    cmd += " --recon %s" % os.path.join(param_list['output_path'],param_list['dump_file_rec'])

  cmd += " --no-signhide"

  sao_cl = ("--no-sao", "--sao")
  cmd += " %s" % sao_cl[param_list['b_sao']]

  amp_cl = ("--no-amp", "--amp")
  cmd += " %s" % amp_cl[param_list['b_amp']]

  headers = ("--no-repeat-headers", "--repeat-headers")
  cmd += " %s" % headers[param_list['b_repeat_headers']]

  gop_cl=("--no-open-gop","--open-gop")
  cmd +=" %s" % gop_cl[param_list['b_open_gop']]

  cmd +=" --ctu %s"% param_list["nMaxCUSize"]
  cmd += " --min-cu-size %s" % (param_list["nMaxCUSize"]>>(param_list['nMaxCUDepth']-1))
  cmd += " --max-tu-size %s" % (1<<param_list['nQuadtreeTULog2MaxSize'])
  cmd += " --tu-intra-depth %s" % param_list['nQuadtreeTUMaxDepthIntra']
  cmd += " --tu-inter-depth %s" % param_list['nQuadtreeTUMaxDepthInter']

  cmd += get_param_cmd_x26x(param_list)

  return cmd

def get_param_cmd_x264(param_list):
  cmd = ""
  cmd += " --threads %s" % param_list['frame_threads']
  cmd += " --lookahead-threads %s" % param_list['lookahead_threads']

  bpyr_cl = ("--b-pyramid none", "--b-pyramid strict")
  mbtree_cl = ("--no-mbtree", "--mbtree")

  cmd += " %s" % bpyr_cl[param_list['bExistRefB']]
  cmd += " %s" % mbtree_cl[param_list['rc_b_cutree']]

  cmd += " --weightp 0"
  cmd += " --no-psy"

  if param_list['eRcType'] == 1:
    cmd += " --nal-hrd cbr"
  elif param_list['eRcType'] == 3:
    cmd += " --nal-hrd vbr"

  tmp_flag = param_list['trace_flag'] & 2
  if tmp_flag == 2:
    cmd += " --dump-yuv %s" % os.path.join(param_list['output_path'],param_list['dump_file_rec'])

  headers = ("--global-header", "--repeat-headers")
  cmd += " %s" % headers[param_list['b_repeat_headers']]

  if param_list['b_open_gop']==1:
    cmd +=" --open-gop"

  cmd += get_param_cmd_x26x(param_list)
  return cmd
