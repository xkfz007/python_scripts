#!/usr/bin/python
import os
import sys
import lib
import subprocess

dec_id = "hmd"
#dec = lib.Decoder_prop(dec_id)
dec=lib.DECODER(dec_id)

param_list = lib.get_default_dec_param_list()

# lib.configure_dec_param(dec,param_list)
cons = lib.parse_dec_cl(dec, param_list)
print dec

cmd_line = lib.get_full_cdec_cmd(dec, param_list)

#reg_file = None
#if lib.determin_sys() == "cygwin":
#    cmd_line += (" 2>&1 |tee -a " + cons)
#    pf = open(cons, "w")
#    print >> pf, "%s" % cmd_line
#    pf.close()
#else:
#    reg_file = open(cons, 'w')
#
## os.system(cmd_line)
#print cmd_line
#subprocess.call(cmd_line, shell=True, stdout=reg_file, stderr=reg_file)
lib.run_cmd(cmd_line,cons,1)
