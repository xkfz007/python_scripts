#!/usr/bin/python
# The main purpose of this script is to wrap the ffmpeg.exe
# so that we will not have to give the exact input file name or output file name.
# Right now, we just need give the glob pattern of the input file name
# and this is very useful for the Chinese file or directory names
__author__ = 'hfz2597'
import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils
from ffprobe import FFProbe



logger=utils.Log('FFMPEG','info')
#fflog = logging.getLogger('ffmpeg')
#fflog.setLevel(logging.WARNING)
#hdr=logging.StreamHandler()
#hdr.setFormatter(logging.Formatter('[%(levelname)s]:%(message)s'))
#fflog.addHandler(hdr)
#fflog=lib.Log('ffmpeg','info')

class AVFormat:
    def __init__(self,name,extensions,description):
        self.name=name
        self.extensions=extensions.split(',')
        self.description=description
        #self.supported_vcodecs=vcodecs.split(',')
        #self.supported_acodecs=acodecs.split(',')

vfmt_list=[
    AVFormat('asf',           'asf,wmv,wma',          'ASF (Advanced / Active Streaming Format)'  ),
    AVFormat('avi',           'avi',                  'AVI (Audio Video Interleaved)'             ),
    AVFormat('f4v',           'f4v',                  'F4V Adobe Flash Video'                     ),
    AVFormat('flv',           'flv',                  'FLV (Flash Video)'                         ),
    AVFormat('m4v',           'm4v',                  'raw MPEG-4 video'                          ),
    AVFormat('matroska',      'mkv,mka',              'Matroska'                                  ),
    AVFormat('mmf',           'mmf',                  'Yamaha SMAF'                               ),
    AVFormat('mov',           'mov',                  'QuickTime / MOV'                           ),
    AVFormat('mp4',           'mp4',                  'MP4 (MPEG-4 Part 14)'                      ),
    AVFormat('mpeg',          'mpg,mpeg',             'MPEG-1 Systems / MPEG program stream'      ),
    AVFormat('mpeg1video',    'mpg,mpeg,m1v',         'raw MPEG-1 video'                          ),
    AVFormat('mpeg2video',    'm2v',                  'raw MPEG-2 video'                          ),
    AVFormat('mpegts',        'ts,m2t,m2ts,mts',      'MPEG-TS (MPEG-2 Transport Stream)'         ),
    AVFormat('mxf',           'mxf',                  'MXF (Material eXchange Format)'            ),
    AVFormat('rm',            'rm,ra,rmvb',           'RealMedia'                                 ),
    AVFormat('swf',           'swf',                  'SWF (ShockWave Flash)'                     ),
    AVFormat('vc1',           'vc1',                  'raw VC-1 video'                            ),
    AVFormat('yuv4mpegpipe',  'y4m',                  'YUV4MPEG pipe'                             ),
    AVFormat('rawvideo',      'yuv,rgb',              'raw video'                                 ),
]
rawfmt_list=[
    AVFormat('h261',          'h261',                 'raw H.261'                                 ),
    AVFormat('h263',          'h263',                 'raw H.263'                                 ),
    AVFormat('h264',          'h264,264,avc',         'raw H.264 video'                           ),
    AVFormat('hevc',          'hevc,265,h265',        'raw HEVC video'                            ),
    AVFormat('raw',           'es,raw',               'raw video'                                 ),
]
afmt_list=[
    AVFormat('ac3',          'ac3',                      'raw AC-3'),
    AVFormat('adts',          'adts,aac',                      'ADTS AAC (Advanced Audio Coding)'),
    AVFormat('flac',          'flac',                     'raw FLAC'),
    AVFormat('mp2',           'mp2,mpa,m2a',              'MP2 (MPEG audio layer 2)'),
    AVFormat('mp3',           'mp3',                      'MP3 (MPEG audio layer 3)'),
    AVFormat('oga',           'oga',                      'Ogg Audio'),
    AVFormat('ogg',           'ogg',                      'Ogg'),
    AVFormat('wav',           'wav',                      'WAV / WAVE (Waveform Audio)'),
]
ifmt_list=[
    AVFormat('gif',           'gif',                      'GIF Animation'),
    AVFormat('image2',        'bmp,jpeg,jpg,png,tiff',    'image2 sequence'),
]

