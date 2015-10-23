import getopt, sys, os
import common_lib, cmd_init_as265, cmd_init_x26x, seq_list, cmd_init_hm, cmd_init_jm
import codec_cmd
import global_vars
import logging

class Encoder_st(codec_cmd.Codec_st):
    def __init__(self,id,executor,help,cmd_func,path):
        #codec_cmd.Codec_st.__init__(self,id,executor,help,version,cmd_func,path)
        super(Encoder_st,self).__init__(id,executor,help,cmd_func,path)
    def __str__(self):
        return "Encoder_st[id=%s,executor=%s,help=%s,path=%s,get_para_cmd=%s]"% \
               (self.id,self.executor,self.help,self.path,self.get_param_cmd)

common_path = 'd:/workspace/'
x265_path = "x265_v1.5_20150211"
if global_vars.x265_ver == "v1.6":
    x265_path = "x265_v1.6_20150403"
hevc_path = 'HEVC_Encoder'
as265_st=Encoder_st(global_vars.as265_name_list[0],'cli_ashevc.exe','',cmd_init_as265.get_enc_param_cmd_as265,
                    os.path.join(common_path, 'arcvideo_codes/HEVC_Codec/', hevc_path, 'bin/x64/Release_WithTrace')
                    )
x265_st=Encoder_st(global_vars.x265_name_list[0],'x265.exe','--log-level full --help',cmd_init_x26x.get_enc_param_cmd_x265,
                   os.path.join(common_path, 'src.x265/trunk/', x265_path, 'build/vc10-x86_64/Release')
                   )
x264_st=Encoder_st(global_vars.x264_name_list[0],'x264.exe','--fullhelp',cmd_init_x26x.get_enc_param_cmd_x264,
                   os.path.join(common_path, 'src.x264/trunk/x264-snapshot-20140915-2245/bin/x64/Release')
                   )
hm_st=Encoder_st(global_vars.hm_name_list[0],'hm.exe','--help',cmd_init_hm.get_enc_param_cmd_hm,
                 os.path.join(common_path, 'src.hm/trunk/hm-10.0/bin/vc10/x64/Release')
                )
jm_st=Encoder_st(global_vars.jm_name_list[0],'lencod.exe','-h',cmd_init_jm.get_enc_param_cmd_jm,
                 os.path.join(common_path, 'SRC.JM/trunk/jm18.5/bin/')
                )
enc_st_list={global_vars.as265_name_list[0]:as265_st,
             global_vars.x265_name_list[0]:x265_st,
             global_vars.x264_name_list[0]:x264_st,
             global_vars.hm_name_list[0]:hm_st,
             global_vars.jm_name_list[0]:jm_st
}

def get_enc_st(id):
    if id in global_vars.as265_name_list:
        id = global_vars.as265_name_list[0]
    elif id in global_vars.x265_name_list:
        id = global_vars.x265_name_list[0]
    elif id in global_vars.x264_name_list:
        id = global_vars.x264_name_list[0]
    elif id in global_vars.hm_name_list:
        id = global_vars.hm_name_list[0]
    elif id in global_vars.jm_name_list:
        id = global_vars.jm_name_list[0]
    else:
        id = 'as265'
    return enc_st_list[id]

class ENCODER(codec_cmd.CODEC):
    def __init__(self,id='as265'):
        #codec_cmd.CODEC.__init__(self,get_enc_st)
        super(ENCODER,self).__init__(get_enc_st)
        #codec_cmd.CODEC.set_id(self,id)
        self.set_id(id)
    def set_fullpath(self,fullpath):
        fpath, fname = os.path.split(fullpath)
        new_id=''
        if fname==as265_st.executor:
            new_id=as265_st.id
        elif fname==x265_st.executor:
            new_id=x265_st.id
        elif fname==x264_st.executor:
            new_id=x264_st.id
        elif fname==hm_st.executor:
            new_id=hm_st.id
        elif fname==jm_st.executor:
            new_id=jm_st.id
        if len(new_id)==0:
            logging.warning('Invaild path "%s", checking is needed'%fullpath)
            self.set_executor(fname)
            self.set_path(fpath)
        else:
            self.set_id(new_id)
            self.set_path(fpath)

    def __str__(self):
        return "ENCODER:%s"%self.cdec_st
    @staticmethod
    def SET_PATH(id,path):
        get_enc_st(id).set_path(path)
    @staticmethod
    def SET_EXECUTOR(id,executor):
        get_enc_st(id).set_executor(executor)


