#!/bin/python
__author__ = 'hfz2597'
# convert videos: resize videos from large resolution to small one
import lib
import os
import subprocess

if __name__ == "__main__":
    dirt = "f:/QQDownload/The.Wire"
    file_list = lib.common_lib.get_file_list(dirt)
    cmd_line = "ffmpeg.exe -y"
    for i in file_list:
        file_size = os.path.getsize(i)
        basename = os.path.basename(i)
        file_name, ext = os.path.splitext(basename)
        output_name = file_name + "_small" + ext
        output_full_name = os.path.join(dirt, output_name)
        # %print "%s:%sB=%sKB=%sMB"%(i,file_size,file_size/1024,file_size/1024/1024)
        cmd_tmp = cmd_line
        cmd_tmp += " -i %s" % i
        cmd_tmp += " -fs %sM" % (file_size / 1024 / 1024 / 4)
        cmd_tmp += " %s" % output_full_name
        print cmd_tmp
        subprocess.call(cmd_tmp, stdout=None, shell=True)
