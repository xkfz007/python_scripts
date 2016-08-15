#!/usr/bin/python
from cookielib import logger
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

TIME_OUT=0
EXIT=False

def usage():
    help_msg = '''USAGE:do_single_job.py [OPTIONS] [ARGS] [ARGS] ....
   OPTIONS:
     -t seconds                  execution  duration
   ARGS:
     <commandline>            command line that will be executed in shell
   '''
    print help_msg
    return
def signal_handler(signum, frame):
    #print('Received signal: ', signum)
    EXIT=True

if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        usage()
        sys.exit()


    options = 't:Yv:'

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], options)
    except getopt.GetoptError as err:
        logging.error(str(err))
        sys.exit(2)
    except Exception, e:
        logging.error(e)

    do_execute = 0
    cmd_list=[]
    log_list=[]
    loglevel = logging.INFO
    log_map = {'info':logging.INFO,
             'debug':logging.DEBUG,
             'error':logging.ERROR,
             'warning':logging.WARNING}


    for opt, arg in opts:
        if opt == '-t':
            TIME_OUT= int(arg)
        elif opt == '-Y':
            do_execute = 1
        elif opt == '-v':
            loglevel = log_map[arg.lower()]
        else:
            loggging.error("Unrecognized option '%s'" % opt)
            sys.exit()
    
    logging.basicConfig(level=loglevel, format='[%(levelname)s]:%(message)s')
    
    if len(args)<1:
        logging.error('Not enough arguments')
        sys.exit()
    
    i=0
    for j in args:
        cmd_list.append(j)
        log_name='job_%s.log'%i
        log_list.append(log_name)
        i=i+1

    if len(cmd_list)<1:
        logging.error('There is no job to do')
        sys.exit()

    
    cmd_cnt=len(cmd_list)
    logging.info('We will execute the following commands(%s):'%cmd_cnt)
    for i in range(0,cmd_cnt):
        logging.info('\t%s >%s'%cmd_list[i],log_list[i])

    if do_execute == 0:
        sys.exit()

    pfile_list=[]
    process_list=[]
    for i in range(0,cmd_cnt):
       pfile = open(log_list[i], "w")
       process = subprocess.Popen(cmd_list[i], stdout=pfile,stderr=pfile,shell=True,close_fds=True, preexec_fn = os.setsid)
       pfile_list.append(pfile)
       process_list.append(process)

    if TIME_OUT==0:
        #subprocess.call(cmd, shell=True, stdout=pfile, stderr=pfile)
        while EXIT==False:
            signal.signal(signal.SIGINT, signal_handler)
        
    else:
        start = datetime.datetime.now()
        time_passed=0
        #process = subprocess.Popen(cmd, stdout=pfile,stderr=pfile,shell=True,close_fds=True, preexec_fn = os.setsid)
        while EXIT==False and time_passed<TIME_OUT:
          signal.signal(signal.SIGINT, signal_handler)
          time.sleep(1)
          now = datetime.datetime.now()
          time_passed=(now - start).seconds
#           if time_passed> TIME_OUT:
#               logging.warning("Time out")
#               break;
#               #try:
#               #  #process.terminate()
#               #  os.killpg( process.pid,signal.SIGUSR1)
#               #except Exception,e:
#               #    sys.exit(0)
#           else:
          logging.info("Process will be terminated after %s seconds"%(TIME_OUT-time_passed))
              
    try:
      #process.terminate()
      logging.warning('EXITING......')
      for i in range(0,cmd_cnt):
          os.killpg( process_list[i].pid,signal.SIGUSR1)
          pfile_list[i].close()
          logging.warning('job %s is KILLED'%i)
    except Exception,e:
        sys.exit(0)

#     if len(trans_log)>0:
#         pfile.close()
    sys.exit(0)