def configure_seq_param(param_list, tmp_name, tmp_width=-1, tmp_height=-1, tmp_fps=-1, tags=''):
    seq_name = seq_list.guess_seqname(tmp_name)
    org_width, org_height, org_fps = seq_list.get_reso_info(seq_name)
    #tmp_width=tmp_list['tmp_nSrcWidth']
    #tmp_height=tmp_list['tmp_nSrcHeight']
    if tmp_width <= 0:
        param_list['nSrcWidth'] = int(org_width)
    else:
        param_list['nSrcWidth'] = int(tmp_width)
    if tmp_height<= 0:
        param_list['nSrcHeight'] = int(org_height)
    else:
        param_list['nSrcHeight'] = int(tmp_height)
    if tmp_fps<= 0:
        param_list['fFrameRate'] = int(org_fps)
    else:
        param_list['fFrameRate'] = int(tmp_fps)

    if len(tags) >0:
        tags = "_" + tags
    param_list['input_filename'] = seq_name + ".yuv"
    param_list['output_filename'] = seq_name + tags + "_str.bin"
    param_list['trace_file_cabac'] = seq_name + tags + "_cabac.log"
    param_list['trace_file_general'] = seq_name + tags + "_general.log"
    param_list['dump_file_rec'] = seq_name + tags + "_rec.yuv"
    param_list['trace_file_prd_y'] = seq_name + tags + "_prdy.log"
    param_list['trace_file_prd_uv'] = seq_name + tags + "_prduv.log"
    param_list['trace_file_cabacrdo'] = seq_name + tags + "_cabacrdo.log"
    param_list['trace_file_arch1rdo'] = seq_name + tags + "_arch1rdo.log"

    return seq_name + tags + "_cons.log"


def set_rc_related_param_manual(param_list, bitrate, vbv_maxrate, vbv_buffer_size):
    param_list['nBitrate'] = bitrate
    param_list['nMaxBitrate'] = vbv_maxrate
    param_list['vbv_buffer_size'] = vbv_buffer_size
    #if bitrate == 0:
    #  param_list['eRcType'] = 0
    #elif vbv_maxrate == 0 or vbv_buffer_size == 0:
    #  param_list['eRcType'] = 8
    #elif vbv_maxrate <= bitrate:
    #  param_list['eRcType'] = 1
    #else:
    #  param_list['eRcType'] = 9

    return


def set_rc_related_param_auto(param_list, factor=2):
    #rc_param = fun_lib.get_bitrate_for_rc(param_list['eRcType'], param_list['nSrcWidth'], param_list['nSrcHeight'], param_list['fFrameRate'], factor)

    reso = '%sx%s' % (param_list['nSrcWidth'], param_list['nSrcHeight'])
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

    brate = param_list['fFrameRate'] * base_rate / 30
    nBitrate = brate * factor
    nMaxBitrate = 0
    vbv_buffer_size = 0

    if param_list['eRcType'] != global_vars.HEVC_RC_ABR:  #not ABR or ABR-2
        if param_list['eRcType'] == global_vars.HEVC_RC_CBR:  #CBR
            nMaxBitrate = nBitrate
        elif param_list['eRcType'] == global_vars.HEVC_RC_VBR:  #"VBR":
            nMaxBitrate = 3 * nBitrate
        vbv_buffer_size = 1 * nMaxBitrate
    #param_list['nBitrate'] = rc_param[0]
    #param_list['nMaxBitrate'] = rc_param[1]
    #param_list['vbv_buffer_size'] = rc_param[2]
    set_rc_related_param_manual(param_list, nBitrate, nMaxBitrate, vbv_buffer_size)
    return


