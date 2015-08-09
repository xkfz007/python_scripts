#!/bin/python
__author__ = 'hfz2597'
# concatenate some video files
import sys
import os
import subprocess

if __name__ == "__main__":
  file_list = sys.argv[1:]
  ffmpeg_bin = "ffmpeg.exe -y"
  file_list2 = []
  #convert the files to .ts
  for i in file_list:
    filename, ext = os.path.splitext(i)
    outfile = filename + ".ts"
    file_list2.append(outfile)
    cmd_line = ffmpeg_bin
    cmd_line += " -i %s -c copy -bsf:v h264_mp4toannexb %s " % (i, outfile)
    subprocess.call(cmd_line, stdout=None, shell=True)
    #concat the .ts files
  #concat_str="concat:"
  #for i in file_list2:
  #  concat_str+="%s|"%i
  concat_str = "|".join(file_list2)
  #concat_str=concat_str[0:-1]
  print concat_str
  merged_file = "all.mp4"
  cmd_line = ffmpeg_bin
  cmd_line += ' -i "concat:%s" -c copy -bsf:a aac_adtstoasc %s' % (concat_str, merged_file)
  subprocess.call(cmd_line, stdout=None, shell=True)

