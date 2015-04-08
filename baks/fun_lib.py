
def get_reso_info(seq_name):
    tmp_list=seq_name.split('_')
    reso=tmp_list[1].split('x')
    reso.append(tmp_list[2])
    return reso

def get_bitrate_for_rc(eRcType,nSrcWidth,nSrcHeight,fFrameRate):
    nBitrate=0
    nMaxBitrate=0
    vbv_buffer_size=0
    reso=str(nSrcWidth)+"x"+str(nSrcHeight)
    if reso == "2560x1600" :
      base_rate=3200
    elif reso == "1920x1080" :
      base_rate=1500
    elif reso == "1280x720"  : 
      base_rate=600
    elif reso== "1024x768"  :
      base_rate=568
    elif reso== "832x480"   :
      base_rate=300
    elif reso== "416x240"   :
      base_rate=75
    elif reso== "640x480"   :
      base_rate=222
    elif reso== "352x288"   :
      base_rate=73
    elif reso== "448x336"   :
      base_rate=110

    brate=fFrameRate*base_rate/30
    factor=2
    nBitrate=brate*factor
    # CBR
    if eRcType == "CBR":
        nMaxBitrate=nBitrate
        vbv_buffer_size=1*nBitrate

    # VBR
    if eRcType == "VBR":
        nMaxBitrate=3*nBitrate
        vbv_buffer_size=1*nMaxBitrate

    info=[nBitrate,nMaxBitrate,vbv_buffer_size]
    return info