def set_rc_related_param_semi_auto(param_list, bitrate):
    if bitrate <= 0:
        #param_list['eRcType']=0
        set_rc_related_param_auto(param_list)
        return
    if bitrate <= 1.0:
        bitrate *= param_list['nSrcWidth'] * param_list['nSrcHeight'] * param_list['fFrameRate'] / 1000
    bitrate = int(bitrate)
    vbv_maxrate = 0
    if param_list['eRcType'] == global_vars.HEVC_RC_CBR:  #1:
        vbv_maxrate = bitrate
    elif param_list['eRcType'] == global_vars.HEVC_RC_VBR:  #3:
        vbv_maxrate = 3 * bitrate
    vbv_bufsize = vbv_maxrate * 1
    set_rc_related_param_manual(param_list, bitrate, vbv_maxrate, vbv_bufsize)
    return


def usage():
    help_msg = '''Usage:cl_run_enc.py [option] [value]...
  options:
   -e <string> encoder name:as265,x265,x264,hm,jm
   -s <string> seqname
   -E <int>:<int>:<int> resolution width:height:fps
   -i <string> input_path
   -o <string> output_path
   -f <int1>:<int2>
      <int1>: frames to be encoded
      <int2>: I frame interval
   -T <int1>:<int2>:<int3> multi-threads
      <int1>: frame parallelism threads
      <int2>: WPP threads
      <int3>: Lookahead threads
   -r <int/string>:<int1>:<int2>:<int3>:<int4> rate control parameters
      <int/string>: rate control method
      <int1>:qp/bitrate
      <int2>:vbv_max_bitrate
      <int3>:vbv_buffer_size
      <int4>:vbv-init-time
   -R <string> ref number
   -b <int1>:<int2>:<int3> b-frame parameters
      <int1>: number of b-frame
      <int2>: bref/b-pyramid/hierarchical:0 disabled, 1 enabled
      <int3>: bframe adaptive, 0: disabled, 1: fast method, 2: trellis
   -c <integer> scenecut value
   -G <integer> open-gop:0 disabled, 1 enabled
   -y dump-yuv
   -C <string> extra command lines
   -O <integer> Lowres:0 auto, 1 semi, 2 quater
   -p <integer> rc pass: 0: single pass encoding,
                         1: 2pass encoding(including first pass and second pass)
                         2: 2pass encoding with clipping
                         3: first pass of 2pass encoding (only for x26x)
                         4: second pass of 2pass encoding (only for x26x)
   -g <string> the 2pass log file (not supported yet)
   -l <integer> number of lookahead frames
   -P <integer> qp step
   -a <integer> aq-mode:0 disabled, 1 Variance AQ, Auto-Variance AQ
   -A <integer> cu tree:0 disabled, 1 enabled
   -k <integer> seek frame
   -j <integer> sao: 0 disabled, 1 enabled
   -J <integer> deblock: 0 disabled, 1 enabled
   --path <string> set the encoder path
   --log print log
   '''
    print help_msg
    return


#def parse_arg(arg,delimiter,X='-1',Y='-1',Z='-1'):
#    cnt=arg.count(delimiter)
#    print 'arg=%s cnt=%s'%(arg,cnt)
#    x=''
#    y=''
#    z=''
#    if cnt>2:
#        logging.error('Invalid arg:%s'%arg)
#        sys.exit()
#    elif cnt>1:
#        x,y,z=arg.split(delimiter)
#    elif cnt>0:
#        x,y=arg.split(delimiter)
#    else:
#        x=arg
#    if len(x)>0:
#        X=x
#    if len(y)>0:
#        Y=y
#    if len(z)>0:
#        Z=z
#    return X,Y,Z

def parse_reso_fps(arg,width=-1,height=-1,fps=-1,delimiter=':'):
    n=3
    x,y,z=common_lib.parse_arg(arg,delimiter,n,str(width),str(height),str(fps))
    return int(x),int(y),int(z)
def parse_rc_param(arg,method=-1,qp_bitrate=-1,vbv_max_rate=-1,vbv_bufsize=-1,vbv_init_time=-1,delimiter=':'):
    n=5
    x,y,z,s,t=common_lib.parse_arg(arg,delimiter,n,str(method),str(qp_bitrate),str(vbv_max_rate),str(vbv_bufsize),str(vbv_init_time))
    method= get_rc_type(x)
    return int(method),int(y),int(z),int(s),int(t)

