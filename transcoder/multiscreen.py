#!/usr/bin/python
__author__ = 'Felix'
import subprocess
import os, sys
import getopt
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logging
import platform
import datetime
import time
import signal
import re
# logging.basicConfig(level=logging.INFO,format='[%(levelname)s]:%(message)s')

FFMPEG_BIN = 'ffmpeg'
FFPROBE_BIN='ffprobe'
COLOR='yellow'
BITRATE=''
TIME_OUT=0
DO_DETECT=0
# ffmpeg -nhb -i "$input1" -i "$input2" -i "$input3" -i "$input4"  \
# -filter_complex "nullsrc=size=640x480 [base]; \
# [0:p:3801:v] setpts=PTS-STARTPTS, scale=320x240 [upperleft]; \
# [1:p:3702:v] setpts=PTS-STARTPTS, scale=320x240 [upperright]; \
# [2:p:4301:v] setpts=PTS-STARTPTS, scale=320x240 [lowerleft]; \
# [3:p:4302:v] setpts=PTS-STARTPTS, scale=320x240 [lowerright]; \
# [base][upperleft] overlay=shortest=0:eof_action=pass [tmp1];\
# [tmp1][upperright] overlay=shortest=0:eof_action=pass:x=320 [tmp2]; \
# [tmp2][lowerleft] overlay=shortest=0:eof_action=pass:y=240 [tmp3]; \
# [tmp3][lowerright] overlay=shortest=0:eof_action=pass:x=320:y=240[out]" \
# -map '[out]' -c:v libx264 -f flv  rtmp://172.16.68.206:19350/live/multi_screen

# ffmpeg -i "$input1" -i "$input2" -i "$input3" -i "$input4"  \
#    -filter_complex "nullsrc=size=640x480 [base]; \
#    [0:v] setpts=PTS-STARTPTS, scale=320x240 [upperleft]; \
#    [1:v] setpts=PTS-STARTPTS, scale=320x240 [upperright]; \
#    [2:v] setpts=PTS-STARTPTS, scale=320x240 [lowerleft]; \
#    [3:v] setpts=PTS-STARTPTS, scale=320x240 [lowerright]; \
#    [base][upperleft] overlay=shortest=1 [tmp1]; \
#    [tmp1][upperright] overlay=shortest=1:x=320 [tmp2]; \
#    [tmp2][lowerleft] overlay=shortest=1:y=240 [tmp3]; \
#    [tmp3][lowerright] overlay=shortest=1:x=320:y=240[tmp4];\
#    movie=giphy.gif[logo1];movie=giphy.gif[logo2];\
#    movie=giphy.gif[logo3];movie=giphy.gif[logo4];\
#    [tmp4][logo1]overlay=x=20:y=20[tt1];\
#    [tt1][logo2]overlay=x=340:y=20[tt2];\
#    [tt2][logo3]overlay=x=20:y=260[tt3];\
#    [tt3][logo4]overlay=x=340:y=260[out]"\
#    -map '[out]' -c:v libx264  -f mpegts udp://235.1.1.2:48880


# ffmpeg -i "$input1" -i "$input2" -i "$input3" -i "$input4"  \
#    -filter_complex "nullsrc=size=640x480 [base]; \
#    [0:v] setpts=PTS-STARTPTS, scale=320x240 [upperleft]; \
#    [base][upperleft] overlay=shortest=1 [tmp1]; \
#    [1:v] setpts=PTS-STARTPTS, scale=320x240 [upperright]; \
#    [tmp1][upperright] overlay=shortest=1:x=320 [tmp2]; \
#    [2:v] setpts=PTS-STARTPTS, scale=320x240 [lowerleft]; \
#    [tmp2][lowerleft] overlay=shortest=1:y=240 [tmp3]; \
#    [3:v] setpts=PTS-STARTPTS, scale=320x240 [lowerright]; \
#    [tmp3][lowerright] overlay=shortest=1:x=320:y=240[tmp4];\
#    [tmp4]drawtext=fontfile='C\:/Windows/Fonts/Calibri.ttf':text="AAAA":fontsize=30:fontcolor=white:x=20:y=20[tt1];\                                                                     
#    [tt1]drawtext =fontfile='C\:/Windows/Fonts/Calibri.ttf':text="BBBB":fontsize=30:fontcolor=white:x=340:y=20[tt2];\
#    [tt2]drawtext =fontfile='C\:/Windows/Fonts/Calibri.ttf':text="CCCC":fontsize=30:fontcolor=white:x=20:y=260[tt3];\
#    [tt3]drawtext =fontfile='C\:/Windows/Fonts/Calibri.ttf':text="DDDD":fontsize=30:fontcolor=white:x=340:y=260[out]"\
#    -map '[out]' -c:v libx264  -f mpegts udp://235.1.1.2:48880
 
