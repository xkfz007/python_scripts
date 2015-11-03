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


def configure_seq_param(param_list, tmp_name, tags=''):
    seq_name = seq_list.guess_seqname(tmp_name)
    org_width, org_height, org_fps = seq_list.get_reso_info(seq_name)
    if param_list['i_src_width'] <= 0:
        param_list['i_src_width'] = int(org_width)

    if param_list['i_src_height'] <= 0:
        param_list['i_src_height'] = int(org_height)

    if param_list['f_framerate'] <= 0:
        param_list['f_framerate'] = int(org_fps)

    if len(tags) >0:
        tags = '_' + tags

    param_list['input_filename'] = seq_name + '.yuv'
    param_list['output_filename'] = seq_name + tags + '_str.bin'
    param_list['trace_file_cabac'] = seq_name + tags + '_cabac.log'
    param_list['trace_file_general'] = seq_name + tags + '_general.log'
    param_list['dump_file_rec'] = seq_name + tags + '_rec.yuv'
    param_list['trace_file_prd_y'] = seq_name + tags + '_prdy.log'
    param_list['trace_file_prd_uv'] = seq_name + tags + '_prduv.log'
    param_list['trace_file_cabacrdo'] = seq_name + tags + '_cabacrdo.log'
    param_list['trace_file_arch1rdo'] = seq_name + tags + '_arch1rdo.log'

    return seq_name + tags + '_cons.log'


def set_bitrate(param_list,bitrate=-1,factor=2):
    if bitrate<=0:
       base_rate_dict={ '2560x1600': 3200,
                        '1920x1080': 1500,
                        '1280x720': 600,
                        '1024x768': 568,
                        '832x480': 300,
                        '416x240': 75,
                        '640x480': 222,
                        '352x288': 73,
                        '448x336': 110,
                        '3840x2160': 8000,
                        }
       reso = '%sx%s' % (param_list['i_src_width'], param_list['i_src_height'])
       if base_rate_dict.has_key(reso):
           base_rate=base_rate_dict[reso]
       else:
           base_rate=5000
       bitrate = param_list['f_framerate'] * base_rate / 30 *factor
    elif bitrate <= 1.0:
       bitrate *= param_list['i_src_width'] * param_list['i_src_height'] * param_list['f_framerate'] / 1000
    param_list['i_bitrate'] = bitrate


def set_max_bitrate(param_list,max_bitrate=-1):
    if max_bitrate <= 0:
       if param_list['e_rctype'] == global_vars.HEVC_RC_CBR:  #CBR
           max_bitrate=param_list['i_bitrate']
       elif param_list['e_rctype'] == global_vars.HEVC_RC_VBR:  #"VBR":
           max_bitrate= 3 * param_list['i_bitrate']
    param_list['i_max_bitrate'] = max_bitrate

def set_buffer_size(param_list,buffer_size=-1):
    if buffer_size <= 0:
       buffer_size = 1 * param_list['i_max_bitrate']
    param_list['i_buffer_size'] = buffer_size

def set_rc_full_param(param_list,bitrate=-1,max_bitrate=-1,buffer_size=-1):
    set_bitrate(param_list,bitrate)
    set_max_bitrate(param_list,max_bitrate)
    set_buffer_size(param_list,buffer_size)