def parse_threads(arg,frame_threads=-1,wpp_threads=-1,lookahead_threads=-1,delimiter=':'):
    n=3
    x,y,z=common_lib.parse_arg(arg,delimiter,n,str(frame_threads),str(wpp_threads),str(lookahead_threads))
    return int(x),int(y),int(z)

def parse_encoder_arg(opt_list,arg,local_dict,delimiter=':'):
    n=len(local_dict)
    opts=list()
    vals=list()
    for (k,v) in local_dict.items():
        opts.append(k)
        vals.append(str(v))
    common_lib.parse_arg_internal(arg,delimiter,vals)

    for i in range(0,n):
        if int(vals[i])>=0:
            opt_list[opts[i]]=int(vals[i])


def parse_frame_num(opt_list,arg):
    local_dict={'frame_num_to_encode':-1,
                'nIntraPicInterval':-1,
                }
    parse_encoder_arg(opt_list,arg,local_dict)

def parse_bframe_param(opt_list,arg):
    #default parameter values
    bframe_num=-1
    bref=-1
    badaptive=-1
    delimiter=':'
    n=3
    x,y,z=common_lib.parse_arg(arg,delimiter,n,str(bframe_num),str(bref),str(badaptive))
    bframe_num=int(x)
    bref=int(y)
    badaptive=int(z)
    if bframe_num>=0:
        opt_list['nBframe'] = bframe_num
    if bref>=0:
        opt_list['bExistRefB'] = bref
    if badaptive>=0:
        opt_list['i_bframe_adaptive'] = badaptive


def get_tag(opt, arg):
    new_arg=arg.replace(':','x')
    str = opt[1:] + new_arg
    return str


def get_rc_type(arg):
    rc_type = 0
    if arg.isdigit():
        rc_type = int(arg)
    elif global_vars.RC_DICT.has_key(arg.upper()):
        rc_type = global_vars.RC_DICT[arg.upper()]
    return rc_type


