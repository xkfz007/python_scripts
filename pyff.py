#!/bin/python
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

FFMPEG_BIN = 'ffmpeg.exe -y'

h264_name_list = ('h264', 'h.264', 'avc', '264')
h265_name_list = ('h265', 'h.265', 'hevc', '265')
bsf_for_mp4 = {'h264': 'h264_mp4toannexb',
               'hevc': 'hevc_mp4toannexb'}
bitstream_name_list=h264_name_list+h265_name_list
yuv_name_list=('yuv','y4m')
mp4_name_list=('mp4','flv','mkv','f4v')
avi_name_list=('avi',)
video_name_list=mp4_name_list+avi_name_list
audio_name_list=('aac','mp3','ogg')

valid_ext_list=h264_name_list+h265_name_list+yuv_name_list+video_name_list+audio_name_list


def usage():
    help_msg = '''Usage:pyff.py [option] <input1> <input2> ...
  options:
   -e <string> the output file extension
      h264/hevc: get the raw bitstream from media file
      yuv: decode the input to get rawvideo(yuv)
      aac,mp3: extract audio from media file
   -a extract audio using the extra command lines from -C,
      ignore the auto generated command lines from extension(-e)
   -o <string> output file tag
   -C <string> the ffmpeg commands
   -t <int> set thread num
   -w <int> set the output width
   -h <int> set the output height
   -m <string> merge the input media files to one
   -Y whether to execute the program
   -H print the FFMpeg help
   arguments:
   <input1> <input2> <input3> file or directory, support pattern globbing
           these are the input files that will be processed
   '''
    print help_msg
    return


def get_cmd_line(input_file, ext, output_tmp, prepared_cmd, extra_cmd):
    fname, fext = os.path.splitext(input_file)
    print 'fname="%s"' % fname
    print 'fext="%s"' % fext
    fext=fext.lower()[1:]
    if ext=='TS' and fext=='ts':
        return ''

    if len(ext) == 0 :
        if len(fext)>0:
            ext = fext
        else:#set default ext
            ext='ext'
    elif len(ext) > 0:
        if ext in bitstream_name_list and fext in mp4_name_list:#'mp4':
            extra_cmd += " -bsf:v %s" % bsf_for_mp4[ext]
        #elif ext in audio_name_list:
        #    if fext in mp4_name_list:
        #        extra_cmd+=" -c:a copy"
        if ext=='TS':
            if fext in mp4_name_list:
                extra_cmd+=" -c copy"
                #if fext=='mp4':
                extra_cmd += " -bsf:v %s -f mpegts" % bsf_for_mp4['h264']
            else:
                extra_cmd+=" -c:v libx264 -c:a libvo_aacenc"


    output_file = "%s%s.%s" % (fname, output_tmp, ext)

    cmd_line = prepared_cmd
    cmd_line += " -i \"%s\"" % input_file
    cmd_line += " %s" % extra_cmd
    cmd_line += " \"%s\"" % output_file
    return (cmd_line,output_file)


def get_default_opt_list():
    opt_list = {}
    # opt_list['input_tmp'] = ''
    opt_list['extra_cmd'] = ''
    opt_list['ext'] = ''
    # opt_list['output_tmp'] = ''
    opt_list['thread_num'] = 0
    opt_list['do_execute'] = 0
    return opt_list

def get_ffmpeg_opt_list():
    ff_opt_list={}
    ff_opt_list['input_file']=''
    ff_opt_list['vcodec']=''
    ff_opt_list['acodec']=''
    return ff_opt_list

def get_input_list(input_list,input_tmp):
    print "input_tmp=%s" % input_tmp
    #if len(input_tmp) == 0:
    #    usage()

    if os.path.isdir(input_tmp):
        print '"%s" is a directory' % input_tmp
        input_list.extend(lib.get_file_list(input_tmp))
    elif os.path.isfile(input_tmp):
        print '"%s" is a file' % input_tmp
        #input_list = []
        input_list.append(input_tmp)
    else:  # globbing is needed
        print '"%s" is glob pattern' % input_tmp
        glob_list=glob.glob(input_tmp)
        for i in glob_list:
            get_input_list(input_list,i)
    # print type(input_file)
    #print "input_list=%s" % input_list


