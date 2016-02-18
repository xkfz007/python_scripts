#!/bin/python
__author__ = 'Felix'
import sys
sys.path.append('..')
import lib
import sys

if __name__=='__main__':
    print sys.getdefaultencoding()
    #reload(sys)
    #sys.setdefaultencoding('utf-8')
    #print sys.getdefaultencoding()
    input_list = []
    arg=sys.argv[1]
    lib.get_input_file_list(input_list, arg)
    cmd='ffmpeg -y'
    size=len(input_list)
    pipe_list=[]
    for i in range(0,size):
        pipe_list.append('temp%s'%i)

