#!/usr/bin/python
# Filename: ffprobe.py
"""
Python wrapper for ffprobe command line tool. ffprobe must exist in the path.
"""

import subprocess
import re
import sys
import os
import platform

class FFFormat:
    def __init__(self, datalines):
        for a in datalines:
            try:
                (key, val) = a.strip().split('=')
                self.__dict__[key] = val
            except:
                b = 1

    def formatName(self,tag='format_name'):
        """
        Returns a string representation of the format.
        """
        format_name = None
        if self.__dict__[tag]:
            format_name = self.__dict__[tag]
        return format_name

    def formatDescription(self,tag='format_long_name'):
        """
        Returns a long representation of the format.
        """
        format_d = None
        if self.__dict__[tag]:
            format_d = self.__dict__[tag]
        return format_d

class FFStream:
    """
    An object representation of an individual stream in a multimedia file.
    """

    def __init__(self, datalines):
        for a in datalines:
            try:
                (key, val) = a.strip().split('=')
                self.__dict__[key] = val
            except:
                b = 1

    def isAudio(self,tag='codec_type'):
        val = False
        if self.__dict__[tag]:
            if str(self.__dict__[tag]) == 'audio':
                val = True
        return val

    def isVideo(self,tag='codec_type'):
        val = False
        if self.__dict__[tag]:
            if self.__dict__[tag] == 'video':
                val = True
        return val

    def isSubtitle(self,tag='codec_type'):
        val = False
        if self.__dict__[tag]:
            if str(self.__dict__[tag]) == 'subtitle':
                val = True
        return val

    def frameSize(self,tag1='width',tag2='height'):
        size = None
        if self.isVideo():
            if self.__dict__[tag1] and self.__dict__[tag2]:
                try:
                    size = (int(self.__dict__[tag1]), int(self.__dict__[tag2]))
                except Exception as e:
                    print "None integer size %s:%s" % (str(self.__dict__[tag1]), str(+self.__dict__[tag2]))
                    size = (0, 0)
        return size

    def pixelFormat(self,tag='pix_fmt'):
        f = None
        if self.isVideo():
            if self.__dict__[tag]:
                f = self.__dict__[tag]
        return f

    def frames(self,tag='nb_frames'):
        f = 0
        if self.isVideo() or self.isAudio():
            if self.__dict__[tag]:
                try:
                    f = int(self.__dict__[tag])
                except Exception as e:
                    print "None integer frame count"
        return f

    def durationSeconds(self,tag='duration'):
        f = 0.0
        if self.isVideo() or self.isAudio():
            if self.__dict__[tag]:
                try:
                    f = float(self.__dict__[tag])
                except Exception as e:
                    print "None numeric duration"
        return f

    def language(self,tag='TAG:language'):
        lang = None
        if self.__dict__[tag]:
            lang = self.__dict__[tag]
        return lang

    def codecName(self,tag='codec_name'):
        codec_name = None
        if self.__dict__[tag]:
            codec_name = self.__dict__[tag]
        return codec_name

    def codecDescription(self,tag='codec_long_name'):
        codec_d = None
        if self.__dict__[tag]:
            codec_d = self.__dict__[tag]
        return codec_d

    def codecTag(self,tag='codec_tag_string'):
        codec_t = None
        if self.__dict__[tag]:
            codec_t = self.__dict__[tag]
        return codec_t


    def bitrate(self,tag='bit_rate'):
        b = 0
        if self.__dict__[tag]:
            try:
                b = int(self.__dict__[tag])
            except Exception as e:
                print "None integer bitrate"
        return b

    def fps(self,tag='avg_frame_rate'):
        f = 0.0
        if self.isVideo():
            if self.__dict__[tag]:
                try:
                    f = float(self.__dict__[tag])
                except Exception as e:
                    print "None numeric duration"
        return f

    def index(self):
        idx = 0
        try:
            idx = int(self.__dict__['index'])
        except Exception as e:
            print "None index"
        return idx

