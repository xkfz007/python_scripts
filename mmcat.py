#!/bin/python
#coding=utf-8
__author__ = 'Felix'
import sys
import lib
import getopt
import os.path

import logging
logging.basicConfig(level=logging.INFO,format='[%(levelname)s]:%(message)s')

FFMPEG_BIN = 'ffmpeg'
default_cmd= '%s -y -f concat -i'%FFMPEG_BIN

def usage():
    help_msg = '''USAGE:pyff.py [OPTIONS]... [ARGUMENTS]...
   OPTIONS:
     -i <string>  merge the input media files to one, only mp4 and mkv is supported
     -I <string>
     -o <string>
     -m <mode/method>
   ARGUMENTS:
     file or directory, support pattern globbing,these are the input files that will be processed
   '''
    print help_msg
    return

def parse_file_list(flist,script):
    f=open(script,'r')
    lines=f.readlines()
    f.close()
    for l in lines:
        chn=l.strip('\n')
        chn=chn.strip(' ')
        if not chn.startswith('#') and len(chn)>0:
            if os.path.exists(chn):
                flist.append(chn)
            else:
                logging.warning('file "%s" does not exist, ignored'%chn)

def get_timestamp():
    import datetime
    import time
    t=time.mktime(datetime.datetime.now().timetuple())
    return int(t)

def get_cmd_with_script(input_list,do_execute=0):
    content=["file '"+line+"'\n" for line in input_list]
    logging.info(content)
    concat_script='concate_script_%s.txt'%get_timestamp()
    if do_execute==1:
        tempf = open(concat_script, 'w')
        try:
            tempf.writelines(content)
        finally:
            tempf.close()
    cmd ='%s "%s"'%(default_cmd,concat_script)
    return cmd

def get_cmd_with_pipe(input_list):
    content=["'"+lib.convert2drivepath(os.path.realpath(line))+"'" for line in input_list]
    content_str=' '.join(content)
    cmd='str=(%s);'%content_str
    cmd+="for i in \"${str[@]}\";do echo \"file '$i'\";done|"
    cmd+='%s pipe:0'%default_cmd
    #cmd =" %s;for i in \"${str[@]}\";do echo \"file '$i'\";done"%cmd_sub
    return cmd

def get_cmd_with_procsub(input_list):
    content=["'"+lib.convert2drivepath(os.path.realpath(line))+"'" for line in input_list]
    content_str=' '.join(content)
    cmd0='str=(%s);'%content_str
    cmd0+="for i in \"${str[@]}\";do echo \"file '$i'\";done"
    cmd='%s <(%s)'%(default_cmd,cmd0)
    return cmd


if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
        sys.exit()


    help = lib.common_lib.HELP(usage, FFMPEG_BIN, '--help')
    #options = 'o:e:aC:T:E:m:t:'
    options = 'o:i:I:m:'
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], options + help.get_opt())
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    except Exception, e:
        print e


    logging.info("opts=%s args=%s"%(opts,args))
    output_arg=''
    addational_file_list=''
    mode=0
    file_script=''

    for opt, arg in opts:
        if opt == '-o':
            output_arg=arg
        elif opt == '-i':
            addational_file_list=arg
        elif opt == '-I':
            file_script=arg
        elif opt == '-m':
            mode=int(arg)
        else:
            help.parse_opt(opt)

    ext='.mkv'#default is mkv
    output_fname='concatenated_file'#default output filename


    if len(file_script)>0 and os.path.exists(file_script):
        logging.info('%s will use script "%s" to concatenate files'%(FFMPEG_BIN,file_script))
        cmd='%s "%s"'%(default_cmd,file_script)
    else:
        input_list = []
        for arg in args:
            lib.get_input_file_list(input_list, arg)

        if len(addational_file_list)>0 and os.path.exists(addational_file_list):
            logging.info('files in "%s" will be parsed'%addational_file_list)
            parse_file_list(input_list,addational_file_list)

        if len(input_list) == 0:
            logging.error('No input file is specified, and No files will be concatenated.')
            sys.exit()

        #TODO
        dummy,ext=os.path.splitext(input_list[0])

        if mode==0:#use pipe
            cmd=get_cmd_with_pipe(input_list)
        elif mode==1:#auto to generate script
            cmd=get_cmd_with_script(input_list,help.get_do_execute())
        elif mode==2:#auto to generate script
            cmd=get_cmd_with_procsub(input_list)

    if len(output_arg)>0:
        if output_arg.startswith('.'):
            ext=output_arg
        else:
            tmp_name,tmp_ext=os.path.splitext(output_arg)
            if len(tmp_name)>0:
                output_fname=tmp_name
            if len(tmp_ext)>0:
                ext=tmp_ext

    output_file=output_fname+ext

    cmd+=' -c copy "%s"'%output_file
    lib.run_cmd(cmd, help.get_do_execute())

    #if os.path.exists(concat_script):
    #    logging.info('file "%s" will be removed.'%concat_script)
        #os.remove(concat_script)


