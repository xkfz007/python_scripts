#!/usr/bin/python

import subprocess
import re
import time
import sys
import os
import datetime

import logging
logging.basicConfig(level=logging.INFO,format='[%(levelname)s]:%(message)s')


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

def get_streams2(channel,url, timeout=20):
    start = datetime.datetime.now()
    streams=[]
    logging.info("Checking %s:%s"%(channel,url))
    cmd= 'ffprobe -show_streams "%s"'%url
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
      process.kill()
    except OSError:
      pass
    return streams

#def get_streams2(channel,url,tag='STREAM'):
#    streams = []
#    logging.info("Checking %s:%s"%(channel,url))
#    cmd= 'ffprobe -show_streams "%s"'%url
#    outlines=timeout_command(cmd, 20)
#    get_fftype(streams,outlines,tag)
#    logging.info("Done......")
#    return streams


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
        if '|' not in chn:
            logging.warning('Invalid format of "%s"'%chn)
            return 
        name,url=chn.split('|')
        channel_list[name.strip(' ')]=url.strip(' ')
    return 

if __name__ == '__main__':
    #source=
    args=sys.argv[1:]
    print args
    if len(args)<1:
        logging.error("Not enough parameters")
        sys.exit(0)
    input_file=''
    channel_list={}
    if len(args)==1 and os.path.exists(args[0]):
        input_file=args[0]
    else:
        for i in args:
            add_channel(channel_list, i)
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
                notify_channel_disconnection(channel, url)
            else:
                logging.info("Channel %s is in normal status:%s"%(channel,url))
    
        logging.info('=======Finish the round %s checking======='%counter)

        time.sleep(10)



