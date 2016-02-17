#!/bin/python
__author__ = 'Felix'
import sys
sys.path.append('..')
import lib
import logging
import os.path

from ffprobe import FFProbe

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
    otag=''
    ofname=''
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

    return opath, ofname, otag, oext

#matroska
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

def detect_file(input_file):
    m = FFProbe(input_file)
    vst=m.video
    assert len(vst)==1
    ast=m.audio
    sst=m.subtitle
    fmt=m.format

    return fmt,vst,ast,sst



def get_cmd_line(input_file, ofpath, ofname, oftag, ofext,  prepared_cmd, extra_cmd):
    infdir, infile = os.path.split(input_file)
    infname, infext = os.path.splitext(infile)

    #detect file info
    inf_fmt,inf_vst,inf_ast,inf_sst=detect_file(input_file)
    if infext.lower() not in fmt_dict[inf_fmt.formatName].extensions:
        logging.warning('Invaild extension of %s, it should be %s'%(infext,fmt_list[inf_fmt.formatName].extensions))
        infext=fmt_list[inf_fmt.formatName].extensions[0]

    #normalize the output
    if len(ofpath) == 0:
        ofpath = infdir
    if len(ofname)==0:
        ofname=infname
    if len(ofext)==0:
        ofext=infext

    logging.info('ofname="%s" ofext="%s"' % (ofname,ofext))

    cdec_cmd=''
    #input is video and output is audio, this means audio will be extracted from video
    if infext in vext_dict.keys():
        cdec_cmd+=' -c:a copy'
        if ofext in vext_dict.keys():
            if len(inf_sst)>0:
                cdec_cmd+=' -c:s copy'
        elif ofext in aext_dict.keys():
            ofext=afmt_dict[inf_ast.name].extensions[0]
            cdec_cmd+=' -vn'

    ofmt=ext_dict[ofext]
    fmt_cmd='-f %s'%ofmt.name
    #if input is mp4 or mkv format and codec is h264, h264_mp4toannexb is needed
    if ( infext in fmt_dict['matroska'].extensions or
        infext in fmt_dict['mp4'].extensions ) and inf_vst.name in bsf_for_mp4.keys():
        fmt_cmd+=' -bsf:v %s'%bsf_for_mp4[inf_vst.name]

    #cdec_md=''
    #if len(cdec_md)==0:
    #    cdec_cmd='-map 0 -c copy'

    output_file = '%s_%s.%s' % (ofname, oftag, ofext)
    if len(ofpath) > 0:
        output_file = '%s%s%s' % (ofpath, os.sep, output_file)

    cmd_line = prepared_cmd
    cmd_line += ' -i "%s"' % input_file
    cmd_line += ' %s' % cdec_cmd
    cmd_line += ' %s' % fmt_cmd
    cmd_line += ' %s' % extra_cmd
    cmd_line += ' "%s"' % output_file
    return (cmd_line, output_file)

if __name__ == '__main__':

    while 1:
       a=raw_input()
       print parse_output(a)
