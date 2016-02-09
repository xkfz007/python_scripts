#!/bin/python
__author__ = 'Felix'
import sys
import lib
import getopt
import os.path
import glob
import chardet

import logging
logging.basicConfig(level=logging.INFO,format='[%(levelname)s]:%(message)s')

FFMPEG_BIN = 'ffmpeg'
def usage():
    help_msg = '''USAGE:addsub.py [option] <video> <subtitle>
    -o <output_file>
    -m <mode>
        0: add *.srt as stream
        1: convert srt to ass and use pipe
        2: convert srt to ass and use intermediate file
        3: convert srt to ass and use intermediate file with hard code and reencoding
    -e <encoding> gbk,big5,utf-8
    EXAMPLES:
    addsub.py "*.mp4" "*.srt" -o out.mkv -Y
    addsub.py "*.mp4" "*.ass" -o out -Y
    addsub.py "*.mp4" "*.srt" -m 0 -Y
    addsub.py "*.mp4" "*.srt" -m 1 -Y
   '''
    print help_msg
    return


if __name__ == '__main__':
    #f=open(sys.argv[1],'r')
    #fenc=chardet.detect(f.read())
    #print fenc

    if len(sys.argv) == 1:
        usage()
        sys.exit()
    elif len(sys.argv) < 3:
        usage()
        sys.exit()

    help = lib.common_lib.HELP(usage, FFMPEG_BIN, '--help')
    options = 'o:m:e:'
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], options + help.get_opt())
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    except Exception, e:
        print e


    logging.info("opts=%s args=%s"%(opts,args))

    output_arg=''
    mode=1
    encoding_type='gbk'

    for opt, arg in opts:
        if opt == '-o':
            output_arg=arg
        elif opt == '-m':
            mode=int(arg)
        elif opt == '-e':
            encoding_type=arg
        else:
            help.parse_opt(opt)

    if len(args)>2:
        logging.error('Too much input,please check')
        sys.exit()

    glob_list=glob.glob(args[0])
    logging.info('"%s" is glob pattern:%s' % (args[0],glob_list))
    if len(glob_list)>1:
        logging.error('Too much input video files,please check')
        sys.exit()
    elif len(glob_list)<1:
        logging.error('Too little input video files,please check')
        sys.exit()
    video_file=glob_list[0]

    glob_list=glob.glob(args[1])
    logging.info('"%s" is glob pattern:%s' % (args[1],glob_list))
    if len(glob_list)>1:
        logging.error('Too much input subtitle files,please check')
        sys.exit()
    elif len(glob_list)<1:
        logging.error('Too little input subtitle files,please check')
        sys.exit()
    subtitle_file=glob_list[0]

    #f=open(subtitle_file,'r')
    #fencoding=chardet.detect(f.read())
    #print fencoding

    ext='.mkv'
    fname,fext=os.path.splitext(video_file)
    if len(output_arg)>0:
       fname=output_arg

    output_file=fname+'.Subtitle'+ext

    cmd=FFMPEG_BIN
    if mode==0:#enlish subtitle, use srt directly
        cmd+=' -y -i "%s" -i "%s" -c copy "%s"'%(video_file,subtitle_file,output_file)
    else:
        intermediate_sub_file=subtitle_file
        if subtitle_file.endswith('.srt'):
            if mode==1:#use pipe
                intermediate_sub_file='-'
                cmd+=' -y -sub_charenc %s -i "%s" -f ass "%s"|'%(encoding_type,subtitle_file,intermediate_sub_file)
                cmd+=FFMPEG_BIN
            elif mode>1:
                intermediate_sub_file='intermediate.ass'
                cmd+=' -y -sub_charenc %s -i "%s" -f ass "%s";'%(encoding_type,subtitle_file,intermediate_sub_file)

        if mode<3:# use subtitle stream
            cmd+=' -y -i "%s" -sub_charenc %s  -i "%s" -c copy "%s"'%(video_file,encoding_type,intermediate_sub_file,output_file)
        elif mode==3:# hard code
            pass
            cmd+=' -y -i "%s" -vf \'ass="%s"\' -c:a copy "%s"'%(video_file,intermediate_sub_file,output_file)
        #if mode==1:#use pipe
        #    cmd+=' -y -i "%s" -sub_charenc gbk -i %s -c copy "%s"'%(video_file,tmp_sub_file,output_file)
        #elif mode>1:#chinese subtitle, need convert to ass first
        #    #tmp_sub_file='intermediate.ass'
        #    #cmd+=' -y -sub_charenc gbk -i "%s" -f ass "%s";'%(subtitle_file,tmp_sub_file)
        #    if mode==2:#add subtitle stream
        #        cmd+='%s -y -i "%s" -sub_charenc gbk -i "%s" -c copy "%s"'%(FFMPEG_BIN,video_file,tmp_sub_file,output_file)
        #    elif mode==3:# hard code
        #        pass
        #        cmd+='%s -y -i "%s" -vf \'ass="%s"\' -c:a copy "%s"'%(FFMPEG_BIN,video_file,tmp_sub_file,output_file)

    lib.run_cmd(cmd, help.get_do_execute())





