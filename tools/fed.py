#!/bin/python
__author__ = 'Felix'
#file encoding detect
import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils
import chardet

def usage():
    help_msg = '''USAGE:fed.py <filename>
   '''
    print help_msg
    return

if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
        sys.exit()

    args=sys.argv[1:]
    input_list=[]
    for arg in args:
         utils.get_input_file_list(input_list, arg)
    #print input_list
    for i in input_list:
        f=open(i,'r')
        fenc=chardet.detect(f.read())
        print '"%s":%s'%(i,fenc)
        f.close()

