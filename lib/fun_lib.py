import sys
import global_vars
def get_reso_info(seq_name):
  common_reso_list=('176x144','352x288','416x240','832x480','1024x768',
                    '1280x720','1920x1080','2560x1600','3840x2160',
                    '640x480','448x336','720x576')
  common_fps_list=(15,20,23,24,25,30,50,60)
  #seq_name format: name_widthxheight_fps or
  #                 name_widthxheight_bitdepth_fps_totalframes
  tmp_list = seq_name.split('_')
  if tmp_list[1] not in common_reso_list:
    print "maybe the resolution is invalid, please check"
    sys.exit()
  reso = tmp_list[1].split('x')
  width = int(reso[0])
  height = int(reso[1])
  #if len(tmp_list)==3:
  #  fps=int(tmp_list[2])
  #elif len(tmp_list)==5:
  #  fps= int(tmp_list[3])
  #else:
  #  fps=30 #default fps
  fps=int(tmp_list[2])
  if fps<15:
    if len(tmp_list)==5:
      fps=int(tmp_list[3])
    else:
      fps=30 #default fps
  if fps not in common_fps_list:
    print "maybe the fps is invalid, please check"
    sys.exit()
  return (width, height, fps)


def get_bitrate_for_rc(eRcType, nSrcWidth, nSrcHeight, fFrameRate, factor=2):
  # nBitrate=0
  #rc_methods=["FQ","CBR","QUALITY_RANK","VBR","CONFERENCE","VBR_TWOPASS_ANALYSE","VBR_TWOPASS_ENC","VBR_Q","ABR","CQP","CRF"]
  #rc_type=rc_methods[eRcType]

  reso = str(nSrcWidth) + "x" + str(nSrcHeight)
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

  brate = fFrameRate * base_rate / 30
  nBitrate = brate * factor
  nMaxBitrate = 0
  vbv_buffer_size = 0

  if eRcType != global_vars.HEVC_RC_ABR :  #not ABR or ABR-2
    if eRcType == global_vars.HEVC_RC_CBR:  #CBR
      nMaxBitrate = nBitrate
    elif eRcType == global_vars.HEVC_RC_VBR:#"VBR":
      nMaxBitrate = 3 * nBitrate
    vbv_buffer_size = 1 * nMaxBitrate

  return (nBitrate, nMaxBitrate, vbv_buffer_size)

