#!/bin/python
__author__ = 'Felix'
import time
import sys
import logging
import os.path
logging.basicConfig(level=logging.INFO,format='[%(levelname)s]:%(message)s')

def task():
    print "task ..."

def timer(n):
    while True:
        print time.strftime('%Y-%m-%d %X',time.localtime())
        task()
        time.sleep(n)

url_dict={
    'video1-jygmobile-zh'       :   'http://221.181.100.24:8088/wd_r1/jygmobile/zh/200/index.m3u8?is_ec=1',
    'video2-jygmobile-gg'       :   'http://221.181.100.24:8088/wd_r1/jygmobile/gg/200/index.m3u8?is_ec=1',
    'video6-gesee-chcdzdy'      :   'http://221.181.100.24:8088/wd_r1/gesee/chcdzdy/200/index.m3u8?is_ec=1',
    'video19-nfmedia-zjdy'      :   'http://221.181.100.24:8088/wd_r1/nfmedia/zjdy/200/index.m3u8?is_ec=1',
    'video20-nfmedia-nfys'      :   'http://221.181.100.24:8088/wd_r1/nfmedia/nfys/200/index.m3u8?is_ec=1',
    'video67-cntv-zzet'         :   'http://221.181.100.24:8088/wd_r1/cntv/zzet/200/index.m3u8?is_ec=1',
    'video68-cntv-zzst'         :   'http://221.181.100.24:8088/wd_r1/cntv/zzst/200/index.m3u8?is_ec=1',
    'video26-peoplecn-szfz'     :   'http://221.181.100.24:8088/wd_r1/peoplecn/szfz/200/index.m3u8?is_ec=1',
    'video27-peoplecn-szyl'     :   'http://221.181.100.24:8088/wd_r1/peoplecn/szyl/200/index.m3u8?is_ec=1',
    'video28-peoplecn-szdsj'    :   'http://221.181.100.24:8088/wd_r1/peoplecn/szdsj/200/index.m3u8?is_ec=1',
    'video29-peoplecn-sztyjk'   :   'http://221.181.100.24:8088/wd_r1/peoplecn/sztyjk/200/index.m3u8?is_ec=1',
    'video30-peoplecn-nnys'     :   'http://221.181.100.24:8088/wd_r1/peoplecn/nnys/200/index.m3u8?is_ec=1',
    'video51-cztv-zsxwzh'       :   'http://221.181.100.24:8088/wd_r1/cztv/zsxwzh/200/index.m3u8?is_ec=1',
    'video52-cztv-zsggsh'       :   'http://221.181.100.24:8088/wd_r1/cztv/zsggsh/200/index.m3u8?is_ec=1',
    'video53-cztv-zsqdly'       :   'http://221.181.100.24:8088/wd_r1/cztv/zsqdly/200/index.m3u8?is_ec=1',
    'video11-northvideo-lnty'   :   'http://221.181.100.24:8088/wd_r1/northvideo/lnty/200/index.m3u8?is_ec=1',
    'video12-northvideo-lnysj'  :   'http://221.181.100.24:8088/wd_r1/northvideo/lnysj/200/index.m3u8?is_ec=1',
    'video13-northvideo-lnds'   :   'http://221.181.100.24:8088/wd_r1/northvideo/lnds/200/index.m3u8?is_ec=1',
    'video14-northvideo-lnsh'   :   'http://221.181.100.24:8088/wd_r1/northvideo/lnsh/200/index.m3u8?is_ec=1',
    'video15-northvideo-lnjyqs' :   'http://221.181.100.24:8088/wd_r1/northvideo/lnjyqs/200/index.m3u8?is_ec=1',
    'video16-northvideo-lnbf'   :   'http://221.181.100.24:8088/wd_r1/northvideo/lnbf/200/index.m3u8?is_ec=1',
    'video17-northvideo-lnyjgw' :   'http://221.181.100.24:8088/wd_r1/northvideo/lnyjgw/200/index.m3u8?is_ec=1',
    'video31-cutv-nndssh'       :   'http://221.181.100.24:8088/wd_r1/cutv/nndssh/200/index.m3u8?is_ec=1',
    'video32-cutv-zzzh'         :   'http://221.181.100.24:8088/wd_r1/cutv/zzzh/200/index.m3u8?is_ec=1',
    'video33-cutv-lzxw'         :   'http://221.181.100.24:8088/wd_r1/cutv/lzxw/200/index.m3u8?is_ec=1',
    'video34-cutv-hhhtxwzh'     :   'http://221.181.100.24:8088/wd_r1/cutv/hhhtxwzh/200/index.m3u8?is_ec=1',
    'video35-cutv-nngg'         :   'http://221.181.100.24:8088/wd_r1/cutv/nngg/200/index.m3u8?is_ec=1',
    'video36-cutv-zzfz'         :   'http://221.181.100.24:8088/wd_r1/cutv/zzfz/200/index.m3u8?is_ec=1',
    'video37-cutv-hhhtysyl'     :   'http://221.181.100.24:8088/wd_r1/cutv/hhhtysyl/200/index.m3u8?is_ec=1',
    'video38-cutv-nnxwzh'       :   'http://221.181.100.24:8088/wd_r1/cutv/nnxwzh/200/index.m3u8?is_ec=1',
    'video39-cutv-zzss'         :   'http://221.181.100.24:8088/wd_r1/cutv/zzss/200/index.m3u8?is_ec=1',
    'video40-cutv-lzkj'         :   'http://221.181.100.24:8088/wd_r1/cutv/lzkj/200/index.m3u8?is_ec=1',
    'video41-cutv-hhhtdssh'     :   'http://221.181.100.24:8088/wd_r1/cutv/hhhtdssh/200/index.m3u8?is_ec=1',
    'video42-cutv-hylive'       :   'http://221.181.100.24:8088/wd_r1/cutv/hylive/200/index.m3u8?is_ec=1',
    'video43-cutv-lzgg'         :   'http://221.181.100.24:8088/wd_r1/cutv/lzgg/200/index.m3u8?is_ec=1',

    }