def usage():
    help_msg = '''USAGE: cl_run_enc.py [OPTIONS]...
   OPTIONS:
     -e <string>              encoder name: as265,x265,x264,hm,jm
     -s <string>              seqname
     -i <string>              input_path
     -o <string>              output_path
     -T <int:int:int>         multi-threaded parameters
                                #1: frame parallelism threads [1]
                                #2: WPP threads [1]
                                #3: Lookahead threads [1]
     -E <width:height:fps>/<widthxheightxfps>
                              resolution parameters
     -f <int:int:int>         frames info that will be encoded
                                #1: Maximum number of frames to encode [-1]
                                #2: Max number of references to be allowed (1 .. 16) [1]
                                #3: First frame to encode [0]
     -g <int:int:int>         gop info
                                #1: I frame interval [250]
                                #2: open-gop, 0:disabled, 1:enabled [1]
                                #3: scenecut, How aggressively to insert extra I-frames [40]
     -b <int:int:int>         b-frame parameters
                                #1: number of b-frame [3]
                                #2: bref/b-pyramid/hierarchical, 0: disabled, 1: enabled [1]
                                #3: bframe adaptive, 0: disabled, 1: fast method, 2: trellis [0]
     -r <int/string:int/float:int:int:int>
                              rate control parameters
                                #1: rate control method, 0/9:cqp, 8:abr, 1:cbr, 9:vbr, 10:crf(Quality-based VBR) [0]
                                #2: qp [26] or bitrate [0] or crf [28.0]
                                #3: the max bitrate [0]
                                #4: the buffer size [0]
                                #5: the vbv init time [0]
     -p <integer>             rate control 2pass [0]
                                -0: single pass encoding,
                                -1: 2pass encoding(including first pass and second pass)
                                -2: 2pass encoding with clipping
                                -3: first pass of 2pass encoding (only for x26x)
                                -4: second pass of 2pass encoding (only for x26x)
     -P <integer>             Preset, trade off performance for compression efficiency [5]
     -u <int:int:int:int:int:int>
                              CU,PU,TU parameters
                                #1: Maximum CU size [6]
                                #2: Maximum CU search depth [3]
                                #3: Maximum log2 value of TU size [5]
                                #4: Minimum log2 value of TU size [2]
                                #5: Max TU recursive depth for intra CUs [1]
                                #6: Max TU recursive depth for inter CUs [1]
     -A <int:int:int:int:int> Analysis
                                #1: Maximum number of merge candidates [2]
                                #2: Enable intra in P frames in veryslow presets [1]
                                #3: Enable intra in B frames in veryslow presets [1]
                                #4: Enable rectangular motion partitions Nx2N and 2NxN [1]
                                #5: Enable asymmetric motion partitions, requires #4 [0]
     -F <int:int>             Loop filters (deblock and SAO)
                                #1: sao, 0:disabled, 1:enabled [0]
                                #2: deblock, 0:disabled, 1:enabled [1]
     -a <int:int:float>       adaptive quatization or cu-tree
                                #1: cu-tree, 0:disabled, 1:enabled [1]
                                #2: aq-mode, 0:disabled, 1:Variance AQ, 2:Auto-Variance AQ [1]
                                #3: aq-strength, reduces blocking and blurring in flat and textured areas [1.0]
     -q <int:int:int>         qp ralated parameters
                                #1: Set max QP step [4]
                                #2: Set min QP [0]
                                #3: Set max QP [51]
     -B <int:int:int:int:int> Bitstream info
                                #1: Emit SPS and PPS headers at each keyframe [0]
                                #2: Emit access unit delimiters at the start of each access unit [0]
                                #3: Emit SEI identifying encoder and parameters [1]
                                #4: Enable HRD parameters signaling [1]
                                #5: Decoded Picture Hash SEI, 0:disabled, 1:MD5, 2:CRC, 3:Checksum  [0]
     -L <int:int:float:float:float>
                              rc ralated lower resolution info
                                #1: Lowres, 0:auto, 1:semi, 2:quater [1]
                                #2: Number of frames for frame-type lookahead (determines encoder latency) [20]
                                #3: Tolerance of ABR ratecontrol and VBV [1.0]
                                #4: QP factor between I and P [1.40]
                                #5: QP factor between P and B[1.30]
     -y                       dump-yuv
     -C <string>              extra command lines


     --path <string>          set the encoder path
     --log                    print log
   '''
    print help_msg
    return


def parse_encoder_arg_int(opt_list,arg,opts,vals,delimiter=':'):
    common_lib.parse_arg_internal(arg,delimiter,vals)
    n=len(opts)
    for i in range(0,n):
        if int(vals[i])>=0:
           opt_list[opts[i]]=int(vals[i])

