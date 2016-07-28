#!/usr/bin/python
__author__ = 'Felix'

import subprocess
import os, sys
import getopt
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logging
import time
import signal

ROOT_DIR = '/home/ubuntu/codec'
BIN_DIR = ROOT_DIR + '/release'
LOGO_DIR = ROOT_DIR + '/logo'


class Logo:
    def __init__(self, logo_path, logo_w, logo_h, logo_x, logo_y):
        self.path = logo_path
        self.w = logo_w
        self.h = logo_h
        self.x = logo_x
        self.y = logo_y

logo1 = Logo(LOGO_DIR + '/zb_44.tga', 92.25, 30.0, 24, 24)    
logo2 = Logo(LOGO_DIR + '/zb_44.tga', 122.81, 30.0, 42.93, 24)    
logo3 = Logo(LOGO_DIR + '/zb_67.tga', 186, 46, 64, 36)    
logo4 = Logo(LOGO_DIR + '/zb_100.tga', 279, 69, 96, 54)    

logo_map = {640:logo1,
          852:logo2,
          1280:logo3,
          1920:logo4,
          }

def get_logo(width, height, logo_path, logo_w, logo_h, logo_x, logo_y):
    cmd = '-vf "[in]scale=%s:%s[scaled_video];movie=%s,scale=%s:%s[logo];[scaled_video][logo]overlay=main_w-overlay_w-%s:%s[out]"'\
    % (width, height, logo_path, logo_w, logo_h, logo_x, logo_y)
    
    logging.debug(cmd)
    
    return cmd

def get_video_encoder(bitrate, profile, level, fps=25, keyint=50):
    cmd = '-c:v libx264 -preset superfast -profile:v %s -level:v %s -r %s -x264-params keyint=%s:scenecut=0 -b:v %sk'\
    % (profile, level, fps, keyint, bitrate)
    
    logging.debug(cmd)
    return cmd

def get_audio_encoder(bitrate, channel=2, sample_rate=44100, volume=1):
    cmd = '-c:a libfdk_aac -profile:a aac_low -b:a %sk -ac %s -ar %s -af volume=%s'\
    % (bitrate, channel, sample_rate, volume) 
    
    logging.debug(cmd)
    return cmd

def get_output_hls(hls_wrap=0, hls_time=10, hls_list_size=15, hls_flags='discont_start', hls_segment_filename='%d.ts', start_number=0, hlsdir=''):
    # using ' 
    opt_list = []
    opt_list.append('hls_wrap=%s' % hls_wrap)
    opt_list.append('hls_time=%s' % hls_time)
    opt_list.append('hls_list_size=%s' % hls_list_size)
    opt_list.append('hls_flags=' + hls_flags)
    opt_list.append("hls_segment_filename='%s/%s'" % (hlsdir, hls_segment_filename))
    opt_list.append('start_number=%s' % start_number)
    
    opt_str = ':'.join(opt_list)
    
    cmd = '[' + opt_str + ']'
    cmd += "'%s/01.m3u8'" % hlsdir
    
    logging.debug(cmd)
    return cmd


def get_multi_output(hls_opts, hls_dir_list):
    # using "
    output_list = []
    hls_wrap = hls_opts['hls_wrap']
    hls_time = hls_opts['hls_time']
    hls_list_size = hls_opts['hls_list_size']
    hls_flags = hls_opts['hls_flags']
    hls_segment_filename = hls_opts['hls_segment_filename']
    start_number = hls_opts['start_number']
    for dir in hls_dir_list:
        out_str = get_output_hls(hls_wrap, hls_time, hls_list_size, hls_flags, hls_segment_filename, start_number, dir)
        output_list.append(out_str)
    
    output_str = '|'.join(output_list)
    
    cmd = '-f tee "' + output_str + '"'
    
    logging.debug(cmd)
    return cmd
    
# def get_output_rtmp():
# def get_output_file():
# def get_output_udp():


def get_encoding_cl(pid, width, height, logo,
                    bitrate, profile, level,
                    abitrate, hls_opts, hls_dir_list):
    cl_list = []
    map_opt = '-map '
    if len(pid) == 0:
        map_opt += ' 0'
    else:
        map_opt += ' p:%s' % pid

    cl_list.append(map_opt)
    cl_list.append(get_logo(width, height, logo.path, logo.w, logo.h, logo.x, logo.y))
    cl_list.append(get_video_encoder(bitrate, profile, level))
    cl_list.append(get_audio_encoder(abitrate))
    cl_list.append("-sn  -metadata service_provider='WONDERTEK'")
    cl_list.append(get_multi_output(hls_opts, hls_dir_list))
    
    cmd = ' '.join(cl_list)

    logging.debug('encoding_cl=' + cmd)
    return cmd
    
    
def get_input_cl(input):
    pid = ""
    cl_list = []
    if input.startswith("rtsp://"):
        cl_list.append("-rtsp_flags prefer_tcp")
    if input.startswith("udp://"):
        input = input[6:]
        logging.debug(input)
        addr = input
        if '/' in input:
           addr, pid = input.split('/')
        input = '"udp://%s?overrun_nonfatal=1&buffer_size=100000000&fifo_size=10000000"' % addr
        
    cl_list.append('-i ' + input)
    cmd = ' '.join(cl_list)
    return cmd, pid