fmt_list=vfmt_list+afmt_list+ifmt_list+rawfmt_list

#format dict
vfmt_dict={}
afmt_dict={}
ifmt_dict={}
rawfmt_dict={}

#extension dict
vext_dict={}
aext_dict={}
iext_dict={}
rawext_dict={}

#all format dict
fmt_dict={}
ext_dict={}
for i in vfmt_list:
   vfmt_dict[i.name]=i
   for j in i.extensions:
       vext_dict[j]=i
fmt_dict.update(vfmt_dict)
ext_dict.update(vext_dict)

for i in afmt_list:
    afmt_dict[i.name]=i
    for j in i.extensions:
        aext_dict[j]=i
fmt_dict.update(afmt_dict)
ext_dict.update(aext_dict)

for i in ifmt_list:
    ifmt_dict[i.name]=i
    for j in i.extensions:
        iext_dict[j]=i
fmt_dict.update(ifmt_dict)
ext_dict.update(iext_dict)

for i in  rawfmt_list:
    rawfmt_dict[i.name]=i
    for j in i.extensions:
        rawext_dict[j]=i
fmt_dict.update(rawfmt_dict)
ext_dict.update(rawext_dict)

class BSFilter:
    def __init__(self,codec,fmt,filter):
        self.codec=codec
        self.filter=filter
        self.fmts=fmt.split(',')

bsf_list=[
    BSFilter('h264','matroska,mp4,flv,mov','h264_mp4toannexb'),
    BSFilter('hevc','matroska,mp4,flv,mov','hevc_mp4toannexb'),
    BSFilter('adts','adts','aac_adtstoasc'),
]

bsf_cdc_dict= {'h264': 'h264_mp4toannexb',
               'hevc': 'hevc_mp4toannexb',
           }
bsf_fmt_list=['matroska','mp4','flv','mov']

bsf_for_mp4 = {'h264': 'h264_mp4toannexb',
               'hevc': 'hevc_mp4toannexb'}
bsf_for_mp4_ext_list=fmt_dict['matroska'].extensions+fmt_dict['mp4'].extensions

h264_name_list = ('h264', 'h.264', 'avc', '264')
h265_name_list = ('hevc', 'h.265', 'h265', '265')
bitstream_name_list = h264_name_list + h265_name_list
yuv_name_list = ('yuv', 'y4m')
mp4_name_list = ('mp4', 'flv', 'mkv', 'f4v')
avi_name_list = ('avi',)
ts_name_list = ('ts',)
video_name_list = mp4_name_list + avi_name_list + ts_name_list
audio_name_list = ('aac', 'mp3', 'ogg', 'wav')

image_name_list = ('jpg', 'jpeg', 'png', 'bmp')
gif_name_list = ('gif',)

valid_ext_list = h264_name_list + \
                 h265_name_list + \
                 yuv_name_list + \
                 video_name_list + \
                 audio_name_list + \
                 image_name_list + \
                 gif_name_list

VIDEO_ENCODER_DEFAULT='libx264'
AUDIO_ENCODER_DEFAULT='aac'
ENCODER_TRANSPARENT='copy'
VIDEO_ENC_CMD='-c:v'
AUDIO_ENC_CMD='-c:a'
SUBTITLE_ENC_CMD='-c:s'
VIDEO_DISABLED='-vn'
AUDIO_DISABLED='-an'
SUBTITLE_DISABLED='-sn'


