#!/bin/python
__author__ = 'Felix'

import sys
sys.path.append("..")
from ffprobe import FFProbe
import logging

if __name__ == '__main__':
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
    print vst
    print ast
    print fmt