def parse_enc_cl(enc):

    if len(sys.argv) == 1:
        usage()
        sys.exit()

    help=common_lib.HELP(usage,enc.get_exe())
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   'i:o:I:f:T:l:q:r:b:a:s:R:e:yC:O:p:P:A:E:c:G:k:j:J:'+help.get_opt(),
                                   ['path=','log'])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    except Exception, e:
        print e

    opt_list = {}  #dict()
    tag_str = ""
    #seq_name = ""
    #tmp_nBitrate = -1
    #tmp_nMaxBitrate = -1
    #tmp_vbv_buffer_size = -1

    #Help_flag = 0
    #Version_flag = 0
    Encoder_flag = 0
    Encoder_path=''

    for opt, arg in opts:
        if opt == "-e":
            #opt_list["encoder_id"] = arg
            enc.set_id(arg.strip())
            help.set_BIN(enc.get_exe())
            help.set_help(enc.get_help())
            Encoder_flag = 1
        elif opt == "-i":
            opt_list["input_path"] = arg
        elif opt == "-o":
            opt_list["output_path"] = arg
        elif opt == "-f":
            parse_frame_num(opt_list,arg)
            tag_str += get_tag(opt, arg)
        elif opt == "-T":
            tmp_value=parse_threads(arg)
            if int(tmp_value[0])>0:
                opt_list["frame_threads"] = int(tmp_value[0])
            if int(tmp_value[1])>0:
                opt_list["wpp_threads"] = int(tmp_value[1])
            if int(tmp_value[2])>0:
                opt_list["lookahead_threads"] = int(tmp_value[2])
            tag_str += get_tag(opt, arg)
        elif opt == "-l":
            opt_list["rc_i_lookahead"] = int(arg)
            tag_str += get_tag(opt, arg)
        elif opt == "-r":
            tmp_value=parse_rc_param(arg)
            if int(tmp_value[0])>=0:
                opt_list["eRcType"] = int(tmp_value[0])
            if opt_list['eRcType'] in (global_vars.HEVC_RC_FIXQUANT, global_vars.HEVC_RC_CQP):
                if int(tmp_value[1])>=0:
                    opt_list["nQp"] = int(tmp_value[1])
            else:
                if int(tmp_value[1])>=0:
                    opt_list['tmp_nBitrate'] = int(tmp_value[1])
                if opt_list['eRcType'] in (global_vars.HEVC_RC_CBR, global_vars.HEVC_RC_VBR):
                    if int(tmp_value[2])>=0:
                        opt_list['tmp_nMaxBitrate'] = int(tmp_value[2])
                    if int(tmp_value[3])>=0:
                        opt_list['tmp_vbv_buffer_size'] = int(tmp_value[3])
                    if int(tmp_value[4])>=0:
                        opt_list["vbv_buffer_init_time"] = int(tmp_value[4])
            tag_str += get_tag(opt, arg)
        elif opt == '-b':
            parse_bframe_param(opt_list,arg)
            tag_str += get_tag(opt, arg)
        elif opt == "-a":
            opt_list["rc_i_aq_mode"] = int(arg)
            tag_str += get_tag(opt, arg)
        elif opt == "-s":
            #seq_name = arg
            opt_list['seq_name'] = arg
        elif opt == "-R":
            opt_list["nMaxRefNum"] = int(arg)
            tag_str += get_tag(opt, arg)
        elif opt == "-y":
            opt_list["trace_flag"] |= 2
        elif opt == "-C":
            opt_list["extra_cls"] = arg
            tag_str += get_tag(opt, "")
        elif opt == "-O":
            opt_list["rc_i_lowres"] = int(arg)
            tag_str += get_tag(opt, arg)
        elif opt == "-p":
            opt_list["rc_i_pass"] = int(arg)
            tag_str += get_tag(opt, arg)
        elif opt == "-P":
            opt_list["rc_i_qp_step"] = int(arg)
            tag_str += get_tag(opt, arg)
        elif opt == "-A":
            opt_list["rc_b_cutree"] = int(arg)
            tag_str += get_tag(opt, arg)
        elif opt == "-E":
            tmp_width, tmp_height, tmp_fps = parse_reso_fps(arg)#arg.split('x')
            opt_list["tmp_nSrcWidth"] = int(tmp_width)
            opt_list["tmp_nSrcHeight"] = int(tmp_height)
            opt_list["tmp_fFrameRate"] = int(tmp_fps)
            tag_str += get_tag(opt, arg)
        elif opt == "-c":
            opt_list["i_scenecut_threshold"] = int(arg)
            tag_str += get_tag(opt, arg)
        elif opt == "-G":
            opt_list["b_open_gop"] = int(arg)
            tag_str += get_tag(opt, arg)
        elif opt in ("-k",):
            opt_list["first_frame"] = int(arg)
            tag_str += get_tag(opt, arg)
        elif opt in ("-j",):
            opt_list["b_sao"] = int(arg)
            tag_str += get_tag(opt, arg)
        elif opt in ("-J",):
            opt_list["b_dbl"] = int(arg)
            tag_str += get_tag(opt, arg)
        elif opt =='--path':
            Encoder_path=arg
            Encoder_flag=1
        elif opt =='--log':
            opt_list['log_print']=1
        else:
            help.parse_opt(opt)

    opt_list['do_execute']=help.get_do_execute()

    if len(Encoder_path)>0:
        if os.path.isdir(Encoder_path):
            enc.set_path(Encoder_path)
        elif os.path.isfile(Encoder_path):
            enc.set_fullpath(Encoder_path)

    #if Help_flag == 1:
    #    os.system(enc.get_help_exe())
    #    sys.exit()

    #if Version_flag == 1:
    #    os.system(enc.get_version_exe())
    #    sys.exit()

    if Encoder_flag == 1:
        if tag_str == "":
            tag_str = enc.get_id()
        else:
            tag_str = enc.get_id() + "_" + tag_str

    #return (opt_list, tag_str, seq_name, tmp_nBitrate, tmp_nMaxBitrate, tmp_vbv_buffer_size)
    return (opt_list, tag_str)