def parse_encoder_arg_mix(opt_list,arg,opts,vals,delimiter=':'):
    typs=[]
    for i in vals:
        typs.append(type(i))

    common_lib.parse_arg_internal(arg,delimiter,vals)
    n=len(opts)
    for i in range(0,n):
        if typs[i]==int and int(vals[i])>=0:
            opt_list[opts[i]]=int(vals[i])
        elif typs[i]==float and float(vals[i])>=0:
            opt_list[opts[i]]=float(vals[i])
        elif typs[i]==str and len(vals[i])>0:
            opt_list[opts[i]]=str(vals[i])


def parse_reso_fps(opt_list,arg):
    opts=('i_src_width', 'i_src_height', 'f_framerate')
    vals=[-1,-1,-1.0]
    if 'x' in arg:
        parse_encoder_arg_mix(opt_list,arg,opts,vals,'x')
    else:
        parse_encoder_arg_mix(opt_list,arg,opts,vals)

def parse_threads(opt_list,arg):
    opts=('i_frame_threads', 'i_wpp_threads', 'i_lookahead_threads')
    vals=[-1 for i in range(0,len(opts))]
    parse_encoder_arg_int(opt_list,arg,opts,vals)

def parse_frame_num(opt_list,arg):
    #default parameter values
    opts=('i_frame_num_to_encode', 'i_maxref', 'i_first_frame')
    vals=[-1 for i in range(0,len(opts))]
    parse_encoder_arg_int(opt_list,arg,opts,vals)

def parse_gop_param(opt_list,arg):
    #default parameter values
    opts=('i_keyint', 'b_open_gop','i_scenecut_threshold')
    vals=[-1 for i in range(0,len(opts))]
    parse_encoder_arg_int(opt_list,arg,opts,vals)

def parse_bframe_param(opt_list,arg):
    opts=('i_bframe', 'b_bframe_pyramid', 'i_bframe_adaptive')
    vals=[-1 for i in range(0,len(opts))]
    parse_encoder_arg_int(opt_list,arg,opts,vals)

def parse_rc_param(opt_list,arg):
    opts=('e_rctype', 'i_bitrate', 'i_max_bitrate', 'i_buffer_size', 'i_buffer_init_time')
    vals=[-1 for i in range(0,len(opts))]
    common_lib.parse_arg_internal(arg,':',vals)

    qp_bitrate_crf=''
    n=len(opts)
    for i in range(0,n):
        print 'opts[%s]=%s,vals[%s]=%s'%(i,opts[i],i,vals[i])
        if opts[i]=='e_rctype': #set rc method
            opt_list[opts[i]]=get_rc_type(vals[i])
        elif opts[i]=='i_bitrate':
            qp_bitrate_crf=str(vals[i])
        else:
            if int(vals[i])>=0:
                opt_list[opts[i]]=int(vals[i])

    if len(qp_bitrate_crf)>0:
        if opt_list['e_rctype'] in (global_vars.HEVC_RC_FIXQUANT, global_vars.HEVC_RC_CQP):
            if int(qp_bitrate_crf)>=0:
                opt_list['i_qp'] = int(qp_bitrate_crf)
        elif opt_list['e_rctype'] == global_vars.HEVC_RC_CRF:
            if float(qp_bitrate_crf)>=0.0:
                opt_list['f_rf_constant'] = float(qp_bitrate_crf)
        else:
            if int(qp_bitrate_crf)>=0:
                opt_list['i_bitrate'] = int(qp_bitrate_crf)

def parse_unit_param(opt_list,arg):
    opts=('i_max_cuwidth', 'i_max_cudepth',
          'i_max_tulog2width', 'i_min_tulog2width',
          'i_max_intra_tudepth', 'i_min_inter_tudepth',)
    vals=[-1 for i in range(0,len(opts))]
    parse_encoder_arg_int(opt_list,arg,opts,vals)

def parse_cutree_aq(opt_list,arg):
    opts=('b_cutree', 'i_aq_mode', 'f_aq_strength', )
    vals=[-1, -1, -1.0]
    parse_encoder_arg_mix(opt_list,arg,opts,vals)

def parse_qp_param(opt_list,arg):
    opts=('i_qp_step', 'i_qp_min', 'i_qp_max', )
    vals=[-1 for i in range(0,len(opts))]
    parse_encoder_arg_int(opt_list,arg,opts,vals)

