#!/bin/python
#coding=utf-8
__author__ = 'Felix'
import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

#import logging
#logging.basicConfig(level=logging.INFO,format='[%(levelname)s]:%(message)s')

FFMPEG_BIN = 'ffmpeg'
#default_cmd= '%s -y -f concat -i'%FFMPEG_BIN
logger=utils.Log('MMCAT')

def usage():
    help_msg = '''USAGE:mmcat.py [OPTIONS]... [ARGUMENTS]...
   OPTIONS:
     -I <filname>  merge the input media files to one, only mp4 and mkv is supported
                   When the filename contains Chinese characters, this option is used
     -o <string>  output filename
     -m <mode/method>
     -T <int> thread number
   ARGUMENTS:
     <files> or <directory>  support pattern globbing,these are the input files that will be processed
                             When the there is no Chinses characters, this method is better
   '''
    print help_msg
    return

def parse_file_list(flist,ifile):
    f=open(ifile,'r')
    lines=f.readlines()
    f.close()
    for l in lines:
        chn=l.strip('\n')
        chn=chn.strip(' ')
        if not chn.startswith('#') and len(chn)>0:
            if os.path.exists(chn):
                flist.append(chn)
            else:
                logger.warning('file "%s" does not exist, ignored'%chn)
def parse_script(flist,script):
    import codecs
    with open(script,'r') as f:
        lines=f.readlines()
    #f=open(script,'r')
    #lines=f.readlines()
    #f.close()
    for l in lines:
        chn=l.strip('\n')
        chn=chn.strip(' ')
        print chn
        if chn.startswith('#') or len(chn)==0:
            continue
        #directive,path=chn.split()
        str_list=chn.split()
        if len(str_list)<2 or str_list[0]!='file':
            continue
        path=str_list[1]
        path=path.strip('\'')
        print isinstance(path,unicode)
        print isinstance(path,str)
        flist.append(path)
        if os.path.exists(path):
            flist.append(path)
        else:
            logger.error('file "%s" does not exist'%path)
            #sys.exit()
    #print flist


def get_timestamp():
    import datetime
    import time
    t=time.mktime(datetime.datetime.now().timetuple())
    return int(t)

def get_cmd_with_script(global_cmd,input_list,do_execute=0):
    content=["file '"+line+"'\n" for line in input_list]
    logger.info(content)
    concat_script='concate_script_%s.txt'%get_timestamp()
    if do_execute==1:
        tempf = open(concat_script, 'w')
        try:
            tempf.writelines(content)
        finally:
            tempf.close()
    cmd ='%s -f concat -i "%s"'%(global_cmd,concat_script)
    return cmd

def generate_pipe_cmd(global_cmd,content_str):
    cmd='str=(%s);'%content_str
    cmd+="for i in \"${str[@]}\";do echo \"file '$i'\";done|"
    cmd+='%s -f concat -i pipe:0'%global_cmd
    return cmd
# for *.mp4 *.flv *.mkv *.avi *.ts
def get_cmd_with_pipe(global_cmd,input_list):
    #content=["'"+lib.convert2drivepath(os.path.realpath(line))+"'" for line in input_list]
    content=["'"+utils.convert2drivepath(line)+"'" for line in input_list]
    content_str=' '.join(content)
    #cmd='str=(%s);'%content_str
    #cmd+="for i in \"${str[@]}\";do echo \"file '$i'\";done|"
    #cmd+='%s pipe:0'%default_cmd
    #cmd =" %s;for i in \"${str[@]}\";do echo \"file '$i'\";done"%cmd_sub
    return generate_pipe_cmd(global_cmd,content_str)

#def get_cmd_with_pipe2(input_list):
#    return cmd

#def get_cmd_with_procsub(input_list):
#    content=["'"+lib.convert2drivepath(os.path.realpath(line))+"'" for line in input_list]
#    content_str=' '.join(content)
#    cmd0='str=(%s);'%content_str
#    cmd0+="for i in \"${str[@]}\";do echo \"file '$i'\";done"
#    cmd='%s <(%s)'%(default_cmd,cmd0)
#    return cmd

# for *.rmvb
def get_cmd_with_filter(global_cmd,input_list):
    input_cmd_list=[]
    filter_cmd_list=[]
    size=len(input_list)
    for i in range(0,size):
        input_cmd_list.append('-i "'+input_list[i]+'"')
        filter_cmd_list.append('[%s:v:0] [%s:a:0]'%(i,i))

    input_cmd_str=' '.join(input_cmd_list)
    filter_cmd_str=' '.join(filter_cmd_list)
    concat_cmd_str='concat=n=%s:v=1:a=1 [v] [a]'%size
    map_cmd_str="-map '[v]' -map '[a]'"
    cmd=global_cmd+' '+input_cmd_str+\
        " -filter_complex '"+filter_cmd_str+" "+concat_cmd_str+"' "+\
        map_cmd_str
    return cmd