def get_monitor_merge_cl_list(hls_dir, output_dir, logfile, duration=10):
    cl_list = []
    monitor_bin = BIN_DIR + '/monitor_merge'
    # monitor_bin='monitor_upload'
    cl_list.append(monitor_bin)
    cl_list.append(hls_dir)
    cl_list.append(output_dir)
    cl_list.append("%s" % duration)
    cl_list.append('>' + logfile)
    cl_list.append('2>&1')
    cl_list.append('&')
    
#     cmd = ' '.join(cl_list)
#     return cmd
    return cl_list
    
    
def get_monitor_upload_cl_list(hls_dir, output_dir, logfile):
    cl_list = []
    monitor_bin = BIN_DIR + '/monitor_upload'
    cl_list.append(monitor_bin)
    cl_list.append(output_dir)
    cl_list.append(hls_dir)
    cl_list.append('>' + logfile)
    cl_list.append('2>&1')
    cl_list.append('&')
    
#     cmd = ' '.join(cl_list)
#     return cmd
    return cl_list
def check_dir(path):
    path = path.strip()  # delete the blankspace before or after the path
    path = path.rstrip('\\')
    path = path.rstrip('/')
    # chech whether the path exists or creat it
    if not os.path.exists(path):
        logging.info("Creating directory " + path)
        os.makedirs(path)

def check_monitor_merge_dirs(cl_list):
    check_dir(cl_list[1])
    check_dir(cl_list[2])

def check_monitor_upload_dirs(cl_list):
    check_dir(cl_list[2])
    
def upload_m3u8(ldir):
     # ## upload index.m3u8
     f = open(ldir + '/index.m3u8', 'w')
     f.write("#EXTM3U\n")
     f.write("#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2084544\n")
     f.write("01.m3u8\n")
     f.close()

# def parse_arg(opt, arg):
#
#    if 'x' not in arg.lower():
#         logging.error('Wrong format of "%s" with arg "%s"' % (opt, arg))
#         sys.exit()
#
#    x, y = arg.split('x')
#    w = int(x)
#    h = int(y)
#    return w, h

def parse_hls_arg(arg):
    x, y, z = arg.split(':')
    return int(x), int(y), int(z)

def parse_task(task):
    widthxheight, bitrate, profile, level, abitrate, out_str = task.split(':')
    w, h = widthxheight.split('x')
    output_dir_list = out_str.split('|')
    return int(w), int(h), int(bitrate), profile, level, int(abitrate), output_dir_list

def get_pid(cmd):
    pid = ""
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out,err = p.communicate()
    for line in out.splitlines():
        if cmd in line:
            pid = int(line.split(None, 1)[0])
            logging.info('Find process ' + pid)
            break
    return pid

# def run_cmd(cmd_line, do_execute=0, log_file='', rec_cl=0):
#    if len(cmd_line) == 0:
#        return
#    print cmd_line
#    if do_execute == 0:
#        return
#    pfile = None
#    if len(log_file) > 0:
#       pfile = open(log_file, "w")
#       if rec_cl == 1:
#          print >> pfile, "%s" % cmd_line
#          if sys.platform  in ('cygwin', 'linux2'):
#            cmd_line += " 2>&1 |tee -a %s" % log_file
#            pfile.close()
#            pfile = None
#
#    # os.system(cmd_line)
#    subprocess.call(cmd_line, yGshell=True, stdout=pfile, stderr=pfile)

def sigint_hander(signum, frame):
    for i in process_list:
        os.kill(i, signal.SIGKILL)
    sys.exit(0)


def usage():
    help_msg = '''USAGE:run_task.py [OPTIONS]... <stream1> <stream2> ...
   OPTIONS:
     -i <string>                                   the input stream 
     -n <string>                                   channel name 
     -h hls_wrap:hls_time:hls_list_size            hls options
     -t widthxheight:bitrate:profile:level:
        abitrate:output_dir      output windows
     -v <string>                                   loglevel
   Example:
     run_task.py -n "cctv3_test" -i "udp://235.1.1.2:48880" -h 10:10:15 \
                 -t 640x480:318:main:3.1:32:/mnt/remote/r4/wd_r4/test/cctv3_test/350 \
                 -t 852x480:568:main:3.1:32:/mnt/remote/r4/wd_r4/test/cctv3_test/600 \
                 -t 1280x480:1072:high:5.1:128:/mnt/remote/r4/wd_r4/test/cctv3_test/1200 \
   '''
    print help_msg
    return