def usage():
    help_msg = '''USAGE:pyff.py [OPTIONS]... [ARGUMENTS]...
   OPTIONS:
     -e <string>  the output file extension
                    -h264/hevc: get the raw bitstream from media file
                    -yuv: decode the input to get rawvideo(yuv)
                    -aac/mp3: extract audio from media file
                    -jpg/png/bmp: extract images from media file
                    -gif: create a gif file from video file
                    -ts
     -a           extract audio using the extra command lines from -C,
                  ignore the auto generated command lines from extension(-e)
     -o <str:str> output file path or file tag:
                    #1: output file path, if it is a dir, it is used, or it is regared as tag
                    #2: output file tag
     -C <string>  the ffmpeg commands
     -T <integer> set thread num
     -t <hour:minute:second.xxx-hour:minute:second.xxx>/
        <hour:minute:second.xxx+hour:minute:second.xxx>
                  set the time duration, and in the first format, quotations are needed because of '-'
     -E <width:height>/<widthxheight>
                  set the output width and height
     -v <loglevel>
   ARGUMENTS:
     file or directory, support pattern globbing,these are the input files that will be processed
   '''
    print help_msg
    return


def detect_file(input_file):
    m = FFProbe(input_file)
    vst=m.video
    #assert len(vst)<=1
    ast=m.audio
    sst=m.subtitle
    fmt=m.format

    return fmt,vst,ast,sst

#def get_codec_cmd(vst,vclist,ast,aclist):
#    if ast.codecName() in ('atrac3','cook','ra_288','sipr'): #unsupported audio codec of mkv
#        acdec_cmd=' %s %s'%(AUDIO_ENC_CMD,AUDIO_ENCODER_DEFAULT)#use default audio codec
#        if ast.bitrate()>64000:
#            acdec_cmd+=' -b:a 64k'
#    if vst.codecName() in ('rv10','rv20'):#unsuported video codecs of mkv
#        vcdec_cmd=' %s %s'%(VIDEO_ENC_CMD,VIDEO_ENCODER_DEFAULT)#use default video codec
#    return vcdec_cmd,acdec_cmd

