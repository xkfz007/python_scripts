#!/bin/python
#a simple yuv player which is implemented by wrapping ffplay using python
__author__ = 'hfz2597'
import getopt
import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils
import os

BIN='ffplay.exe'
logger=utils.Log('YP')

def usage():
    msg='''USAGE: f.py [OPTIONS]... [FILE]...
   OPTIONS:
     -E <width:height:fps>/<widthxheightxfps>
                              resolution parameters
   FILE:
     files that we want to display
  '''
    print msg
    return

def parse_reso_fps(arg,width=-1,height=-1,fps=-1,delimiter='x'):
    x,y,z=utils.parse_arg(arg,delimiter,str(width),str(height),str(fps))
    return int(x),int(y),int(z)

default_seq_path='f:/sequences/'
if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
        sys.exit()

    help=utils.HELP(usage,BIN,'--help',logger)
    options='E:'
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], options +help.get_opt())
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    except Exception, e:
        print e

    width=-1
    height=-1
    fps=-1
    for opt, arg in opts:
        if opt == '-E':
            width,height,fps=parse_reso_fps(arg,width,height,fps)
        else:
            help.parse_opt(opt)

    if len(args) == 0:
        logger.error('No input is specified, please check')
        sys.exit()
    input_file=args[0]
    dpath = os.path.dirname(input_file)
    name = os.path.basename(input_file)
    name = utils.seq_list.guess_seqname(name)
    if len(dpath)==0:
        dpath=default_seq_path
    input_file= os.path.join(dpath, name+'.yuv')
    if not os.path.exists(input_file):
        logger.error('Input "%s" doesn\'t exist, please check'%input_file)
        sys.exit()

    if width<0 or height<0 or fps<0:
        width, height, fps = utils.get_reso_info(name)

    cmd=BIN
    cmd += ' -i "%s"' % input_file
    cmd += ' -f rawvideo'
    cmd += ' -video_size %sx%s' % (width, height)
    cmd += ' -framerate %s' % fps

    utils.run_cmd(cmd,help.get_do_execute())

    #cmd_line="ffplay.exe -i f:/sequences/Dblowingbubbles_416x240_8_50_500.yuv  -f rawvideo -video_size 416x240"
    #subprocess.Popen(cmd_line,stdout=None,stderr=None,shell=True)
    #subprocess.Popen(cmd_line,stdout=None,stderr=None,shell=True)