def remove_some_tmp_files(path):
    ext_list = (".bin", ".rcstat", ".pinfo", ".log")
    common_lib.delete_files(path, ext_list)


def check_files(param_list):
    #check the input file
    input_fullname = os.path.join(param_list['input_path'], param_list['input_filename'])
    if not os.path.exists(input_fullname):
        logging.error('Input file "%s" does not exist. Please check' % input_fullname)
        sys.exit()

    #check the outputfiles: if exists, delete it
    output_fullname = os.path.join(param_list['output_path'], param_list['output_filename'])
    if os.path.exists(output_fullname):
        os.remove(output_fullname)
        logging.info('Deleted output file: %s' % output_fullname)

    output_fullname = os.path.join(param_list['output_path'], param_list['trace_file_cabac'])
    if os.path.exists(output_fullname):
        os.remove(output_fullname)
        logging.info('Deleted output file: %s' % output_fullname)

    output_fullname = os.path.join(param_list['output_path'], param_list['trace_file_general'])
    if os.path.exists(output_fullname):
        os.remove(output_fullname)
        logging.info('Deleted output file: %s' % output_fullname)

    output_fullname = os.path.join(param_list['output_path'], param_list['trace_file_prd_y'])
    if os.path.exists(output_fullname):
        os.remove(output_fullname)
        logging.info('Deleted output file: %s' % output_fullname)

    output_fullname = os.path.join(param_list['output_path'], param_list['trace_file_prd_uv'])
    if os.path.exists(output_fullname):
        os.remove(output_fullname)
        logging.info('Deleted output file: %s' % output_fullname)

    output_fullname = os.path.join(param_list['output_path'], param_list['trace_file_cabacrdo'])
    if os.path.exists(output_fullname):
        os.remove(output_fullname)
        logging.info('Deleted output file: %s' % output_fullname)

    output_fullname = os.path.join(param_list['output_path'], param_list['trace_file_arch1rdo'])
    if os.path.exists(output_fullname):
        os.remove(output_fullname)
        logging.info('Deleted output file: %s' % output_fullname)


def get_total_frame_num(filename, width, height):
    size = os.path.getsize(filename)
    filesize = width * height * 3 / 2
    num_frames = size / filesize
    return num_frames


def check_params(param_list):
    param_list['output_path'] = common_lib.format_path(param_list['output_path'])
    param_list['input_path'] = common_lib.format_path(param_list['input_path'])

    common_lib.check_path(param_list['output_path'])
    check_files(param_list)

    if param_list['frame_num_to_encode'] == 0:
        param_list['frame_num_to_encode'] = get_total_frame_num(
            os.path.join(param_list['input_path'], param_list['input_filename']),
            param_list['nSrcWidth'], param_list['nSrcHeight'])
    if param_list['nIntraPicInterval']==0:
        param_list['nIntraPicInterval']=param_list['fFrameRate']
    return


