#!/bin/python
__author__ = 'Felix'
import subprocess
import os, sys
import getopt
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logging
#logging.basicConfig(level=logging.INFO,format='[%(levelname)s]:%(message)s')

#ffmpeg -nhb -i "$input1" -i "$input2" -i "$input3" -i "$input4"  \
#-filter_complex "nullsrc=size=640x480 [base]; \
#[0:p:3801:v] setpts=PTS-STARTPTS, scale=320x240 [upperleft]; \
#[1:p:3702:v] setpts=PTS-STARTPTS, scale=320x240 [upperright]; \
#[2:p:4301:v] setpts=PTS-STARTPTS, scale=320x240 [lowerleft]; \
#[3:p:4302:v] setpts=PTS-STARTPTS, scale=320x240 [lowerright]; \
#[base][upperleft] overlay=shortest=0:eof_action=pass [tmp1];\
#[tmp1][upperright] overlay=shortest=0:eof_action=pass:x=320 [tmp2]; \
#[tmp2][lowerleft] overlay=shortest=0:eof_action=pass:y=240 [tmp3]; \
#[tmp3][lowerright] overlay=shortest=0:eof_action=pass:x=320:y=240[out]" \
#-map '[out]' -c:v libx264 -f flv  rtmp://172.16.68.206:19350/live/multi_screen
def get_single_win(idx="",pid="",name="",win_w=320,win_h=240):
    stream_idx="[%s:v]"%(idx)
    scale="%sx%s"%(win_w,win_h)
    if len(pid) != 0:
        stream_idx="[%s:p:%s:v]"%(idx,pid)
        
    cmd="%s setpts=PTS-STARTPTS, scale=%s [%s]"%(stream_idx,scale,name)
    return cmd

def get_single_overlay(in1="",in2="",pos_x=0,pos_y=0,out=""):
    cmd="[%s][%s]overlay=shortest=0:eof_action=pass:x=%s:y=%s[%s]"%(in1,in2,pos_x,pos_y,out)
    return cmd

def get_all_wins(col_cnt,row_cnt,win_w,win_h,pid_list):
    win_list=[]
    for j in range(row_cnt):
        for i in range(col_cnt):
            idx=j*col_cnt+i
            name="win_%s"%idx
            pid=pid_list[idx]
            swin_cmd=get_single_win(idx,pid,name,win_w,win_h)
            win_list.append(swin_cmd)
    cmd=';'.join(win_list)
    logging.debug("all_wins="+cmd)
    return cmd


def get_all_overlay(col_cnt,row_cnt,win_w,win_h):
    overlay_list=[]
    for j in range(row_cnt):
        for i in range(col_cnt):
            idx=j*col_cnt+i
            in1="ol_%s"%idx
            in2="win_%s"%idx
            out="ol_%s"%(idx+1)
            if j==0 and i==0:
                in1='base'
            if j==row_cnt-1 and i==col_cnt-1:
                out='out'
            x=i*win_w;
            y=win_h*j;
            solay=get_single_overlay(in1,in2,x,y,out)
            overlay_list.append(solay)
    cmd=';'.join(overlay_list)
    logging.debug("all_overlay="+cmd)
    return cmd

def get_filter_cl(col_cnt,row_cnt,width,height,pid_list):
    win_w=width/col_cnt;
    win_h=height/row_cnt;
    cmd='-filter_complex "nullsrc=size=%sx%s [base];'%(width,height)
    cmd+=get_all_wins(col_cnt, row_cnt, win_w, win_h, pid_list)
    cmd+=';'
    cmd+=get_all_overlay(col_cnt, row_cnt, win_w, win_h)
    cmd+='"'
    logging.debug("filter_cl="+cmd)
    return cmd

def get_input_cl(input_list,pid_list):
    cmd=""
    cnt=len(input_list)
    for i in range(cnt):
        input=input_list[i]
        logging.debug(input)
        if input.startswith("udp://"):
            input=input[6:]
            logging.debug(input)
            addr=input
            if '/' in input:
                 addr,pid=input.split('/')
                 if len(pid)>0:
                     pid_list[i]="%s"%pid
            input="udp://%s?overrun_nonfatal=1&buffer_size=100000000&fifo_size=10000000"%addr
        
        cmd+='-i "%s" '%input
            
    logging.debug("input_cl="+cmd)
    return cmd