def parse_filter_param(opt_list,arg):
    opts=('b_sao', 'b_dbl',)
    vals=[-1 for i in range(0,len(opts))]
    parse_encoder_arg_int(opt_list,arg,opts,vals)

def parse_analysis_param(opt_list,arg):
    opts=('i_merge', 'b_pintra', 'b_bintra', 'b_rect', 'b_amp',)
    vals=[-1 for i in range(0,len(opts))]
    parse_encoder_arg_int(opt_list,arg,opts,vals)

def parse_bitstream_param(opt_list,arg):
    opts=('b_repeat_headers', 'b_enable_access_unit_delimiters',
          'b_emit_hrd_sei', 'b_emit_info_sei', 'i_decoded_picture_hash_sei',)
    vals=[-1 for i in range(0,len(opts))]
    parse_encoder_arg_int(opt_list,arg,opts,vals)

def parse_rc_lowres_param(opt_list,arg):
    opts=('i_lowres', 'i_lookahead', 'f_rate_tolerance', 'f_ip_factor', 'f_pb_factor',)
    vals=[-1, -1, -1.0, -1.0, -1.0]
    parse_encoder_arg_mix(opt_list,arg,opts,vals)

def get_tag(opt, arg):
    new_arg=arg.replace(':','x')
    str = opt[1:] + new_arg
    return str


def get_rc_type(arg):
    rc_type = 0
    if type(arg)==int:
        rc_type = int(arg)
    elif type(arg)==str and global_vars.RC_DICT.has_key(arg.upper()):
        rc_type = global_vars.RC_DICT[arg.upper()]

    return rc_type

def parse_enc_cl(enc):

    if len(sys.argv) == 1:
        usage()
        sys.exit()

    help=common_lib.HELP(usage,enc.get_exe())
    options='e:s:i:o:T:E:f:g:b:r:p:P:u:A:F:a:q:B:L:yC:'
    try:
        opts, args = getopt.getopt(sys.argv[1:], options +help.get_opt(),
                                   ['path=','log'])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    except Exception, e:
        print e

    opt_list = {}  #dict()
    tag_str = ""

    Encoder_flag = 0
    Encoder_path=''

    for opt, arg in opts:
        if opt == '-e':
            #opt_list['encoder_id'] = arg
            enc.set_id(arg.strip())
            help.set_BIN(enc.get_exe())
            help.set_help(enc.get_help())
            Encoder_flag = 1
        elif opt == '-s':
            opt_list['seq_name'] = arg
        elif opt == '-i':
            opt_list['input_path'] = arg
        elif opt == '-o':
            opt_list['output_path'] = arg
        elif opt == '-T':
            parse_threads(opt_list,arg)
            tag_str += get_tag(opt, arg)
        elif opt == '-E':
            parse_reso_fps(opt_list,arg)
            tag_str += get_tag(opt, arg)
        elif opt == '-f':
            parse_frame_num(opt_list,arg)
            tag_str += get_tag(opt, arg)
        elif opt == '-g':
            parse_gop_param(opt_list,arg)
            tag_str += get_tag(opt, arg)
        elif opt == '-b':
            parse_bframe_param(opt_list,arg)
            tag_str += get_tag(opt, arg)
        elif opt == '-r':
            parse_rc_param(opt_list,arg)
            tag_str += get_tag(opt, arg)
        elif opt == '-p':
            opt_list['i_pass'] = int(arg)
            tag_str += get_tag(opt, arg)
        elif opt == '-P':
            opt_list['i_preset'] =int(arg)
            tag_str += get_tag(opt, arg)
        elif opt == '-u':
            parse_unit_param(opt_list,arg)
            tag_str += get_tag(opt, arg)
        elif opt in ('-A',):
            parse_analysis_param(opt_list,arg)
            tag_str += get_tag(opt, arg)
        elif opt in ('-F',):
            parse_filter_param(opt_list,arg)
            tag_str += get_tag(opt, arg)
        elif opt == '-a':
            parse_cutree_aq(opt_list,arg)
            tag_str += get_tag(opt, arg)
        elif opt == '-q':
            parse_qp_param(opt_list,arg)
            tag_str += get_tag(opt, arg)
        elif opt in ('-B',):
            parse_bitstream_param(opt_list,arg)
            tag_str += get_tag(opt, arg)
        elif opt in ('-L',):
            parse_rc_lowres_param(opt_list,arg)
            tag_str += get_tag(opt, arg)
        elif opt == '-y':
            opt_list['i_trace_flag'] |= 2
        elif opt == '-C':
            opt_list['extra_cls'] = arg
            tag_str += get_tag(opt, '')
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

    #return (opt_list, tag_str, seq_name, tmp_i_bitrate, tmp_i_max_bitrate, tmp_i_buffer_size)
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

    if param_list['i_frame_num_to_encode'] == 0:
        param_list['i_frame_num_to_encode'] = get_total_frame_num(
            os.path.join(param_list['input_path'], param_list['input_filename']),
            param_list['i_src_width'], param_list['i_src_height'])
    if param_list['i_keyint']==0:
        param_list['i_keyint']=param_list['f_framerate']
    return


