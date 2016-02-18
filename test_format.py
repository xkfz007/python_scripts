#!/bin/python
class AVFormat:
    def __init__(self,name,extensions,description):
        self.name=name
        self.extensions=extensions.split(',')
        self.description=description

fmt_list=[
AVFormat('asf',           'asf,wmv,wma',              'ASF (Advanced / Active Streaming Format)'),
AVFormat('avi',           'avi',                      'AVI (Audio Video Interleaved)'),
AVFormat('adts',          'aac',                      'ADTS AAC (Advanced Audio Coding)'),
AVFormat('f4v',           'f4v',                      'F4V Adobe Flash Video'),
AVFormat('flac',          'flac',                     'raw FLAC'),
AVFormat('flv',           'flv',                      'FLV (Flash Video)'),
AVFormat('gif',           'gif',                      'GIF Animation'),
AVFormat('h261',          'h261',                     'raw H.261'),
AVFormat('h263',          'h263',                     'raw H.263'),
AVFormat('h264',          'h264,264,avc',             'raw H.264 video'),
AVFormat('hevc',          'hevc,265,h265',            'raw HEVC video'),
AVFormat('image2',        'bmp,jpeg,jpg,png,tiff',    'image2 sequence'),
AVFormat('m4v',           'm4v',                      'raw MPEG-4 video'),
AVFormat('matroska',      'mkv,mka',                  'Matroska'),
AVFormat('mmf',           'mmf',                      'Yamaha SMAF'),
AVFormat('mov',           'mov',                      'QuickTime / MOV'),
AVFormat('mp2',           'mp2,mpa,m2a',              'MP2 (MPEG audio layer 2)'),
AVFormat('mp3',           'mp3',                      'MP3 (MPEG audio layer 3)'),
AVFormat('mp4',           'mp4',                      'MP4 (MPEG-4 Part 14)'),
AVFormat('mpeg',          'mpg,mpeg',                 'MPEG-1 Systems / MPEG program stream'),
AVFormat('mpeg1video',    'mpg,mpeg,m1v',             'raw MPEG-1 video'),
AVFormat('mpeg2video',    'm2v',                      'raw MPEG-2 video'),
AVFormat('mpegts',        'ts,m2t,m2ts,mts',          'MPEG-TS (MPEG-2 Transport Stream)'),
AVFormat('mxf',           'mxf',                      'MXF (Material eXchange Format)'),
AVFormat('oga',           'oga',                      'Ogg Audio'),
AVFormat('ogg',           'ogg',                      'Ogg'),
AVFormat('rawvideo',      'yuv,rgb',                  'raw video'),
AVFormat('rm',            'rm,ra,rmvb',               'RealMedia'),
AVFormat('swf',           'swf',                      'SWF (ShockWave Flash)'),
AVFormat('vc1',           'vc1',                      'raw VC-1 video'),
AVFormat('wav',           'wav',                      'WAV / WAVE (Waveform Audio)'),
AVFormat('yuv4mpegpipe',  'y4m',                      'YUV4MPEG pipe'),
]
fmt_dict={}
ext_dict={}
for i in fmt_list:
   fmt_dict[i.name]=i
   for j in i.extensions:
       ext_dict[j]=i

print "fmt_dict:"
for (k,v) in fmt_dict.items():
    print '\t[%s %s]'%(k,v.description)

print "ext_dict:"
for (k,v) in ext_dict.items():
    print '\t[%s %s]'%(k,v.name)
