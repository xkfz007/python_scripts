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
import logging

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

image_name_list=('jpg','jpeg','png','bmp')
gif_name_list=('gif',)

valid_ext_list=h264_name_list+h265_name_list+yuv_name_list+\
               video_name_list+audio_name_list+\
               image_name_list+gif_name_list


def usage():
    help_msg = '''Usage:pyff.py [option] <input1> <input2> ...
  options:
   -e <string> the output file extension
      h264/hevc: get the raw bitstream from media file
      yuv: decode the input to get rawvideo(yuv)
      aac,mp3: extract audio from media file
      jpg,png,bmp: extract images from media file
      gif:create a gif file from video file
   -a extract audio using the extra command lines from -C,
      ignore the auto generated command lines from extension(-e)
   -o <path>:<tag> output file path or file tag:
      <path>: if <path> is a dir, it is used, or it is regared as <tag>
   -C <string> the ffmpeg commands
   -T <int> set thread num
   -t <hour:minute:second.xxx-hour:minute:second.xxx> set the time duration
   -r <int>x<int> set the output width and height
   -m <filename> merge the input media files to one, only mp4 and mkv is supported
   arguments:
   <input1> <input2> <input3> file or directory, support pattern globbing
           these are the input files that will be processed
   '''
    print help_msg
    return



def get_cmd_line(input_file, ext, output_path,output_tag, prepared_cmd, extra_cmd):
    indir,infile=os.path.split(input_file)
    if len(output_path)==0:
        output_path=indir
    assert len(infile)>0
    fname, fext = os.path.splitext(infile)
    print 'fname="%s"' % fname
    print 'fext="%s"' % fext
    fext=fext.lower()[1:]
    if ext=='TS' and fext=='ts':
        return ('',input_file)

    if len(ext) == 0 :
        if len(fext)>0:
            if fext in mp4_name_list:
               ext = fext
               extra_cmd += ' -c:a copy'
            else:# if the extension is rmvb, we will use mp4 for output file
                ext='mp4'
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

    output_file = "%s_%s.%s" % (fname, output_tag, ext)
    if '.' in output_tag:# regard there is an extension in output_tag
        output_file='%s.%s'%(output_tag,ext)

    if len(output_path)>0:
       output_file = "%s%s%s" % (output_path,os.sep, output_file)

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

def get_input_list(input_list,arg):

    if os.path.isdir(arg):
        logging.info('"%s" is a directory' % arg)
        input_list.extend(lib.get_file_list(arg))
    elif os.path.isfile(arg):
        logging.info('"%s" is a file' % arg)
        input_list.append(arg)
    else:  # globbing is needed
        glob_list=glob.glob(arg)
        logging.info('"%s" is glob pattern:%s' % (arg,glob_list))
        for i in glob_list:
            get_input_list(input_list,i)
    # print type(input_file)
    #print "input_list=%s" % input_list

def parse_arg(arg,X,Y,delimiter):
    cnt=arg.count(delimiter)
    if cnt>2:
        logging.error('Invalid arg:%s'%arg)
        sys.exit()
    elif cnt>0:
        x,y=arg.split(delimiter)
        if len(x)>0:
            X=x
        if len(y)>0:
            Y=y
    else:
        X=arg
    return X,Y

def parse_reso(arg,width=-2,height=-2,delimiter='x'):
    x,y=parse_arg(arg,str(width),str(height),delimiter)
    return int(x),int(y)

def parse_time(arg,startp='',dura='',delimiter='+'):
    x,y=parse_arg(arg,startp,dura,delimiter)
    return x,y

def parse_outpath(arg,output_path='',output_tag='',delimiter=':'):
    opath,otag=parse_arg(arg,output_path,output_tag,delimiter)
    #lib.check_path(opath)
    if not os.path.isdir(opath):
        if len(otag)>0:
           opt=input('Directory "%s" does not exist, do you want to create it?(Y/N)'%opath)
           if opt.lower() in 'yes':
               os.makedirs(opath)
               logging.info('Diectory "%s" is created.'%arg)
           else:
               logging.error('Diectory "%s" does not exist, using the current directory'%arg)
               opath=''
        else:
            opath,otag=otag,opath

    return opath,otag