import subprocess
import threading
class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    #def getResults(self):
    #    return self.res

    def run(self):
        logging.info('staring [', self.name, '] at: ', time.ctime())
        #self.res = self.func(*self.args)
        self.func(*self.args)
        logging.info('\t [', self.name, '] done at: ', time.ctime())


def play_channels(channel_list,step=1):
    for cha in channel_list:
        #url='http://221.181.100.24:8088/wd_r1/peoplecn/nnys/200/index.m3u8?is_ec=1'
        #url=url_dict[cha]
        num,owner,chn=cha.split('-')
        url='http://221.181.100.24:8088/wd_r1/'+owner+'/'+chn+'/'+'200/index.m3u8?is_ec=1'
        #url=url.replace('200','600')
        #cmd='vlc --video-on-top %s'%url
        cmd='vlc %s'%url
        #cmd='ffplay %s'%url
        logging.info('start to play %s:%s'%(cha,url))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #p = subprocess.Popen(cmd)
        logging.info('playing %s'%url)
        time.sleep(2.0*60)
        logging.info('time up, terminating....')
        p.terminate()
        logging.info('terminated')


def test_loop(label,num):
    for i in range(num,num+10):
        print '%s:%s'%(label,i)

    #thread.exit_thread()


if __name__=='__main__':

    channel_released_list=[
        'video1-jygmobile-zh',
        'video2-jygmobile-gg',
        'video6-gesee-chcdzdy',
        'video19-nfmedia-zjdy',
        'video20-nfmedia-nfys',
        'video67-cntv-zzet',
        'video68-cntv-zzst',
        ]
    channel_unreleased_list=[
        'video26-peoplecn-szfz',
        'video27-peoplecn-szyl',
        'video28-peoplecn-szdsj',
        'video29-peoplecn-sztyjk',
        'video30-peoplecn-nnys',
        'video32-cutv-zzzh',
        'video33-cutv-lzxw',
        'video34-cutv-hhhtxwzh',
        'video35-cutv-nngg',
        'video36-cutv-zzfz',
        'video37-cutv-hhhtysyl',
        'video38-cutv-nnxwzh',
        'video39-cutv-zzss',
        'video40-cutv-lzkj',
        'video41-cutv-hhhtdssh',
        'video42-cutv-hylive',
        'video43-cutv-lzgg',
        #'video51-cztv-zsxwzh'video31-cutv-nndssh'
        #'video52-cztv-zsggsh',
        #'video53-cztv-zsqdly',
        #'video11-northvideo-lnty',
        #'video12-northvideo-lnysj',
        #'video13-northvideo-lnds',
        #'video14-northvideo-lnsh',
        #'video15-northvideo-lnjyqs',
        #'video16-northvideo-lnbf',
        #'video17-northvideo-lnyjgw',
    ]

    if len(sys.argv) == 1:
        logging.error('Not enough parameters!')
        sys.exit()

    if not os.path.exists(sys.argv[1]):
        logging.error('File %s does not exist!'%sys.argv[1])
        sys.exit()
    input_file=sys.argv[1]
    f=open(input_file,'r')
    lines=f.readlines()
    f.close()

    chn_list=[]
    for line in lines:
        #print line.strip('\n')
        chn=line.strip('\n')
        chn=chn.strip(' ')
        if not chn.startswith('#') and len(chn)>0:
            chn_list.append(chn)
            print chn

    #thread.start_new_thread(play_channels,(channel_released_list,))
    #thread.start_new_thread(play_channels,(channel_unreleased_list,))
    #play_channels(channel_released_list)

    #t1=MyThread(play_channels,(channel_released_list,),'A')
    #t2=MyThread(play_channels,(channel_unreleased_list,),'B')

    #t1.start()
    #t2.start()

    #t1.join()
    #t2.join()


    try:
        play_channels(chn_list)
    except KeyboardInterrupt:
        print "User Press Ctrl+C,Exit"
    except EOFError:
        print "User Press Ctrl+D,Exit"

