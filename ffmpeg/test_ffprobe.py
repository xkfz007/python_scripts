#!/bin/python
__author__ = 'Felix'

import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ffprobe import FFProbe
import utils

#if __name__ == '__main__':
def test_ff():
    if len(sys.argv[1:])!=1:
        logging.error("Wrong number of input arguments!")
        sys.exit()

    inputfile=sys.argv[1]
    m = FFProbe(inputfile)
    v_num=len(m.video)
    a_num=len(m.audio)
    #assert v_num==1 and a_num==1
    vst=m.video
    ast=m.audio
    #vcodec=vst.codec()
    #acodec=ast.codec()
    fmt=m.format
    print 'format:'
    print '\tformat_name=%s'%fmt.formatName()
    for a in vst:
        print 'video:'
        print '\tcodec_name=%s description=%s'%(a.codecName(),a.codecDescription())
    for a in ast:
        print 'audio:'
        print '\tcodec_name=%s description=%s language=%s'%(a.codecName(),a.codecDescription(),a.language())

if __name__ == "__main__":
    log = utils.Log('TEST','info')
    log.info("info")
    log.warning("warning")
    log.error("error")
