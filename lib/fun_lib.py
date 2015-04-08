def get_reso_info(seq_name):
  tmp_list = seq_name.split('_')
  reso = tmp_list[1].split('x')
  width = reso[0]
  height = reso[1]
  fps = tmp_list[2]
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

  if eRcType != 8:  #not ABR
    if eRcType == 1:  #CBR
      nMaxBitrate = nBitrate
    elif rc_type == "VBR":
      nMaxBitrate = 3 * nBitrate
    vbv_buffer_size = 1 * nMaxBitrate

  return (nBitrate, nMaxBitrate, vbv_buffer_size)

