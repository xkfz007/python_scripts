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

    def format(self):
        """
        Returns a string representation of the format.
        """
        format_name = None
        if self.__dict__['format_name']:
            format_name = self.__dict__['format_name']
        return format_name

    def formatDescription(self):
        """
        Returns a long representation of the format.
        """
        format_d = None
        if self.__dict__['format_long_name']:
            format_d = self.__dict__['format_long_name']
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

    def isAudio(self):
        """
        Is this stream labelled as an audio stream?
        """
        val = False
        if self.__dict__['codec_type']:
            if str(self.__dict__['codec_type']) == 'audio':
                val = True
        return val

    def isVideo(self):
        """
        Is the stream labelled as a video stream.
        """
        val = False
        if self.__dict__['codec_type']:
            if self.__dict__['codec_type'] == 'video':
                val = True
        return val

    def isSubtitle(self):
        """
        Is the stream labelled as a subtitle stream.
        """
        val = False
        if self.__dict__['codec_type']:
            if str(self.__dict__['codec_type']) == 'subtitle':
                val = True
        return val

    def frameSize(self):
        """
        Returns the pixel frame size as an integer tuple (width,height) if the stream is a video stream.
        Returns None if it is not a video stream.
        """
        size = None
        if self.isVideo():
            if self.__dict__['width'] and self.__dict__['height']:
                try:
                    size = (int(self.__dict__['width']), int(self.__dict__['height']))
                except Exception as e:
                    print "None integer size %s:%s" % (str(self.__dict__['width']), str(+self.__dict__['height']))
                    size = (0, 0)
        return size

    def pixelFormat(self):
        """
        Returns a string representing the pixel format of the video stream. e.g. yuv420p.
        Returns none is it is not a video stream.
        """
        f = None
        if self.isVideo():
            if self.__dict__['pix_fmt']:
                f = self.__dict__['pix_fmt']
        return f

    def frames(self):
        """
        Returns the length of a video stream in frames. Returns 0 if not a video stream.
        """
        f = 0
        if self.isVideo() or self.isAudio():
            if self.__dict__['nb_frames']:
                try:
                    f = int(self.__dict__['nb_frames'])
                except Exception as e:
                    print "None integer frame count"
        return f

    def durationSeconds(self):
        """
        Returns the runtime duration of the video stream as a floating point number of seconds.
        Returns 0.0 if not a video stream.
        """
        f = 0.0
        if self.isVideo() or self.isAudio():
            if self.__dict__['duration']:
                try:
                    f = float(self.__dict__['duration'])
                except Exception as e:
                    print "None numeric duration"
        return f

    def language(self):
        """
        Returns language tag of stream. e.g. eng
        """
        lang = None
        if self.__dict__['TAG:LANGUAGE']:
            lang = self.__dict__['TAG:LANGUAGE']
        return lang

    def codec(self):
        """
        Returns a string representation of the stream codec.
        """
        codec_name = None
        if self.__dict__['codec_name']:
            codec_name = self.__dict__['codec_name']
        return codec_name

    def codecDescription(self):
        """
        Returns a long representation of the stream codec.
        """
        codec_d = None
        if self.__dict__['codec_long_name']:
            codec_d = self.__dict__['codec_long_name']
        return codec_d

    def codecTag(self):
        """
        Returns a short representative tag of the stream codec.
        """
        codec_t = None
        if self.__dict__['codec_tag_string']:
            codec_t = self.__dict__['codec_tag_string']
        return codec_t


    def bitrate(self):
        """
        Returns bitrate as an integer in bps
        """
        b = 0
        if self.__dict__['bit_rate']:
            try:
                b = int(self.__dict__['bit_rate'])
            except Exception as e:
                print "None integer bitrate"
        return b

    def fps(self):
        """
        Returns the runtime duration of the video stream as a floating point number of seconds.
        Returns 0.0 if not a video stream.
        """
        f = 0.0
        if self.isVideo():
            if self.__dict__['avg_frame_rate']:
                try:
                    f = float(self.__dict__['avg_frame_rate'])
                except Exception as e:
                    print "None numeric duration"
        return f

    def video_rotate(self):
        """
        Returns bitrate as an integer in bps
        """
        b = 0
        try:
            b = int(self.__dict__['TAG:rotate'])
        except Exception as e:
            print "None integer TAG:rotate"
        return b

    def image_rotate(self):
        """
        Returns bitrate as an integer in bps
        """
        b = 0
        try:
            b = int(self.__dict__['TAG:Orientation'])
        except Exception as e:
            print "None integer TAG:Orientation"
        return b

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
            cmd = "ffprobe -show_streams " + input_file
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

            cmd = "ffprobe -show_format " + input_file
            tmp_formats=get_ffinfo(cmd,'FORMAT')
            assert len(tmp_formats)==1
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