def get_single_win(idx="", pid="", name="", win_w=320, win_h=240):
    stream_idx = "[%s:v]" % (idx)
    scale = "%sx%s" % (win_w, win_h)
    if len(pid) != 0:
        stream_idx = "[%s:p:%s:v]" % (idx, pid)
        
    cmd = "%s setpts=PTS-STARTPTS, scale=%s [%s]" % (stream_idx, scale, name)
    return cmd

def get_single_overlay(in1="", in2="", pos_x=0, pos_y=0, out=""):
    cmd = "[%s][%s]overlay=shortest=0:eof_action=pass:x=%s:y=%s[%s]" % (in1, in2, pos_x, pos_y, out)
    return cmd

def get_all_wins(col_cnt, row_cnt, win_w, win_h, pid_list):
    win_list = []
    for j in range(row_cnt):
        for i in range(col_cnt):
            idx = j * col_cnt + i
            name = "win_%s" % idx
            pid = pid_list[idx]
            swin_cmd = get_single_win(idx, pid, name, win_w, win_h)
            win_list.append(swin_cmd)
    cmd = ';'.join(win_list)
    logging.debug("all_wins=" + cmd)
    return cmd


def get_all_overlay(col_cnt, row_cnt, win_w, win_h):
    overlay_list = []
    for j in range(row_cnt):
        for i in range(col_cnt):
            idx = j * col_cnt + i
            in1 = "ol_%s" % idx
            in2 = "win_%s" % idx
            out = "ol_%s" % (idx + 1)
            if j == 0 and i == 0:
                in1 = 'base'
            if j == row_cnt - 1 and i == col_cnt - 1:
                out = 'out'
            x = i * win_w;
            y = win_h * j;
            solay = get_single_overlay(in1, in2, x, y, out)
            overlay_list.append(solay)
    cmd = ';'.join(overlay_list)
    logging.debug("all_overlay=" + cmd)
    return cmd

# [0:p:3801:v] setpts=PTS-STARTPTS, scale=320x240 [upperleft]; \
# [base][upperleft] overlay=shortest=0:eof_action=pass [tmp1];\
# [1:p:3702:v] setpts=PTS-STARTPTS, scale=320x240 [upperright]; \
# [tmp1][upperright] overlay=shortest=0:eof_action=pass:x=320 [tmp2]; \
# [2:p:4301:v] setpts=PTS-STARTPTS, scale=320x240 [lowerleft]; \
# [tmp2][lowerleft] overlay=shortest=0:eof_action=pass:y=240 [tmp3]; \
# [3:p:4302:v] setpts=PTS-STARTPTS, scale=320x240 [lowerright]; \
# [tmp3][lowerright] overlay=shortest=0:eof_action=pass:x=320:y=240[out]" \
def get_single_cell(idx, pid, scale, sin, inter, sout, x, y):
    stream_idx = "[%s:v]" % (idx)
#     scale = "%sx%s" % (w, h)
    if len(pid) != 0:
        stream_idx = "[%s:p:%s:v]" % (idx, pid)
        
    cmd = "%s setpts=PTS-STARTPTS, scale=%s [%s];" % (stream_idx, scale, inter)
    cmd += "[%s][%s]overlay=shortest=0:eof_action=pass:x=%s:y=%s[%s]" % (sin, inter, x, y, sout)
    return cmd
def get_single_logo(sin, inter, sout, logo_path, logo_w, logo_h, logo_x, logo_y):
    cmd = 'movie="%s",scale=%sx%s[%s];[%s][%s]overlay=x=%s:y=%s[%s]' % \
    (logo_path, logo_w, logo_h, inter, sin, inter, logo_x, logo_y, sout)
    
    return cmd;

