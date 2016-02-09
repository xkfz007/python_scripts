#!/bin/python
__author__ = 'Felix'
import sys
sys.path.append('..')
import lib
import sys
import fileinput
import os.pipe

if __name__=='__main__':
    print sys.getdefaultencoding()
    #reload(sys)
    #sys.setdefaultencoding('utf-8')
    #print sys.getdefaultencoding()
    input_list = []
    arg=sys.argv[1]
    lib.get_input_file_list(input_list, arg)
    tmp=open('a.txt','w')
    for i in input_list:
        #j=unicode(i.decode('utf-8'))
        print '%s'%i
        print isinstance(i,unicode)
        print isinstance(i,str)
        #print i.encode('gbk')
        #print unicode(i,'utf-8')
        #print i.decode('utf-8')
        #print '%s'%j.encode('gbk')
        #print i.decode('utf-8').encode('gbk')
        #print i.decode('utf-8').encode('gbk')
        line=i+'\n'
        #tmp.write(line.decode('utf-8').encode('ascii'))
        #tmp.write(j.encode('gbk'))
        #tmp.write(line.decode('gbk','ignore').encode('utf-8'))
        #print isinstance(line,str)
        tmp.write(line)
    tmp.close()