if __name__ == '__main__':

    if len(sys.argv) == 1:
        usage()
        sys.exit()


    options = 'i:n:h:t:Yv:'

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], options)
    except getopt.GetoptError as err:
        logging.error(str(err))
        sys.exit(2)
    except Exception, e:
        logging.error(e)

    channel_name = ''
    input_stream = ''
    output = ''
    task_list = []
    do_execute = 0
    loglevel = logging.INFO
    log_map = {'info':logging.INFO,
             'debug':logging.DEBUG,
             'error':logging.ERROR,
             'warning':logging.WARNING}

    time_start = str(int(time.time()))
    time_prefix = time.strftime("%Y%m%d%H%M%S", time.localtime())
    hls_opts = {}
    hls_opts['hls_wrap'] = 20
    hls_opts['hls_time'] = 10          
    hls_opts['hls_list_size'] = 15
    hls_opts['hls_flags'] = 'discont_start'
    hls_opts['hls_segment_filename'] = time_prefix + '-01-%d.ts'
    hls_opts['start_number'] = time_start


    for opt, arg in opts:
        if opt == '-i':
            input_stream = arg
        elif opt == '-t':
            task_list.append(arg)
        elif opt == '-n':
            channel_name = arg
        elif opt == '-h':
            hls_opts['hls_wrap'], hls_opts['hls_time'], hls_opts['hls_list_size'] = parse_hls_arg(arg)
        elif opt == '-Y':
            do_execute = 1
        elif opt == '-v':
            loglevel = log_map[arg.lower()]
        else:
            loggging.error("Unrecognized option '%s'" % opt)
            sys.exit()
    
    logging.basicConfig(level=loglevel, format='[%(levelname)s]:%(message)s')
    
    if len(channel_name) == 0:
        logging.error("Please set channel name")
        sys.exit(0)
        
    if len(input_stream) == 0:
        logging.error("Please set input stream")
        sys.exit(0)

    if len(task_list) == 0:
        logging.error("Please set task output")
        sys.exit(0)
        


    cl_list = []
    monitor_cl_list = []
    
    FFMPEG_BIN = BIN_DIR + '/lvtranscode'
    cl_list.append(FFMPEG_BIN)
    cl_list.append('-hide_banner -threads auto -y  -itsoffset 0.5 -async 1')

#     input = 'udp://235.1.1.1:48880'
    input_cl, pid = get_input_cl(input_stream)

    cl_list.append(input_cl)

#     channel_name = 'cctv3_test'
#     bitrate_list = ['350', '600', '1200']

#     output_dir_list = []

#     do_execute=0
    
    for task in task_list:
        width, height, bitrate, profile, level, abitrate, output_dir_list = parse_task(task)

        out_cnt = len(output_dir_list)
        hls_dir_list = []
        for i in range(out_cnt):
            total_bitrate = bitrate + abitrate
            dpath = "%s_%s/%s_%s/%s_%s" % (channel_name , time_start, total_bitrate, time_start, i, time_start) 
            hls_dir_list.append(dpath)
            output_dir = output_dir_list[i]
            mon_logfile = "monitor_" + channel_name + '_' + str(total_bitrate) + '_' + str(i) + '.log'
            if output_dir.startswith('http://'):
                type = 1
            elif output_dir.startswith('/'):
                type = 0  # LOCAL_IDX
            if type == 0:
               monitor_cl_list.append(get_monitor_merge_cl_list(dpath, output_dir, mon_logfile, hls_opts['hls_time']))
            else:
               monitor_cl_list.append(get_monitor_upload_cl_list(dpath, output_dir, mon_logfile))

        task_enc_cl = get_encoding_cl(pid, width, height, logo_map[width],
                               bitrate, profile, level, abitrate, hls_opts, hls_dir_list)
        cl_list.append(task_enc_cl)
                   
    trans_log = channel_name + '_trans.log'
            
    cl_list.append('>' + trans_log)
    cl_list.append('2>&1')
    cl_list.append('&')
    
#     all_task_cl=' '.join(task_cl_list)
    
    logging.debug(cl_list)
    full_trans_cmd = ' '.join(cl_list)
#     print full_trans_cmd
    logging.info(full_trans_cmd)
    logging.debug(trans_log)
    
    logging.debug(monitor_cl_list)
    
    process_list = []
    
    for inner_lst in monitor_cl_list:
        logging.debug(inner_lst)
        mon_cmd = ' '.join(inner_lst)
        mon_logfile = channel_name + '_monitor.log'
#         print mon_cmd + "\n"
        logging.info(mon_cmd)
        if do_execute == 0:
            continue

        if inner_lst[0].endswith('monitor_merge'):
            check_monitor_merge_dirs(inner_lst)
            upload_m3u8(inner_lst[1])
        elif inne_lst[0].endswith('monitor_upload'):
            check_monitor_upload_dirs(inner_lst)
            upload_m3u8(inner_lst[2])
        
        subprocess.call(mon_cmd, shell=True, stdout=None, stderr=None)
#        run_cmd(mon_cmd, do_execute, mon_logfile, 1)
        pid = get_pid(mon_cmd)
        if len(pid) != 0:
            process_list.append(pid)
    
    if do_execute == 0:
        sys.exit(0)
    subprocess.call(full_trans_cmd, shell=True, stdout=None, stderr=None)
#    run_cmd(full_trans_cmd, do_execute, trans_log, 1)
    pid = get_pid(full_trans_cmd)
    if len(pid) != 0:
        process_list.append(pid)

    signal.signal(signal.SIGINT, sigint_hander)
    while True:
       pass 