def get_cmd_line(input_file, ofpath, ofname, oftag, ofext,  pre_cmd, post_cmd, extra_cmd):
    infdir, infile = os.path.split(input_file)
    infname, infext = os.path.splitext(infile)
    #if infext.startswith('.'):
    #    infext=infext[1:]
    infext=utils.format_ext2(infext)

    #detect file info
    inf_fmt,inf_vst,inf_ast,inf_sst=detect_file(input_file)
    #if infext not in fmt_dict[infext].extensions:
    #    logger.warning('Invaild extension of %s, it should be %s'%(infext,fmt_list[infext].extensions))
    #    infext=fmt_list[infext].extensions[0]

    #in_astream=inf_ast[0]
    #in_sstream=inf_sst[0]

    #map_cmd=''
    #idx=0
    #bitrate=inf_vst[idx].bitrate
    ##frameSize=inf_vst[idx].frameSize
    #if len(inf_vst)>1:
    #    for i in inf_vst:
    #        if i.bitrate>bitrate:
    #            bitrate=i.bitrate
    #            idx=i
    #in_vstream=inf_vst[idx]
    #map_cmd+=' -map 0:%s'%idx

    #idx=0
    #if len(inf_ast)>1:
    #    for i in inf_ast:



    #normalize the output
    if len(ofpath) == 0:
        ofpath = infdir
    if len(ofname)==0:
        ofname=infname
    if len(ofext)==0:
        ofext=infext

    #if ofname==infname and ofext==infext:#add tag to distinguish in and out
    #    oftag+='out'

    #logger.info('ofname="%s" ofext="%s"' % (ofname,ofext))

    #input is video and output is audio, this means audio will be extracted from video
    if infext not in vext_dict.keys():
        logger.error('Invalid extension "%s" of "%s"'%(infext,input_file))
        sys.exit()

    if ofext==ofext.upper():
       ofmt=ext_dict[ofext.lower()]
    else:
       ofmt=ext_dict[ofext]

    if ofmt.name=='raw':#auto decide the output format
        #fmt_cmd='-f %s'%inf_vst[0].codecName()
        #oftag+='%s'%inf_vst[0].codecName()
        ofmt=ext_dict[inf_vst[0].codecName]

    fmt_cmd='-f %s'%ofmt.name

    vcdec_cmd=''
    acdec_cmd=''
    scdec_cmd=''

    #if ofext in vext_dict.keys():
    if ofmt.name in vfmt_dict.keys():

        #if inf_ast[0].bitrate()>96000:
        #    acdec_cmd='  -b:a 96k -c:a libvorbis'
        #else:
        #    acdec_cmd=' -c:a copy'
        acdec_cmd=' %s %s'%(AUDIO_ENC_CMD,ENCODER_TRANSPARENT)

        if ofext==ofext.upper():#in default situation, we will use copy
            vcdec_cmd=' %s %s'%(VIDEO_ENC_CMD,ENCODER_TRANSPARENT)
        else:
            #if input is mp4 or mkv format and codec is h264, h264_mp4toannexb is needed
            if infext in bsf_fmt_list and ofmt.name not in bsf_fmt_list \
                    and inf_vst[0].codecName() in bsf_cdc_dict.keys():
                fmt_cmd+=' -bsf:v %s'%bsf_cdc_dict[inf_vst[0].codecName()]

        if ofmt.name =='matroska' or ofmt.name=='mpegts':
            if inf_ast[0].codecName() in ('atrac3','cook','ra_288','sipr'): #unsupported audio codec of mkv
                acdec_cmd=' %s %s'%(AUDIO_ENC_CMD,AUDIO_ENCODER_DEFAULT)#use default audio codec
                #if inf_ast[0].bitrate()>64000:
                #    acdec_cmd+=' -b:a 64k'
            if inf_vst[0].codecName() in ('rv10','rv20'):#unsuported video codecs of mkv
                vcdec_cmd=' %s %s'%(VIDEO_ENC_CMD,VIDEO_ENCODER_DEFAULT)#use default video codec

        elif ofmt.name=='mp4':
            if inf_vst[0].codecName() not in ('h264','hevc','vc1','mpeg2','mpeg4','h263'):
                vcdec_cmd=' %s %s'%(VIDEO_ENC_CMD,VIDEO_ENCODER_DEFAULT)#use default video codec
            if inf_ast[0].codecName() not in ('aac','ac3','eac3','dirac','mp2','mp3','vorbis'):
                acdec_cmd=' %s %s'%(AUDIO_ENC_CMD,AUDIO_ENCODER_DEFAULT)#use default audio codec
                #if inf_ast[0].bitrate()>64000:
                #    acdec_cmd+=' -b:a 64k'

        elif ofmt.name=='flv':
            if inf_vst[0].codecName() not in ('flv1','h263','mpeg4','flashsv', 'flashsv2', 'vp6f','vp6','vp6a','h264','hevc'):
                vcdec_cmd=' %s %s'%(VIDEO_ENC_CMD,VIDEO_ENCODER_DEFAULT)#use default video codec
            if inf_ast[0].codecName() not in ('mp3','adpcm_swf','aac','nellymoser','speex'):
                acdec_cmd=' %s %s'%(AUDIO_ENC_CMD,AUDIO_ENCODER_DEFAULT)#use default audio codec
                #if inf_ast[0].bitrate()>64000:
                #    acdec_cmd+=' -b:a 64k'


        if len(inf_sst)>0:
            scdec_cmd=' %s %s'%(SUBTITLE_ENC_CMD,ENCODER_TRANSPARENT)

        logger.info('inf_fmt.name=%s ofmt.name=%s inf_vst.name=%s'
                     % (inf_fmt.formatName(),ofmt.name,inf_vst[0].codecName()))

    elif ofmt.name in afmt_dict.keys():
        #ofext=afmt_dict[inf_ast[0].codecName()].extensions[0]
        vcdec_cmd=' %s'%VIDEO_DISABLED
        acdec_cmd=' %s %s'%(AUDIO_ENC_CMD,ENCODER_TRANSPARENT)
        #if inf_ast[0].bitrate()>64000 and ofext!=ofext.upper():
        #    acdec_cmd=' -c:a libvorbis -b:a 64k'
        if ofext!=ofext.upper():
            acdec_cmd=' %s %s'%(AUDIO_ENC_CMD,AUDIO_ENCODER_DEFAULT)

    #elif ofmt.name in ifmt_dict.keys() or ofmt.name in rawfmt_dict.keys():
    #    if len(inf_sst)>0:
    #        scdec_cmd=' %s'%SUBTITLE_DISABLED
    #    if len(inf_ast)>0:
    #        acdec_cmd=' %s'%AUDIO_DISABLED
    elif ofmt.name in ifmt_dict.keys():
        if ofext==ofext.upper():
            vcdec_cmd=' -r 1 -vframe 1'
        else:
            oftag+='%d'


    #ensure input filename and output filename are different
    if len(oftag)==0 and ofname==infname and ofext.lower()==infext.lower():
        oftag+='%s'%inf_vst[0].codecName()
        #oftag+='out'

    #output_file = '%s_%s.%s' % (ofname, oftag, ofext)
    output_file=ofname
    if len(oftag)>0:
        output_file+='_'+oftag
    output_file+='.'+ofext.lower()

    if len(ofpath) > 0:
        output_file = '%s%s%s' % (ofpath, os.sep, output_file)

    cmd_line = pre_cmd
    cmd_line += ' -i "%s"' % input_file
    #cmd_line += ' %s' % map_cmd
    cmd_line += ' %s' % vcdec_cmd
    cmd_line += ' %s' % acdec_cmd
    cmd_line += ' %s' % scdec_cmd
    cmd_line += ' %s' % post_cmd
    cmd_line += ' %s' % extra_cmd
    cmd_line += ' %s' % fmt_cmd
    cmd_line += ' "%s"' % output_file
    return (cmd_line, output_file)


