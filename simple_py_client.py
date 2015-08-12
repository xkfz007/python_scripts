#!/bin/python
#This is a simple file read clinet
__author__ = 'hfz2597'
import xmlrpclib
#proxy = xmlrpclib.ServerProxy('http://172.21.40.170:8001')
#f=proxy.file_reader(r'F:\encoder_test_output\as265_output\DEBUG_RC_WHOLE_PROCESS_ABR_rls.txt')
#print f
proxy = xmlrpclib.ServerProxy('http://172.21.40.25:8002')# Attention: http is needed
f=proxy.file_reader(r'E:\hfz\a.py')
print f
