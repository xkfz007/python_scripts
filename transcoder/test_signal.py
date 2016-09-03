#!/usr/bin/python
import signal
import time

EXIT=False
def signal_handler(signum, frame):
        global EXIT
        print('Received signal: ', signum)
        EXIT=True
        print 'EXIT=%s'%EXIT
def signal_handler2(signum, frame):
        print('Received signal: ', signum)
        print('we will exit')


signal.signal(signal.SIGHUP, signal_handler) # 1
signal.signal(signal.SIGINT, signal_handler) # 2
while True:
        #signal.signal(signal.SIGQUIT, signal_handler) # 3
        #signal.signal(signal.SIGALRM, signal_handler) # 14
        #signal.signal(signal.SIGTERM, signal_handler) # 15
        #signal.signal(signal.SIGCONT, signal_handler) # 18
        print('waiting,EXIT=%s'%EXIT)
        time.sleep(1)
        if EXIT==True:
            print 'Exit=%s'%EXIT
            break
        #while True:
        #    print('waiting')
        #    time.sleep(1)
print "OK,we get out of the while loop"
