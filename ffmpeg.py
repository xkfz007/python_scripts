#!/usr/bin/python
# The main purpose of this script is to wrap the ffmpeg.exe
# so that we will not have to give the exact input file name or output file name.
# Right now, we just need give the glob pattern of the input file name
# and this is very useful for the Chinese file or directory names
__author__ = 'hfz2597'
import sys
import getopt
import os
import subprocess
import glob
import lib
import logging

from ffprobe import FFProbe


class AVFormat:
    def __init__(self,name,extensions,description):
        self.name=name
        self.extensions=extensions.split(',')
        self.description=description

vfmt_list=[
    AVFormat('asf',           'asf,wmv,wma',              'ASF (Advanced / Active Streaming Format)'),
    AVFormat('avi',           'avi',                      'AVI (Audio Video Interleaved)'),
    AVFormat('f4v',           'f4v',                      'F4V Adobe Flash Video'),
    AVFormat('flv',           'flv',                      'FLV (Flash Video)'),
    AVFormat('h261',          'h261',                     'raw H.261'),
    AVFormat('h263',          'h263',                     'raw H.263'),
    AVFormat('h264',          'h264,264,avc',             'raw H.264 video'),
    AVFormat('hevc',          'hevc,265,h265',            'raw HEVC video'),
    AVFormat('m4v',           'm4v',                      'raw MPEG-4 video'),
    AVFormat('matroska',      'mkv,mka',                  'Matroska'),
    AVFormat('mmf',           'mmf',                      'Yamaha SMAF'),
    AVFormat('mov',           'mov',                      'QuickTime / MOV'),
    AVFormat('mp4',           'mp4',                      'MP4 (MPEG-4 Part 14)'),
    AVFormat('mpeg',          'mpg,mpeg',                 'MPEG-1 Systems / MPEG program stream'),
    AVFormat('mpeg1video',    'mpg,mpeg,m1v',             'raw MPEG-1 video'),
    AVFormat('mpeg2video',    'm2v',                      'raw MPEG-2 video'),
    AVFormat('mpegts',        'ts,m2t,m2ts,mts',          'MPEG-TS (MPEG-2 Transport Stream)'),
    AVFormat('mxf',           'mxf',                      'MXF (Material eXchange Format)'),
    AVFormat('rawvideo',      'yuv,rgb',                  'raw video'),
    AVFormat('rm',            'rm,ra,rmvb',               'RealMedia'),
    AVFormat('swf',           'swf',                      'SWF (ShockWave Flash)'),
    AVFormat('vc1',           'vc1',                      'raw VC-1 video'),
    AVFormat('yuv4mpegpipe',  'y4m',                      'YUV4MPEG pipe'),

]
afmt_list=[
    AVFormat('ac3',          'ac3',                      'raw AC-3'),
    AVFormat('adts',          'aac',                      'ADTS AAC (Advanced Audio Coding)'),
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

fmt_list=vfmt_list+afmt_list+ifmt_list

vfmt_dict={}
afmt_dict={}
ifmt_dict={}

vext_dict={}
aext_dict={}
iext_dict={}

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
     -m <string>  merge the input media files to one, only mp4 and mkv is supported
   ARGUMENTS:
     file or directory, support pattern globbing,these are the input files that will be processed
   '''
    print help_msg
    return

def detect_file(input_file):
    m = FFProbe(input_file)
    vst=m.video
    assert len(vst)<=1
    ast=m.audio
    sst=m.subtitle
    fmt=m.format

    return fmt,vst,ast,sst


def get_cmd_line(input_file, ofpath, ofname, oftag, ofext,  prepared_cmd, extra_cmd):
    infdir, infile = os.path.split(input_file)
    infname, infext = os.path.splitext(infile)
    if infext.startswith('.'):
        infext=infext[1:]

    #detect file info
    inf_fmt,inf_vst,inf_ast,inf_sst=detect_file(input_file)
    #if infext.lower() not in fmt_dict[inf_fmt.format].extensions:
    #    logging.warning('Invaild extension of %s, it should be %s'%(infext,fmt_list[inf_fmt.format].extensions))
    #    infext=fmt_list[inf_fmt.format].extensions[0]

    #normalize the output
    if len(ofpath) == 0:
        ofpath = infdir
    if len(ofname)==0:
        ofname=infname
    if len(ofext)==0:
        ofext=infext

    if ofname==infname:#add tag to distinguish in and out
        oftag+='out'

    logging.info('ofname="%s" ofext="%s"' % (ofname,ofext))

    cdec_cmd=''
    #input is video and output is audio, this means audio will be extracted from video
    if infext in vext_dict.keys():
        cdec_cmd+=' -c:a copy'
        if ofext in vext_dict.keys():
            if len(inf_sst)>0:
                cdec_cmd+=' -c:s copy'
        elif ofext in aext_dict.keys():
            ofext=afmt_dict[inf_ast[0].codec()].extensions[0]
            cdec_cmd+=' -vn'

    ofmt=ext_dict[ofext]
    fmt_cmd='-f %s'%ofmt.name
    #if input is mp4 or mkv format and codec is h264, h264_mp4toannexb is needed
    if infext in bsf_for_mp4_ext_list and ofext not in bsf_for_mp4_ext_list\
            and inf_vst[0].codec() in bsf_for_mp4.keys()\
            and ofext in vext_dict.keys():
        fmt_cmd+=' -bsf:v %s'%bsf_for_mp4[inf_vst[0].codec()]

    #cdec_md=''
    #if len(cdec_md)==0:
    #    cdec_cmd='-map 0 -c copy'

    #output_file = '%s_%s.%s' % (ofname, oftag, ofext)
    output_file=ofname
    if len(oftag)>0:
        output_file+='_'+oftag
    output_file+='.'+ofext
    if len(ofpath) > 0:
        output_file = '%s%s%s' % (ofpath, os.sep, output_file)

    cmd_line = prepared_cmd
    cmd_line += ' -i "%s"' % input_file
    cmd_line += ' %s' % cdec_cmd
    cmd_line += ' %s' % fmt_cmd
    cmd_line += ' %s' % extra_cmd
    cmd_line += ' "%s"' % output_file
    return (cmd_line, output_file)


def parse_reso(arg, width=-2, height=-2, delimiter='x'):
    x, y = lib.parse_arg(arg, delimiter, str(width), str(height))
    return int(x), int(y)


def parse_time(arg, startp='', dura='', delimiter='+'):
    x, y = lib.parse_arg(arg, delimiter, startp, dura)
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
    opath, otag_oext = lib.parse_arg(arg, delimiter, default_opath, default_otag_oext)
    logging.info('opth=%s,otag_oext=%s' % (opath, otag_oext))
    ofname_oext=''
    if '.' in opath:#format like: movies/conan/1.mp4
        opath, ofname_oext= os.path.split(opath)

    logging.info('opth=%s,ofname_oext=%s,otag_oext=%s' % (opath, ofname_oext,otag_oext))
    if len(opath) > 0 and not os.path.isdir(opath):
        #opt = raw_input('Directory "%s" does not exist, do you want to create it?(Y/N)' % opath)
        #if opt.lower() in 'yes':
        #    os.makedirs(opath)
        #    logging.info('Diectory "%s" is created.' % arg)
        #else:
        #    logging.error('Diectory "%s" does not exist, using the current directory' % opath)
        #    opath='.'
        if len(ofname_oext)==0:
            logging.warning('Directory does not exist, filename will be created')
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

    help = lib.common_lib.HELP(usage, FFMPEG_BIN, '--help')
    #options = 'o:e:aC:T:E:m:t:'
    options = 'o:C:T:E:t:m:'
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], options + help.get_opt())
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    except Exception, e:
        print e

    #output related
    output_path = ''
    output_fname = ''
    output_tag = ''
    output_ext = ''

    #merged file related
    #merged_path=''
    #merged_fname=''
    #merged_tag=''
    #merged_ext=''
    merged_file = ''

    extra_cmd = ''
    #extension = ''
    thread_num = ''
    #auto_audio_flag = 1
    width = -2
    height = -2
    startp = ''
    dura = ''
    endp = ''

    logging.info("opts=%s args=%s"%(opts,args))

    for opt, arg in opts:
        if opt == '-o':
            output_path, output_fname,output_tag,output_ext = parse_output(arg)
        #elif opt == '-e':
        #    extension = arg
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
        elif opt == '-m':
            merged_file=arg
            #merged_path, merged_fname,merged_tag,merged_ext = parse_output(merged_file)
            #mflag=1
        elif opt == '-t':
            if '+' in arg:
                startp, dura = parse_time(arg, startp, dura)
            elif '-' in arg:
                startp, endp = parse_time(arg, startp, endp, '-')
        else:
            help.parse_opt(opt)

    if len(args) == 0:
        logging.error('No input is specified, please check')
        sys.exit()

    input_list = []
    for arg in args:
        lib.get_input_file_list(input_list, arg)

    if len(input_list) == 0:
        logging.error('Input is invalid, please check')
        sys.exit()


    logging.info("opath=%s ofname=%s otag=%s oext=%s" %(output_path,output_fname,output_tag,output_ext))
    #logging.info("mpath=%s mfname=%s mtag=%s mext=%s" %(merged_path,merged_fname,merged_tag,merged_ext))

    if len(merged_file)>0:
        output_ext='ts'

    prepared_cmd = FFMPEG_BIN
    prepared_cmd += ' -y'

    #if len(output_tag) == 0:  # =='':
    #    output_tag = "out"
    #output_tag+='out'

    #add option -threads
    if len(thread_num) > 0:
        prepared_cmd += ' -threads %s' % thread_num

    #add option duration
    if len(dura) > 0:
        if len(startp) > 0:
            prepared_cmd += ' -ss %s' % startp
        prepared_cmd += ' -t %s' % dura
    elif len(endp) > 0:
        if len(startp) > 0:
            extra_cmd += ' -ss %s' % startp
        extra_cmd += ' -to %s' % endp

    if width > 0 or height > 0:  # option -r: resize the input video file
        extra_cmd += ' -vf scale=%s:%s' % (width, height)
        output_tag+='%sx%s'%(width,height)


    cmd_list = []
    output_list = []
    for input_file in input_list:
        print input_file
        if not os.path.isfile(input_file):
            logging.error('"%s" is not a file, but is in the input_list' % input_file)
            continue
        cmd_line, output_file = get_cmd_line(input_file, output_path, output_fname,output_tag,output_ext,
                                             prepared_cmd, extra_cmd)
        print cmd_line
        cmd_list.append(cmd_line)
        output_list.append(output_file)

    if len(merged_file) > 0:
        concat_str = "|".join(output_list)
        print concat_str
        cmd_line = FFMPEG_BIN
        #cmd_line += ' -i "concat:%s" -c copy -bsf:a aac_adtstoasc %s' % (concat_str, merged_file)
        cmd_line += ' -i "concat:%s" -c:v copy -c:a pcm_alaw %s' % (concat_str, merged_file)
        print cmd_line
        cmd_list.append(cmd_line)


    logging.info('FINAL COMMANDS:')
    for cmd in cmd_list:
        lib.run_cmd(cmd, help.get_do_execute())