def get_cell(input, background, output, w, h, x, y, logo='', text='', use_tsrc=0):
    cmd_list = [];
    cmd = '[%s]setpts=PTS-STARTPTS,scale=%sx%s[scaled_input]' % (input, w, h)
    cmd_list.append(cmd)
    overlayed = 'overlayed_input'
    cmd = '[%s][scaled_input]overlay=x=%s:y=%s[%s]' % (background, x, y, overlayed)
    tmp_output = overlayed
    cmd_list.append(cmd)
    if len(logo) > 0:
        watermarked = 'watermarked_input'
        cmd = "movie=filename='%s',scale=%sx%s[logo]" % (logo, w / 8, h / 8)
        cmd=cmd.replace('\\', '\\\\').replace(':', '\:')
        cmd_list.append(cmd)
        cmd = '[%s][logo]overlay=x=%s:y=%s[%s]' % (tmp_output, x + 10, y + 10, watermarked)
        tmp_output = watermarked
        cmd_list.append(cmd)
    if len(text) > 0:
        texted = 'texted_input'
        sysinfo = platform.system()
        sysinfo = sysinfo.upper()
        if sysinfo.find("WINDOWS")>=0 or sysinfo.find("CYGWIN") >= 0:
             font_path = 'C\:/Windows/Fonts/Calibri.ttf'
        elif sysinfo.find("LINUX") >= 0:
             font_path = '/usr/share/fonts/truetype/freefont/FreeSerif.ttf'
        cmd = "[%s]drawtext=fontfile='%s':text='%s':fontsize=%s:fontcolor=%s:x=%s:y=%s[%s]" % (tmp_output, font_path, text, w/8,COLOR,x + 10, y + 10, texted)
        tmp_output = texted
        cmd_list.append(cmd)
    full_cmd = ';'.join(cmd_list).replace(tmp_output, output)
    
    return full_cmd

def get_cells(count, cols, rows, w, h, pid_list, logo_list, text_list):

    cell_list = []
    for i in range(count):
        input = "%s:v" % i
        pid = pid_list[i]
        if len(pid) != 0:
            input = "%s:p:%s:v" % (i, pid)
        background = 'stream_' + str(i)
        output = 'stream_' + str(i + 1)
        if i == 0:
            background = 'base'
        if i == count - 1:
            output = 'out'
        x = (i % cols) * w
        y = (i / cols) * h
        logo = logo_list[i]
        text = text_list[i]
        ccmd = get_cell(input, background, output, w, h, x, y, logo, text)
        cell_list.append(ccmd)

    full_cmd = ';'.join(cell_list)

    return full_cmd

def get_filter_cl(count, col_cnt, row_cnt, width, height, pid_list, logo_list, text_list):
    win_w = width / col_cnt;
    win_h = height / row_cnt;
    cell_cl = get_cells(count, col_cnt, row_cnt, win_w, win_h, pid_list,logo_list,text_list)
    cmd = '-filter_complex "nullsrc=size=%sx%s [base];%s"' % (width, height, cell_cl)
    logging.debug("filter_cl=" + cmd)
    return cmd

class FFStream:
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

def get_fftype(streams,lines,tag):
    datalines=[]
    start_tag='\['+tag.upper()+'\]'
    end_tag='\[\/'+tag.upper()+'\]'
    for a in iter(lines, b''):
        if re.match(start_tag, a):
            datalines = []
        elif re.match(end_tag, a):
            streams.append(FFStream(datalines))
            datalines = []
        else:
            datalines.append(a)


def get_streams2(url, timeout=20):
    start = datetime.datetime.now()
    streams=[]
    cl_list=[]
    cl_list.append(FFPROBE_BIN)
    if url.startswith("rtsp://"):
        cl_list.append("-rtsp_flags prefer_tcp")
    cl_list.append('-show_streams')
    cl_list.append('"%s"'%url)
    cmd=' '.join(cl_list)
    process = subprocess.Popen(cmd, bufsize=100000, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True, close_fds=True)
    while process.poll() is None:
      time.sleep(0.1)
      now = datetime.datetime.now()
      if (now - start).seconds> timeout:
          logging.warning("Time out......")
          try:
            process.terminate()
          except Exception,e:
            return None
          return streams
    logging.info("Analysing streams......")
    get_fftype(streams,process.stdout.readline,'STREAM')
    get_fftype(streams,process.stderr.readline,'STREAM')
    if process.stdout:
      process.stdout.close()
    if process.stderr:
      process.stderr.close()
    try:
      process.kill()
    except OSError:
      pass
    return streams

