def get_reso_info(seq_name):
    tmp_list = seq_name.split('_')
    reso = tmp_list[1].split('x')
    reso.append(tmp_list[2])
    return reso


def get_bitrate_for_rc(e_rctype, i_src_width, i_src_height, f_framerate):
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

    brate = f_framerate * base_rate / 30
    factor = 2
    i_bitrate = brate * factor
    # CBR
    if e_rctype == "CBR":
        i_max_bitrate = i_bitrate
        i_buffer_size = 1 * i_bitrate

    # VBR
    if e_rctype == "VBR":
        i_max_bitrate = 3 * i_bitrate
        i_buffer_size = 1 * i_max_bitrate

    info = [i_bitrate, i_max_bitrate, i_buffer_size]
    return info

