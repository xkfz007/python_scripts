#!/bin/python
__author__ = 'hfz2597'
import argparse

# parser = argparse.ArgumentParser(description='Short sample app',usage="Usage:./test.py [option] [value]...")
parser = argparse.ArgumentParser()

#parser.add_argument('-i', action="store", dest='input_file',help="input file name")
#parser.add_argument('-ss', action="store", dest='time_off',help="set the start time offset")
#parser.add_argument('-t', action="store", dest='duration', help="record or transcode 'duration' seconds of audio/video")
#parser.add_argument('-to', action="store", dest='time_stop',help=" record or transcode stop time")
#parser.add_argument('-H', action="store_true", default=False,dest='ff_help',help="show the ffmpeg help")
#parser.add_argument('-o', action="store", default=0,dest='operation',type=int,
#                    help="operations\n0: cut video\n1: get audio from video\n2: convert the video to pictures\n3: resize the video")
#parser.add_argument('-e', action="store", dest='extension',help=" extension of output file")
#parser.add_argument('-s', action="store", dest='size',help="set frame size (WxH or abbreviation)")
#parser.add_argument('-y', action="store_true", default=False,dest='overwrite',help="overwrite output files")
#parser.add_argument('-n', action="store_true", default=False,dest='overwrite',help="never overwrite output files")
#parser.add_argument('output_file', action="store", help="output file name")

#parser.add_argument('-ss', action="store", dest='time_off',help="set the start time offset")
parser.add_argument('-a', action="store_true", default=False, dest='a', help="overwrite output files")
parser.add_argument('-b', action="store_true", default=False, dest='b', help="overwrite output files")
parser.add_argument('-c', action="store_true", default=False, dest='c', help="overwrite output files")
parser.add_argument('-d', action="store_true", default=False, dest='d', help="overwrite output files")


#print parser.parse_args(['-a', '-bval', '-c', '3'])
results = parser.parse_args()
print results