def configure_rc_param(param_list):
    #check if it is 2pass
    if param_list['e_rctype'] == global_vars.HEVC_RC_ABR_TWOPASS_ANAlYSE:
        param_list['e_rctype'] = global_vars.HEVC_RC_ABR
        param_list['i_pass'] = 1
    elif param_list['e_rctype'] == global_vars.HEVC_RC_VBR_TWOPASS_ANAlYSE:
        param_list['e_rctype'] = global_vars.HEVC_RC_VBR
        param_list['i_pass'] = 1

    rc_type = param_list['e_rctype']
    if param_list['i_pass'] != 0:
        if rc_type in (global_vars.HEVC_RC_CBR, global_vars.HEVC_RC_CQP, global_vars.HEVC_RC_FIXQUANT):
            logging.warning('2pass is incompatible with %s' % global_vars.RC_STRING[rc_type])
            #sys.exit()
        elif rc_type not in (global_vars.HEVC_RC_ABR, global_vars.HEVC_RC_VBR):
            logging.warning('2pass is incompatible with %s' % global_vars.RC_STRING[rc_type])


    if rc_type not in (global_vars.HEVC_RC_FIXQUANT, global_vars.HEVC_RC_CQP,global_vars.HEVC_RC_CRF):
        #set_bitrate(param_list,param_list['i_bitrate'])
        #set_max_bitrate(param_list,param_list['i_max_bitrate'])
        #set_buffer_size(param_list,param_list['i_buffer_size'])
        set_rc_full_param(param_list,param_list['i_bitrate'],param_list['i_max_bitrate'],param_list['i_buffer_size'])


def get_default_tmp_list(param_list):
    tmp_list = {}  #dict()
    tmp_list['seq_name'] = os.path.splitext(param_list['input_filename'])[0]
                         #param_list['input_filename'].replace(".yuv","")
    #tmp_list['tmp_i_bitrate'] = -1
    #tmp_list['tmp_i_max_bitrate'] = -1
    #tmp_list['tmp_i_buffer_size'] = -1
    tmp_list['extra_cls'] = ""
    #tmp_list['tmp_i_src_width'] = -1
    #tmp_list['tmp_i_src_height'] = -1
    #tmp_list['tmp_f_framerate'] = -1
    tmp_list['do_execute']=0
    tmp_list['log_print']=0
    return tmp_list


def configure_enc_param(enc, param_list):
    tag_str = ""
    tmp_list = get_default_tmp_list(param_list)
    param_len = len(param_list)
    tmp_list_len = len(tmp_list)

    if len(sys.argv) >= 1:
        #opt_list, tag_str, seq_name, tmp_i_bitrate, tmp_i_max_bitrate, tmp_i_buffer_size = parse_cl(enc)
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
    cons_log = configure_seq_param(param_list, tmp_list['seq_name'],tag_str)

    configure_rc_param(param_list)

    check_params(param_list)

    return (cons_log, tmp_list['extra_cls'],tmp_list['do_execute'])