def parse_reso(arg, width=-2, height=-2, delimiter='x'):
    x, y = utils.parse_arg(arg, delimiter, str(width), str(height))
    return int(x), int(y)


def parse_time(arg, startp='', dura='', delimiter='+'):
    x, y = utils.parse_arg(arg, delimiter, startp, dura)
    return x, y


'''
ffmpeg.py conan1.mkv
ffmpeg.py conan1.mkv -o .mp4
ffmpeg.py conan1.mkv -o a.mp4
ffmpeg.py conan1.mkv -o a.ts
ffmpeg.py conan1.mkv -o a.jpg
ffmpeg.py conan1.mkv -o a.hevc
ffmpeg.py conan1.mkv -o a.h264
ffmpeg.py conan1.mkv -o a.yuv
ffmpeg.py conan1.mkv -o dir/aa.yuv
ffmpeg.py conan1.mkv -o dir/.264
ffmpeg.py conan1.mkv -o dir/aa
ffmpeg.py conan1.mkv -o dir:bb
ffmpeg.py conan1.mkv -o dir:a.mp4
ffmpeg.py conan1.mkv -o dir:.mp4
ffmpeg.py conan1.mkv -o dir/bb.264:aa
ffmpeg.py conan1.mkv -o a

'''
def parse_output(arg, default_opath='', default_otag_oext='', delimiter=':'):
    opath, otag_oext = utils.parse_arg(arg, delimiter, default_opath, default_otag_oext)
    if opath.endswith('/') or opath.endswith('\\'):
        opath=opath[0:-1]
    logger.info('opth=%s,otag_oext=%s' % (opath, otag_oext))
    ofname_oext=''
    if '.' in opath:#format like: movies/conan/1.mp4
        opath, ofname_oext= os.path.split(opath)

    logger.info('opth=%s,ofname_oext=%s,otag_oext=%s' % (opath, ofname_oext,otag_oext))
    if len(opath) > 0 and not os.path.isdir(opath):
        #opt = raw_input('Directory "%s" does not exist, do you want to create it?(Y/N)' % opath)
        #if opt.lower() in 'yes':
        #    os.makedirs(opath)
        #    fflog.info('Diectory "%s" is created.' % arg)
        #else:
        #    fflog.error('Diectory "%s" does not exist, using the current directory' % opath)
        #    opath='.'
        if len(ofname_oext)==0:
            logger.warning('Directory does not exist, filename will be created')
            tmp=opath.replace('/','_')
            ofname_oext=tmp.replace('\\','_')
        opath=''

    oext=''
    oext2=''
    #otag=''
    #ofname=''
    if '.' in ofname_oext:#split ofname_oext to get filename and extension
        ofname,oext=ofname_oext.split('.')
    else:
        ofname=ofname_oext

    if '.' in otag_oext:# split the extension of output file from variable otag_oext
        otag,oext2=otag_oext.split('.')
    else:
        otag=otag_oext

    if len(oext)==0 and len(oext2)>0:
        oext=oext2

    if oext.startswith('.'):
        oext=oext[1:]

    return opath, ofname, otag, oext