if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
        sys.exit()

    help=lib.common_lib.HELP(usage,FFMPEG_BIN,'--help')
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'o:e:aC:T:r:m:t:'+help.get_opt())
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    except Exception, e:
        print e

    # opt_list = get_default_opt_list()
    #input_tmp = ''
    #output_tmp = ''
    output_tag=''
    output_path=''
    extra_cmd = ''
    extension = ''
    thread_num = ''
    #do_execute = 0
    #decode_flag = 0
    #bitstream_type = ""
    auto_audio_flag=1
    width=-2
    height=-2
    merged_file=''
    #time_str=''
    startp=''
    dura=''
    endp=''

    print opts
    print args

    for opt, arg in opts:
        if opt == '-o':
            #output_tmp = arg
            output_path,output_tag=parse_outpath(arg)
        elif opt == '-e':
            extension = arg
        elif opt == '-a':
            auto_audio_flag= 0
        elif opt == '-C':
            extra_cmd = arg
        elif opt == '-T':
            thread_num = arg
        elif opt == '-r':
            #width= int(arg)
            width,height=parse_reso(arg,width,height)
        elif opt=='-m':
            merged_file=arg
        elif opt=='-t':
            if '+' in arg:
                startp,dura=parse_time(arg,startp,dura)
            elif '-' in arg:
                startp,endp=parse_time(arg,startp,endp,'-')
        #elif opt[1] in help.get_opt():
        #    help.parse_opt(opt)
        else:
            help.parse_opt(opt)


    if len(args) == 0:
        logging.error('No input is specified, please check')
        sys.exit()

    input_list=[]
    for arg in args:
        get_input_list(input_list,arg)

    if len(input_list) == 0:
        logging.error('Input is invalid, please check')
        sys.exit()

    if len(output_tag) == 0:  # =='':
        output_tag = "out"
    else:
        if '.' in output_tag:
            output_tag,extension=os.path.splitext(output_tag)
    #    if not output_tag.startswith('_'):
    #        output_tag = '_' + output_tag
    print "output_tag=%s"%output_tag
    print type(extension)
    print 'extension=%s'%extension

    prepared_cmd = FFMPEG_BIN

    if len(thread_num) > 0:
        prepared_cmd += ' -threads %s' % thread_num

    if len(dura)>0:
        if len(startp)>0:
            prepared_cmd+=' -ss %s'%startp
        prepared_cmd+=' -t %s'%dura
    if len(endp)>0:
        if len(startp)>0:
            extra_cmd+=' -ss %s'%startp
        extra_cmd+=' -to %s'%endp

    if len(merged_file)>0: # option -m: merge the inputfiles
        extension='TS'
    elif len(extension)>0 : # option -e: do actions according to the extension
        if extension.startswith('.'):
           extension =  extension[1:]
        extension=extension.lower()
        if not extension in valid_ext_list:
            logging.error('Invaild extension, please check')
            sys.exit()

        if extension in yuv_name_list:# decode to get raw yuv
            output_tag = 'rec'
            extra_cmd += ' -an -f rawvideo'
        elif extension in bitstream_name_list:# just get the raw stream
            output_tag= 'bin'
            if extension in h264_name_list:
                extension= 'h264'
            elif extension in h265_name_list:
                extension= 'hevc'
            extra_cmd += ' -c:v copy'
            extra_cmd += ' -an -f %s' % extension
        elif extension in audio_name_list:
            output_tag='audio'
            extra_cmd+=' -vn'
            if auto_audio_flag==1:
                extra_cmd+=' -c:a copy'
            else:
                extra_cmd+=' -b:a 64k'#set bitrate for audio
        elif extension in image_name_list:
            output_tag='%3d'
        elif extension in gif_name_list:
            extra_cmd+=' -r 15'
            extra_cmd+=' -an'


    if width>0 or height >0:# option -r: resize the input video file
        extra_cmd+=' -vf scale=%s:%s'%(width,height)


    cmd_list = []
    output_list=[]
    for input_file in input_list:
        print input_file
        if not os.path.isfile(input_file):
            logging.error('"%s" is not a file, but is in the input_list'%input_file)
        cmd_line,output_file = get_cmd_line(input_file, extension, output_path,output_tag, prepared_cmd, extra_cmd)
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


    if help.get_do_execute()== 1:
        for cmd in cmd_list:
            if len(cmd)==0:
                continue
            print cmd
            # os.system(cmd)
            subprocess.call(cmd, stdout=None, stderr=None, shell=True)
        if len(merged_file)>0:
            for i in output_list:
                if os.path.exists(i):
                    #os.remove(i)
                   logging.info('"%s" is deleted'%i)



