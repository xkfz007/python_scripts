#!/bin/python
#coding=utf-8
__author__ = 'Felix'
import sys
import lib
import getopt
import os.path

import logging
logging.basicConfig(level=logging.INFO,format='[%(levelname)s]:%(message)s')

def usage():
    help_msg = '''USAGE:pyff.py [OPTIONS]... [ARGUMENTS]...
   OPTIONS:
     -i <string>  merge the input media files to one, only mp4 and mkv is supported
     -I <string>
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
if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
        sys.exit()

    FFMPEG_BIN = 'ffmpeg'

    help = lib.common_lib.HELP(usage, FFMPEG_BIN, '--help')
    #options = 'o:e:aC:T:E:m:t:'
    options = 'o:i:I:'
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], options + help.get_opt())
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    except Exception, e:
        print e


    logging.info("opts=%s args=%s"%(opts,args))
    output_file=''
    addational_file_list=''
    use_file=0
    file_script=''

    for opt, arg in opts:
        if opt == '-o':
            output_file=arg
        elif opt == '-i':
            addational_file_list=arg
        elif opt=='-I':
            file_script=arg
        else:
            help.parse_opt(opt)

    if len(args) == 0:
        logging.error('No input is specified, please check')
        sys.exit()

    input_list = []
    for arg in args:
        lib.get_input_file_list(input_list, arg)

    concat_script=''

    #if len(input_list)==0:
    #    if len(addational_file_list)>0 and os.path.exists(addational_file_list):
    #        logging.info('just use the addational filelist "%s" as script'%addational_file_list)
    #        concat_script=addational_file_list
    #    else:
    #        logging.error('No input file is specified, and No files will be concatenated.')
    #        sys.exit()
    #else:
    if len(addational_file_list)>0 and os.path.exists(addational_file_list):
        logging.info('files in "%s" will be parsed'%addational_file_list)
        parse_file_list(input_list,addational_file_list)

    if len(input_list) == 0:
        logging.error('No input file is specified, and No files will be concatenated.')
        sys.exit()

    #TODO
    dummy,ext=os.path.splitext(input_list[0])

    #content=[]
    #for p in input_list:
    #    line='file "'+p+'"'
    #    logging.info(line)

    cmd= FFMPEG_BIN
    cmd+= ' -y'
    cmd+= ' -f concat -i'
    cmd_pre=''
    if use_file == 1:
        content=["file '"+line+"'\n" for line in input_list]
        logging.info(content)
        concat_script='concate_script_%s.txt'%get_timestamp()
        if help.get_do_execute():
            import codecs
            tempf = codecs.open(concat_script, 'w','utf-8')

            try:
                for p in content:
                    tempf.write(p.decode('gbk'))
                #tempf.writelines(content)
            finally:
                tempf.close()
        cmd +=' "%s"'%concat_script
    else:
        content=["'"+lib.convert2drivepath(os.path.realpath(line))+"'" for line in input_list]
        content_str=' '.join(content)
        cmd_pre='str=(%s);'%content_str
        cmd_pre+="for i in \"${str[@]}\";do echo \"file '$i'\";done|"
        cmd+=' pipe:0'
        #cmd =" %s;for i in \"${str[@]}\";do echo \"file '$i'\";done"%cmd_sub

    if len(output_file)==0:
        output_file='concatenated_file'+ext
    cmd +=' -c copy %s'%output_file

    cmd=cmd_pre+cmd

    lib.run_cmd(cmd, help.get_do_execute())

    if os.path.exists(concat_script):
        logging.info('file "%s" will be removed.'%concat_script)
        #os.remove(concat_script)