FFTYPE_LIST={'STREAM':FFStream,
             'FORMAT':FFFormat,}


def get_fftype(streams,lines,tag):
    datalines=[]
    FFTYPE=FFTYPE_LIST[tag.upper()]
    start_tag='\['+tag.upper()+'\]'
    end_tag='\[\/'+tag.upper()+'\]'
    for a in iter(lines, b''):
        if re.match(start_tag, a):
            datalines = []
        elif re.match(end_tag, a):
            streams.append(FFTYPE(datalines))
            datalines = []
        else:
            datalines.append(a)


def get_ffinfo(cmd,tag):
    streams = []
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    get_fftype(streams,p.stdout.readline,tag)
    get_fftype(streams,p.stderr.readline,tag)
    #datalines=[]
    #FFTYPE=FFTYPE_LIST[tag.upper()]
    #start_tag='\['+tag.upper()+'\]'
    #end_tag='\[\/'+tag.upper()+'\]'
    #for a in iter(p.stdout.readline, b''):
    #    if re.match(start_tag, a):
    #        datalines = []
    #    elif re.match(end_tag, a):
    #        streams.append(FFTYPE(datalines))
    #        datalines = []
    #    else:
    #        datalines.append(a)

    #for a in iter(p.stderr.readline, b''):
    #    if re.match(start_tag, a):
    #        datalines = []
    #    elif re.match(end_tag, a):
    #        streams.append(FFTYPE(datalines))
    #        datalines = []
    #    else:
    #        datalines.append(a)
    p.stdout.close()
    p.stderr.close()
    return streams

#def get_format(formats,lines):
#    datalines=[]
#    tag='FORMAT'
#    start_tag='\['+tag.upper()+'\]'
#    end_tag='\[\/'+tag.upper()+'\]'
#    for a in iter(lines, b''):
#        if re.match(start_tag, a):
#            datalines = []
#        elif re.match(end_tag, a):
#            formats.append(FFStream(datalines))
#            datalines = []
#        else:
#            datalines.append(a)
class FFProbe:
    """
    FFProbe wraps the ffprobe command and pulls the data into an object form::
      metadata=FFProbe('multimedia-file.mov')
    """
    # type = 0 image, 1 video, 2 audio
    def __init__(self, input_file):
        #self.input_file = input_file

        # the following check are removed to improve speed
        # try:
        # with open(os.devnull, 'w') as tempf:
        #     subprocess.check_call(["ffprobe", "-h"], stdout=tempf, stderr=tempf)
        # except:
        #   raise IOError('ffprobe not found.')

        if os.path.isfile(input_file):
            #if str(platform.system()) == 'Windows':
            #    cmd = ["ffprobe", "-show_streams", input_file]
            #else:
            #    cmd = ["ffprobe -show_streams " + input_file]
            cmd = 'ffprobe -show_streams "%s"'%input_file
            self.video = []
            self.audio = []
            self.subtitle=[]
            tmp_streams=get_ffinfo(cmd,'STREAM')
            for a in tmp_streams:
                if a.isAudio():
                    self.audio.append(a)
                elif a.isVideo():
                    self.video.append(a)
                elif a.isSubtitle():
                    self.subtitle.append(a)

            cmd = 'ffprobe -show_format "%s"'% input_file
            tmp_formats=get_ffinfo(cmd,'FORMAT')
            #print tmp_formats
            #assert len(tmp_formats)==1
            if len(tmp_formats)<1:
                print 'Invaild format, please check'
                sys.exit()
            self.format=tmp_formats[0]


if __name__ == '__main__':
    print "Module ffprobe"
    m = FFProbe("e:/movies/conan/[APTX4869][CONAN][689][480P][AVC_AAC][CHS](A29CF385).mp4")
    for s in m.streams:
        if s.isVideo():
            framerate = s.frames() / s.durationSeconds()
            print framerate
            print s.frameSize()
        print s.durationSeconds()
        print s.frames()
        print s.isVideo()