if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
        sys.exit()

    FFMPEG_BIN = 'ffmpeg'

    help = utils.HELP(usage, FFMPEG_BIN, '--help',logger)
    #options = 'o:e:aC:T:E:m:t:'
    options = 'e:o:C:T:E:t:m:v'
    #try:
    #    opts, args = getopt.gnu_getopt(sys.argv[1:], options + help.get_opt())
    #except getopt.GetoptError as err:
    #    logger.error(str(err))
    #    sys.exit(2)
    #except Exception, e:
    #    logger.error(e)
    opts,args=utils.my_getopt(sys.argv[1:],options+help.get_opt())

    #output related
    output_path = ''
    output_fname = ''
    output_tag = ''
    output_ext = ''

    extra_cmd = ''
    #extension = ''
    muxer=''
    thread_num = ''
    #auto_audio_flag = 1
    width = -2
    height = -2
    startp = ''
    dura = ''
    endp = ''

    logger.info("opts=%s args=%s"%(opts,args))

    for opt, arg in opts:
        if opt == '-o':
            output_path, output_fname,output_tag,output_ext = parse_output(arg)
        elif opt == '-e':
            muxer= arg
        #elif opt == '-a':
        #    auto_audio_flag = 0
        elif opt == '-C':
            extra_cmd = arg
        elif opt == '-T':
            thread_num = arg
        elif opt == '-E':
            if ':' in arg:
                width, height = parse_reso(arg, width, height, ':')
            else:
                width, height = parse_reso(arg, width, height)
        elif opt == '-t':
            if '+' in arg:
                startp, dura = parse_time(arg, startp, dura)
            elif '-' in arg:
                startp, endp = parse_time(arg, startp, endp, '-')
        elif opt=='-v':
            logger.set_level('debug')
        else:
            help.parse_opt(opt)

    if len(args) == 0:
        logger.error('No input is specified, please check')
        sys.exit()

    input_list = []
    for arg in args:
        utils.get_input_file_list(input_list, arg)

    if len(input_list) == 0:
        logger.error('Input is invalid, please check')
        sys.exit()


    logger.info("opath=%s ofname=%s otag=%s oext=%s" %(output_path,output_fname,output_tag,output_ext))

    pre_cmd = FFMPEG_BIN
    pre_cmd += ' -y'

    post_cmd=''

    #if len(output_tag) == 0:  # =='':
    #    output_tag = "out"
    #output_tag+='out'

    #add option -threads
    if len(thread_num) > 0:
        post_cmd += ' -threads %s' % thread_num

    #add option duration
    if len(dura) > 0:
        if len(startp) > 0:
            pre_cmd += ' -ss %s' % startp
        pre_cmd += ' -t %s' % dura
    elif len(endp) > 0:
        if len(startp) > 0:
            post_cmd += ' -ss %s' % startp
        post_cmd += ' -to %s' % endp

    if width > 0 or height > 0:  # option -r: resize the input video file
        post_cmd += ' -vf scale=%s:%s' % (width, height)
        output_tag+='%sx%s'%(width,height)


    cmd_list = []
    output_list = []
    for input_file in input_list:
        print input_file
        if not os.path.isfile(input_file):
            logger.error('"%s" is not a file, but is in the input_list' % input_file)
            continue
        cmd_line, output_file = get_cmd_line(input_file, output_path, output_fname,output_tag,output_ext,
                                             pre_cmd, post_cmd,extra_cmd)
        #print cmd_line
        cmd_list.append(cmd_line)
        output_list.append(output_file)

    logger.info('FINAL COMMANDS:')
    for cmd in cmd_list:
        utils.run_cmd(cmd, help.get_do_execute())