def get_input_cl(input_list, pid_list):
    in_list=[]
    cnt = len(input_list)
    for i in range(cnt):
        input = input_list[i].strip(' ')
        logging.debug(input)
        if DO_DETECT>0:
           streams=get_streams2(input,DO_DETECT)
           if len(streams)<=0:
               logging.error('Could not detect the stream: %s'%(input))
               input=''
           else:
               logging.info('Stream "%s" is OK'%(input))
        if len(input)==0:
            logging.warning('Empty input found, use "testsrc" instead')
            in_list.append('-f lavfi -i testsrc')
            continue
        if input.startswith("rtsp://"):
            in_list.append("-rtsp_flags prefer_tcp")
        if input.startswith("udp://"):
            input = input[6:]
            logging.debug(input)
            addr = input
            if '/' in input:
                 addr, pid = input.split('/')
                 if len(pid) > 0:
                     pid_list[i] = "%s" % pid
            input = "udp://%s?overrun_nonfatal=1&buffer_size=100000000&fifo_size=10000000" % addr
        
        in_list.append('-thread_queue_size 1024')
        in_list.append('-i "%s"' % input)
            
    cmd=' '.join(in_list)
    logging.debug("input_cl=" + cmd)
    return cmd

def get_output_cl(output):
    cl_list=[]
    cl_list.append('-map "[out]" -c:v libx264')
    if len(BITRATE)>0:
        cl_list.append('-b:v %s'%BITRATE)
    format = ""
    if output.startswith("udp://"):
        format = "mpegts"
    elif output.startswith("rtmp://"):
        format = "flv"
    if len(format)>0:
        cl_list.append('-f %s'%format)
    cl_list.append(output)
    cmd=' '.join(cl_list)
    logging.debug("output_cl=" + cmd)
    return cmd

def usage():
    help_msg = '''USAGE:multiscreen.py [OPTIONS]... <stream1> <stream2> ...
   OPTIONS:
     -i <string|string>/<file>   the input stream file list or multi input streams separated by '|'
     -o <file>                   output address 
     -s <width>x<height>         output screen size 
     -w <col>x<row>              output windows
     -v <string>                 loglevel
     -l <string|string>          logos of each window separated by '|' 
     -t <string|string>          text of each window separated by '|'
     -c <string>                 color of text
     -b <int>M/<int>k            set bitrate of output
     -T seconds                  Time out
     -D seconds                  detect input to decide if use it, time out 'seconds'
     -L <file>                   output transcoder log
   Example:
     multiscreen.py -i "udp://235.1.1.1:48880|udp://235.1.1.1:48880|udp://235.1.1.1:48880|udp://235.1.1.1:48880" -o "udp://235.1.1.2:48880" -s 640x480 -w 2x2 
   '''
    print help_msg
    return

def parse_arg(opt, arg):

    if 'x' not in arg.lower():
         logging.error('Wrong format of "%s" with arg "%s"' % (opt, arg))
         sys.exit()

    x, y = arg.split('x')
    w = int(x)
    h = int(y)
    return w, h

