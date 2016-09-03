#!/usr/bin/python

import subprocess
import re
import time
import sys
import os
import datetime
import hashlib
#import warnings

import logging
import getopt
import signal


import smtplib  
from email.mime.text import MIMEText  
from email.header import Header  

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
    #print 'lines=%s'%lines
    start_tag='\['+tag.upper()+'\]'
    end_tag='\[\/'+tag.upper()+'\]'
    for a in iter(lines, b''):
        #print "a=%s"%a
        #print 'datalines=%s'%datalines
        if re.match(start_tag, a):
            datalines = []
        elif re.match(end_tag, a):
            streams.append(FFStream(datalines))
            datalines = []
        else:
            datalines.append(a)


def get_streams(channel,url,tag='STREAM'):
    streams = []
    logging.info("Checking %s:%s"%(channel,url))
    cmd= 'ffprobe -show_streams "%s"'%url
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    get_fftype(streams,p.stdout.readline,tag)
    get_fftype(streams,p.stderr.readline,tag)
    p.stdout.close()
    p.stderr.close()
    logging.info("Done......")
    return streams

def get_streams2(channel,url, timeout=5):
    start = datetime.datetime.now()
    streams=[]
    logging.info("Checking %s:%s"%(channel,url))
    cmd= 'ffprobe -show_streams "%s"'%url
    process = subprocess.Popen(cmd, bufsize=100000, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True, close_fds=True,preexec_fn = os.setsid)
    #logging.info("Analyzing stream......")
    while process.poll() is None:
      time.sleep(0.1)
      now = datetime.datetime.now()
      if (now - start).seconds> timeout:
          logging.warning("Time out......")
          try:
            #porcess.terminate()
            os.killpg( process.pid,signal.SIGTERM)
          except Exception,e:
            #warnings.warn(e)
            return streams
          return streams
    #out = process.communicate()[0]
    #print out
    logging.info("Analysing streams......")
    #print "readline1=%s"%(process.stdout.readline)
    #print "readline2=%s"%(process.stderr.readline)
    get_fftype(streams,process.stdout.readline,'STREAM')
    get_fftype(streams,process.stderr.readline,'STREAM')
    #if process.stdin:
    #  process.stdin.close()
    if process.stdout:
      process.stdout.close()
    if process.stderr:
      process.stderr.close()
    try:
      os.killpg( process.pid,signal.SIGTERM)
      #process.kill()
    except OSError:
      pass
    return streams

def send_email(sender,reciver,subject,text,username,password):
    #sender = '***'  
    #receiver = '***'  
    #subject = 'python email test'  
    #smtpserver = 'smtp.163.com'  
    #username = '***'  
    #password = '***'  
    
  
    msg = MIMEText(text,'text','utf-8') 
    msg['Subject'] = Header(subject, 'utf-8')  
      
    try:
        logging.warning('Sending Email.....')
        smtp = smtplib.SMTP()  
        smtp.connect('smtp.163.com',25)  
        smtp.login(username, password)  
        smtp.sendmail(sender, reciver, msg.as_string())  
        smtp.quit()
        logging.warning('Email has been sent out.....')
    except smtplib.SMTPException:
        logging.error('Email could not been sent out.....')


def notify_channel_disconnection(channel,url):
    sender='wondertek_test@163.com'
    reciver=['wondertek_test@163.com']
    subject='WARNING:%s'%channel
    username='wondertek_test@163.com'
    password='hfz123'#'123456@wd'
    text='Channel %s is disconnected:%s'%(channel,url)
    send_email(sender,reciver,subject,text,username,password)
    
def add_channel(chn_dict,str):
    chn = str.strip('\n')
    chn = chn.strip(' ')
    if len(chn)>0 and not chn.startswith('#'):
        if ' ' not in chn:
            logging.warning('No channel name of stream "%s"'%chn)
            url=chn
            name=hashlib.new("md5",url).hexdigest()[0:8].upper()
        else:
            name,url=chn.split(' ')
        channel_list[name.strip(' ')]=url.strip(' ')
    return 

def usage():
    help_msg = '''USAGE:stream_checker.py -i "<name1> <stream1>|<name2> <stream2>" ...
    or 
                        stream_ckecker.py -i <stream_list_file>
    OPTIONS:
     -i <name string|name string>/<file>   the input stream file list or multi input streams separated by '|'
     -T seconds                  Time out
     -L <file>                   output transcoder log
    If the stream is disconnected, an email will be send to wondertek_test@163.com(123456@wd)
   Example:
     stream_checker.py -i "CCTV1 udp://235.1.1.1:48880/2801|CCTV2 udp://235.1.1.1:48880/2802"
     stream_checker.py channel_list.txt 
     channel_list.txt:
     CCTV1     udp://236.114.126.13:5001
     CCTV1HD   udp://236.114.126.32:5001
     CCTV2     udp://236.114.126.13:5001
     CCTV5     udp://236.114.126.13:5001
     CCTV5HD   udp://236.114.126.42:5001
     CCTV5plus udp://236.114.126.21:5001
   '''
    print help_msg
    return

if __name__ == '__main__':
    #source=
    args=sys.argv[1:]
    #print args
    if len(args)<1:
        usage()
        sys.exit(0)

    options = 'L:i:hT:'

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], options)
    except getopt.GetoptError as err:
        logging.error(str(err))
        sys.exit(2)
    except Exception, e:
        logging.error(e)

    input_stream_list_or_file=''
    log_file=''
    TIME_OUT=10


    for opt, arg in opts:
        if opt == '-i':
            input_stream_list_or_file = arg
        elif opt=='-L':
            log_file=arg
        elif opt=='-T':
            TIME_OUT=int(arg)
        elif opt=='-h':
            usage()
            sys.exit(0)
        else:
            loggging.error("Unrecognized option '%s'" % opt)
            sys.exit()
    if len(log_file)>0:
       logging.basicConfig(level=logging.INFO,format='[%(asctime)s][%(levelname)s]:%(message)s',datefmt='%Y-%m-%d %H:%M:%S', filename=log_file)
    else:
       logging.basicConfig(level=logging.INFO,format='[%(asctime)s][%(levelname)s]:%(message)s',datefmt='%Y-%m-%d %H:%M:%S')
           
    input_file=''
    channel_list={}
    if len(input_stream_list_or_file) > 0:
        if os.path.exists(input_stream_list_or_file):
            input_file=input_stream_list_or_file
        else:
            for i in input_stream_list_or_file.split('|'):
                add_channel(channel_list, i)
            if len(channel_list) == 0:
                logging.error("No input is set")
                sys.exit()


    counter=0
    while True:
        counter=counter+1
        logging.info('=======Begin the round %s checking======='%counter)
        #channel_list={
        #          'CCTV1':'rtmp://61.178.152.174/live/live3',
        #          'CCTV2':'http://live.zzbtv.com:80/live/live123/800K/tzwj_video.m3u8',
        #          }

        if os.path.exists(input_file):
            logging.info("Reading input from file '%s'" % input_file)
            f = open(input_file, 'r')
            lines = f.readlines()
            f.close()
            for line in lines:
                add_channel(channel_list, line)

        for (channel,url) in channel_list.items():
            streams=get_streams2(channel,url)
            if len(streams)<=0:
                logging.error("Could not detect the channel %s(%s)"%(channel,url))
                #notify_channel_disconnection(channel, url)
            else:
                logging.info("Channel %s is in normal status:%s"%(channel,url))
    
        logging.info('=======Finish the round %s checking======='%counter)

        time.sleep(TIME_OUT)