if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
        sys.exit()

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'o:e:aC:t:w:h:m:YH')
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    except Exception, e:
        print e

    # opt_list = get_default_opt_list()
    input_tmp = ''
    output_tmp = ''
    extra_cmd = ''
    extension = ''
    thread_num = 0
    do_execute = 0
    #decode_flag = 0
    #bitstream_type = ""
    auto_audio_flag=1
    width=-2
    height=-2
    merged_file=''
    print opts
    print args

    for opt, arg in opts:
        if opt == "-o":
            output_tmp = arg
        elif opt == "-e":
            extension = arg
        elif opt == "-a":
            auto_audio_flag= 0
        elif opt == "-C":
            extra_cmd = arg
        elif opt == "-t":
            thread_num = int(arg)
        elif opt == "-w":
            width= int(arg)
        elif opt == "-h":
            height= int(arg)
        elif opt=="-m":
            merged_file=arg
        elif opt == "-Y":
            do_execute = 1
        elif opt == "-H":
            cmd_line = FFMPEG_BIN + " -h"
            os.system(cmd_line)
            sys.exit()
        else:
            assert False, "unknown option"

    if len(args) == 0:
        print "Error: No input is specified, please check"
        sys.exit()
    input_list=[]
    for arg in args:
        get_input_list(input_list,arg)

    if len(input_list) == 0:
        print "Error: Input is invalid, please check"
        sys.exit()

    if len(output_tmp) == 0:  # =='':
        output_tmp = "_out"
    else:
        if not output_tmp.startswith('_'):
            output_tmp = '_' + output_tmp
    print "output_tmp=%s"%output_tmp

    prepared_cmd = FFMPEG_BIN
    if thread_num > 0:
        prepared_cmd += " -threads %s" % thread_num

    if len(merged_file)>0:
        extension='TS'
    elif len(extension)>0 :
        if extension.startswith('.'):
           extension =  extension[1:]
        extension=extension.lower()
        if not extension in valid_ext_list:
            print "Error: invaild extension, please check"
            sys.exit()

        if extension in yuv_name_list:# decode to get raw yuv
            output_tmp = '_rec'
            extra_cmd += " -an -f rawvideo"
        elif extension in bitstream_name_list:# just get the raw stream
            output_tmp= '_bin'
            if extension in h264_name_list:
                extension= 'h264'
            elif extension in h265_name_list:
                extension= 'hevc'
            extra_cmd += " -c:v copy"
            extra_cmd += " -an -f %s" % extension
        elif extension in audio_name_list:
            output_tmp='_aud'
            extra_cmd+=" -vn"
            if auto_audio_flag==1:
                extra_cmd+=" -c:a copy"
            else:
                extra_cmd+=" -b:a 64k"#set bitrate for audio

    elif width>0 or height >0:
        extra_cmd += " -c:a copy"
        extra_cmd+=" -vf scale=%s:%s"%(width,height)


    cmd_list = []
    output_list=[]
    for input_file in input_list:
        print input_file
        if not os.path.isfile(input_file):
            print 'Error: "%s" is not file, but is in the input_list'%input_file
        cmd_line,output_file = get_cmd_line(input_file, extension, output_tmp, prepared_cmd, extra_cmd)
        print cmd_line
        cmd_list.append(cmd_line)
        output_list.append(output_file)
        #elif os.path.isdir(input_file):
        #    print '"%s" is a directory' % input_file
        #    input_file_list2 = lib.get_file_list(input_file)
        #    print "input_file_list2=%s" % input_file_list2
        #    for input_file2 in input_file_list2:
        #        cmd_line = get_cmd_line(input_file2, extension, output_tmp, prepared_cmd, extra_cmd)
        #        print cmd_line
        #        cmd_list.append(cmd_line)
    if len(merged_file)>0:
        concat_str = "|".join(output_list)
        print concat_str
        cmd_line = FFMPEG_BIN
        cmd_line += ' -i "concat:%s" -c copy -bsf:a aac_adtstoasc %s' % (concat_str, merged_file)
        print cmd_line
        cmd_list.append(cmd_line)


    if do_execute == 1:
        for cmd in cmd_list:
            if len(cmd)==0:
                continue
            print cmd
            # os.system(cmd)
            subprocess.call(cmd, stdout=None, stderr=None, shell=True)
        if len(merged_file)>0:
            for i in output_list:
                if os.path.exists(i):
                    os.remove(i)
                    print '"%s" is deleted'%i