# for *.rmvb
def get_cmd_with_tempfiles(global_cmd,input_list):
    tmpfile_cmd_list=[]
    tmpfile_list=[]
    size=len(input_list)
    for i in range(0,size):
        tmpfile_list.append('intermediate%s.mkv'%i)
        tmpfile_cmd_list.append('%s -i "%s" -c:v copy intermediate%s.mkv'%(global_cmd,input_list[i],i))

    cmd=';'.join(tmpfile_cmd_list)

    content=["'"+line+"'" for line in tmpfile_list]
    content_str=' '.join(content)
    #cmd+=";str=(%s);for i in \"${str[@]}\";do echo \"file '$i'\";done|"%' '.join(content)
    #cmd+='ffmpeg -y -f concat -i pipe:0 -c copy '

    return cmd+';'+generate_pipe_cmd(global_cmd,content_str)
if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
        sys.exit()


    help = utils.HELP(usage, FFMPEG_BIN, '--help',logger)
    options = 'o:i:I:m:T:'
    opts,args=utils.my_getopt(sys.argv[1:],options+help.get_opt())

    logger.info("opts=%s args=%s"%(opts,args))
    output_arg=''
    #addational_file_list=''
    mode=0
    file_script=''
    thread_num=-1
    global_cmd=FFMPEG_BIN+' -y'

    for opt, arg in opts:
        if opt == '-o':
            output_arg=arg
        #elif opt == '-i':
        #    addational_file_list=arg
        elif opt == '-I':
            file_script=arg
        elif opt == '-m':
            mode=int(arg)
        elif opt == '-T':
            thread_num=int(arg)
        else:
            help.parse_opt(opt)

    #add option -threads
    if thread_num > 0:
        global_cmd+= ' -threads %s' % thread_num

    ext='.mkv'#default is mkv
    output_fname='concatenated_file'#default output filename
    enc_cmd='-c copy'


    input_list = []
    if len(file_script)>0 and os.path.exists(file_script):
        logger.info('%s will use script "%s" to concatenate files'%(FFMPEG_BIN,file_script))
        cmd='%s -f concat -i "%s"'%(global_cmd,file_script)
        #parse_script(input_list,file_script)
    else:
        if len(args)==0:
            logger.error('No input file is specified.')
            sys.exit()

        if 0:#len(args)==1 and '*' in args[0] and not args[0].endswith('rmvb'):
           #input_list.append(args[0])
           pass
        else:
            for arg in args:
                utils.get_input_file_list(input_list, arg)

        #if len(addational_file_list)>0 and os.path.exists(addational_file_list):
        #    logging.info('files in "%s" will be parsed'%addational_file_list)
        #    parse_file_list(input_list,addational_file_list)

        if len(input_list) == 0:
            logger.error('No input file is specified, and No files will be concatenated.')
            sys.exit()

        #TODO
        dummy,tmp_ext=os.path.splitext(input_list[0])
        #if lib.format_ext(tmp_ext)!='.rmvb':
        if len(tmp_ext)>0:
            ext=utils.format_ext(tmp_ext)

        if 0:#len(input_list) == 1:
            #if not '*' in input_list[0]:
            #    logging.error('Only one file')
            #    sys.exit()
            #else:
            #    cmd=generate_pipe_cmd(input_list[0])
            pass
        else:
            if ext=='.rmvb':
                ext='.mkv'
                if mode==0:
                    enc_cmd='-c:v copy'#'-c:v libx264'
                    cmd=get_cmd_with_tempfiles(global_cmd,input_list)
                elif mode==1:
                    enc_cmd=''#-c:v copy'#'-c:v libx264'
                    cmd=get_cmd_with_filter(global_cmd,input_list)
            else:
                if mode==0:#use pipe
                    cmd=get_cmd_with_pipe(global_cmd,input_list)
                elif mode==1:#auto to generate script
                    cmd=get_cmd_with_script(global_cmd,input_list,help.get_do_execute())
                #elif mode==2:#auto to generate script
                #    cmd=get_cmd_with_procsub(input_list)

    if len(output_arg)>0:
        if output_arg.startswith('.'):
            ext=utils.format_ext(output_arg)
        else:
            tmp_name,tmp_ext=os.path.splitext(output_arg)
            if len(tmp_name)>0:
                output_fname=tmp_name
            if len(tmp_ext)>0:
                ext=utils.format_ext(tmp_ext)

    ext=utils.format_ext(ext)

    output_file=output_fname+ext

    #cmd+=' %s "%s"'%(enc_cmd,output_file)
    cmd+=' %s'%enc_cmd
    cmd+=' "%s"'%output_file
    utils.run_cmd(cmd, help.get_do_execute())

    #if os.path.exists(concat_script):
    #    logging.info('file "%s" will be removed.'%concat_script)
        #os.remove(concat_script)