if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        usage()
        sys.exit()


    options = 'i:o:s:w:Yv:l:t:c:b:T:D:L:'

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], options)
    except getopt.GetoptError as err:
        logging.error(str(err))
        sys.exit(2)
    except Exception, e:
        logging.error(e)

    input_stream_list_or_file = ''
    output = ''
    logo_input=''
    text_input=''
    width = -1
    height = -1
    rows = -1
    cols = -1
    do_execute = 0
    loglevel = logging.INFO
    log_map = {'info':logging.INFO,
             'debug':logging.DEBUG,
             'error':logging.ERROR,
             'warning':logging.WARNING}
    trans_log=''


    for opt, arg in opts:
        if opt == '-i':
            input_stream_list_or_file = arg
        elif opt == '-o':
            output = arg
        elif opt == '-s':
            width, height = parse_arg(opt, arg)
        elif opt == '-w':
            cols, rows = parse_arg(opt, arg)
        elif opt == '-Y':
            do_execute = 1
        elif opt == '-v':
            loglevel = log_map[arg.lower()]
        elif opt=='-l':
            logo_input=arg
        elif opt=='-t':
            text_input=arg
        elif opt=='-c':
            COLOR=arg
        elif opt=='-b':
            BITRATE=arg
        elif opt=='-T':
            TIME_OUT=int(arg)
        elif opt=='-D':
            DO_DETECT=int(arg)
        else:
            loggging.error("Unrecognized option '%s'" % opt)
            sys.exit()
    
    logging.basicConfig(level=loglevel, format='[%(levelname)s]:%(message)s')

    # if len(args) != 0:
    #     for arg in args:
    #          input_list.append(arg)

    input_list = []
    if len(input_stream_list_or_file) > 0:
        if os.path.exists(input_stream_list_or_file):
            logging.info("Reading input from file '%s'" % input_stream_list_or_file)

            f = open(input_stream_list_or_file, 'r')
            lines = f.readlines()
            f.close()
            for line in lines:
                chn = line.strip('\n')
                chn = chn.strip(' ')
                if not chn.startswith('#'):
                    input_list.append(chn)
        else:
#             for i in input_stream_list_or_file.split('|'):
#                 if len(i)!=0:
#                    input_list.append(i)
             input_list.extend(input_stream_list_or_file.split('|'))

    if len(input_list) == 0:
        logging.error("No input is set")
        sys.exit()
    
    logo_list=['']*len(input_list)
    if  len(logo_input)>0:
        tmp=logo_input.split('|')
        for i in range(len(tmp)):
            if i>=len(input_list):
                break;
            if len(tmp[i])>0:
                logo_list[i]=tmp[i]

    text_list=['']*len(input_list)
    if  len(text_input)>0:
        tmp=text_input.split('|')
        for i in range(len(tmp)):
            if i>=len(input_list):
                break;
            if len(tmp[i])>0:
                text_list[i]=tmp[i]
    
    
    if width == -1 or height == -1:
        logging.error("Invalid value of width or height")
        sys.exit()
    if rows == -1 or cols == -1:
        loggging.error("Invalid value of rows or cols")
        sys.exit()

    win_cnt = rows * cols

    if len(input_list) > win_cnt:
        logging.warning("Input streams are much more than  windows")
#         sys.exit()
        
    logging.info("input_list:%s" % input_list)
        
    if len(output) == 0:
        logging.error("Ouput is not set")
        sys.exit()

    pid_list = [''] * len(input_list) 
    # input_list=['udp://235.1.1.1:48880',
    #            'udp://235.1.1.1:48880',
    #            'udp://235.1.1.1:48880',
    #            'udp://235.1.1.1:48880',
    #            ]
    # output='udp://235.1.1.2:48880'

    # cmd = FFMPEG_BIN + " "
    # cmd += get_input_cl(input_list[0:win_cnt], pid_list) + " "
    # cmd += get_filter_cl(cols, rows, width, height, pid_list) + " "
    # cmd += get_output_cl(output)
    cl_list = []
    cl_list.append(FFMPEG_BIN)
    cl_list.append(get_input_cl(input_list, pid_list)) 
    cl_list.append(get_filter_cl(len(input_list),cols, rows, width, height, pid_list,logo_list,text_list)) 
    cl_list.append(get_output_cl(output))
    
    cmd = ' '.join(cl_list)

    
    logging.info(cmd)

    if do_execute == 0:
        sys.exit()

    pfile = None
    if len(trans_log)>0:
       pfile = open(trans_log, "w")

    if TIME_OUT==0:
        subprocess.call(cmd, shell=True, stdout=pfile, stderr=pfile)
    else:
        start = datetime.datetime.now()
        process = subprocess.Popen(cmd, stdout=pfile,stderr=pfile,shell=True,close_fds=True, preexec_fn = os.setsid)

        while process.poll() is None:
          time.sleep(1)
          now = datetime.datetime.now()
          time_passed=(now - start).seconds
          if time_passed> TIME_OUT:
              logging.warning("Time out, EXITING......")
              try:
                #process.terminate()
                os.killpg( process.pid,signal.SIGUSR1)
              except Exception,e:
                  sys.exit(0)
          else:
              logging.info("Process will be terminated after %s seconds"%(TIME_OUT-time_passed))
              
        pfile.close()
        sys.exit(0)