def get_output_cl(output):
    codec=' -map "[out]" -c:v libx264 '
    format=""
    if output.startswith("udp://"):
        format="mpegts"
    elif output.startswith("rtmp://"):
        format="flv"
    cmd=codec+" "+" -f "+format+" "+output
    logging.debug("output_cl="+cmd)
    return cmd

def usage():
    help_msg = '''USAGE:multiscreen.py [OPTIONS]... <stream1> <stream2> ...
   OPTIONS:
     -i <string>         the input stream file list
     -o <string>         output address 
     -s <width>x<height> output screen size 
     -w <col>x<row>      output windows
     -v <string>         loglevel
   Example:
     multiscreen.py -o "udp://235.1.1.2:48880" -s 640x480 -w 2x2 "udp://235.1.1.1:48880"  "udp://235.1.1.1:48880"  "udp://235.1.1.1:48880"  "udp://235.1.1.1:48880" 
   '''
    print help_msg
    return

def parse_arg(opt,arg):

    if 'x' not in arg.lower():
         logging.error('Wrong format of "%s" with arg "%s"'%(opt,arg))
         sys.exit()

    x,y=arg.split('x')
    w=int(x)
    h=int(y)
    return w,h

if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        usage()
        sys.exit()

    FFMPEG_BIN = 'ffmpeg'

    options = 'i:o:s:w:Yv:'

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], options)
    except getopt.GetoptError as err:
        logging.error(str(err))
        sys.exit(2)
    except Exception, e:
        logging.error(e)

    input_stream_file=''
    output=''
    input_list=[]
    width=-1
    height=-1
    rows=-1
    cols=-1
    do_execute=0
    loglevel=logging.INFO
    log_map={'info':logging.INFO,
             'debug':logging.DEBUG,
             'error':logging.ERROR,
             'warning':logging.WARNING}


    for opt, arg in opts:
        if opt == '-i':
            input_stream_file=arg
        elif opt == '-o':
            output=arg
        elif opt == '-s':
            width,height=parse_arg(opt,arg)
        elif opt == '-w':
            cols,rows=parse_arg(opt,arg)
        elif opt == '-Y':
            do_execute=1
        elif opt== '-v':
            loglevel=log_map[arg.lower()]
        else:
            loggging.error("Unrecognized option '%s'"%opt)
            sys.exit()
    
    logging.basicConfig(level=loglevel,format='[%(levelname)s]:%(message)s')

    if len(args) != 0:
         for arg in args:
              input_list.append(arg)

    if len(input_stream_file) >0 and os.path.exist(input_stream_file):
        logging.info("Reading input from file '%s'"%input_stream_file)

        f=open(input_stream_file,'r')
        lines=f.readlines()
        f.close()
        for line in lines:
            chn=line.strip('\n')
            chn=chn.strip(' ')
            if not chn.startswith('#'):
                input_list.append(chn)
    
    if width==-1 or height==-1:
        logging.error("Invalid value of width or height")
        sys.exit()
    if rows==-1 or cols==-1:
        loggging.error("Invalid value of rows or cols")
        sys.exit()

    win_cnt=rows*cols

    if len(input_list)==0:
        logging.error("No input is set")
        sys.exit()

    if len(input_list) !=win_cnt:
        logging.error("Input stream number does not equal number of windows")
        sys.exit()
        
    logging.info("input_list:%s"%input_list)
        
    if len(output)==0:
        logging.error("Ouput is not set")
        sys.exit()

    pid_list=[""]*win_cnt
    
    #input_list=['udp://235.1.1.1:48880',
    #            'udp://235.1.1.1:48880',
    #            'udp://235.1.1.1:48880',
    #            'udp://235.1.1.1:48880',
    #            ]
    #output='udp://235.1.1.2:48880'

    cmd=FFMPEG_BIN+" "
    cmd+=get_input_cl(input_list[0:win_cnt],pid_list)
    cmd+=get_filter_cl(cols, rows, width, height, pid_list)
    cmd+=get_output_cl(output)
    
    logging.info(cmd)

    if do_execute==0:
        sys.exit()

    subprocess.call(cmd, shell=True, stdout=None, stderr=None)