def configure_rc_param(param_list, tmp_list):
    #check if it is 2pass
    if param_list['eRcType'] == global_vars.HEVC_RC_ABR_TWOPASS_ANAlYSE:
        param_list['eRcType'] = global_vars.HEVC_RC_ABR
        param_list['rc_i_pass'] = 1
    elif param_list['eRcType'] == global_vars.HEVC_RC_VBR_TWOPASS_ANAlYSE:
        param_list['eRcType'] = global_vars.HEVC_RC_VBR
        param_list['rc_i_pass'] = 1

    rc_type = param_list['eRcType']
    if param_list['rc_i_pass'] != 0:
        if rc_type in (global_vars.HEVC_RC_CBR, global_vars.HEVC_RC_CQP, global_vars.HEVC_RC_FIXQUANT):
            logging.warning('2pass is incompatible with %s' % global_vars.RC_STRING[rc_type])
            #sys.exit()
        elif rc_type not in (global_vars.HEVC_RC_ABR, global_vars.HEVC_RC_VBR):
            logging.warning('2pass is incompatible with %s' % global_vars.RC_STRING[rc_type])

    if rc_type != global_vars.HEVC_RC_FIXQUANT and rc_type != global_vars.HEVC_RC_CQP:
        if tmp_list['tmp_nBitrate'] <= 0:
            set_rc_related_param_auto(param_list)
            return
        elif rc_type == global_vars.HEVC_RC_ABR and tmp_list['tmp_nBitrate'] > 0:
            tmp_list['tmp_nMaxBitrate'] = 0
            tmp_list['tmp_vbv_buffer_size'] = 0
            #set_rc_related_param_manual(param_list, tmp_nBitrate, 0, 0)
        elif rc_type == global_vars.HEVC_RC_CBR and tmp_list['tmp_nBitrate'] > 0:
            if tmp_list['tmp_nMaxBitrate'] <= 0:
                tmp_list['tmp_nMaxBitrate'] = tmp_list['tmp_nBitrate']
            if tmp_list['tmp_vbv_buffer_size'] <= 0:
                tmp_list['tmp_vbv_buffer_size'] = tmp_list['tmp_nMaxBitrate']
                #set_rc_related_param_manual(param_list, tmp_nBitrate, tmp_nMaxBitrate, tmp_vbv_buffer_size)
        elif rc_type == global_vars.HEVC_RC_VBR and tmp_list['tmp_nBitrate'] > 0:
            if tmp_list['tmp_nMaxBitrate'] <= 0:
                tmp_list['tmp_nMaxBitrate'] = 3 * tmp_list['tmp_nBitrate']
            if tmp_list['tmp_vbv_buffer_size'] <= 0:
                tmp_list['tmp_vbv_buffer_size'] = tmp_list['tmp_nMaxBitrate']
                #set_rc_related_param_manual(param_list, tmp_nBitrate, tmp_nMaxBitrate, tmp_vbv_buffer_size)
        set_rc_related_param_manual(param_list, tmp_list['tmp_nBitrate'], tmp_list['tmp_nMaxBitrate'],
                                    tmp_list['tmp_vbv_buffer_size'])
        return


def get_default_tmp_list(param_list):
    tmp_list = {}  #dict()
    tmp_list['seq_name'] = os.path.splitext(param_list['input_filename'])[0]
                         #param_list['input_filename'].replace(".yuv","")
    tmp_list['tmp_nBitrate'] = -1
    tmp_list['tmp_nMaxBitrate'] = -1
    tmp_list['tmp_vbv_buffer_size'] = -1
    tmp_list['extra_cls'] = ""
    tmp_list['tmp_nSrcWidth'] = -1
    tmp_list['tmp_nSrcHeight'] = -1
    tmp_list['tmp_fFrameRate'] = -1
    tmp_list['do_execute']=0
    tmp_list['log_print']=0
    return tmp_list


def configure_enc_param(enc, param_list):
    tag_str = ""
    tmp_list = get_default_tmp_list(param_list)
    param_len = len(param_list)
    tmp_list_len = len(tmp_list)

    if len(sys.argv) >= 1:
        #opt_list, tag_str, seq_name, tmp_nBitrate, tmp_nMaxBitrate, tmp_vbv_buffer_size = parse_cl(enc)
        opt_list, tag_str = parse_enc_cl(enc)
        for (k, v) in opt_list.items():
            if param_list.has_key(k):
                param_list[k] = v
            else:
                #print "Bug may exist in this program"
                tmp_list[k] = v
        if param_len != len(param_list):
            logging.error('dict(param_list) has been changed somewhere. Please fix this bug.')
            sys.exit()
        if tmp_list_len != len(tmp_list):
            logging.error('dict(tmp_list) has been changed somewhere. Please fix this bug.')
            sys.exit()

    print tmp_list
    cons_log = configure_seq_param(param_list, tmp_list['seq_name'], tmp_list['tmp_nSrcWidth'],
                                   tmp_list['tmp_nSrcHeight'], tmp_list['tmp_fFrameRate'], tag_str)

    configure_rc_param(param_list, tmp_list)

    check_params(param_list)

    return (cons_log, tmp_list['extra_cls'],tmp_list['do_execute'])


