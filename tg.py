#!/bin/python
# uncompress file under linux
__author__ = 'hfz2597'
import sys
import lib
import getopt
import os



def help():
    msg='''usage:tg.py [options] [path or file]
    -e <string> the extension which identify the compression type
    example: uncompress:
             tg.py a.tar.gz  : uncompress a.tar.gz to the current directory
             tg.py a.tar.gz b/ : uncompress a.tar.gz to directory b/
             tg.py a.txt : compress a.txt to a.tar.gz
             tg.py a.txt -e xz : compress a.txt to a.xz
             tg.py b/ : compress directory b/ to b.tar.gz
  '''
    print msg
    return
if __name__ == '__main__':
    if len(sys.argv) == 1:
        help()
        sys.exit()

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'e:Yh')
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    except Exception, e:
        print e

    extension = ''
    do_execute = 0

    for opt, arg in opts:
        if opt == "-e":
            extension = arg
        elif opt == "-Y":
            do_execute = 1
        elif opt == "-h":
            help()
            sys.exit()
        else:
            assert False, "unknown option"

    if len(args) == 0:
        print "Error: No input is specified, please check"
        sys.exit()

    input_file=''
    input_file=args[0]
    fname,fext=os.path.split(input_file)
    fname2=fname
    fext2=''
    if fname.endswith(".tar"):
        fname2,fext2=os.path.split(fname)
        assert fext2=='.tar'
    target_dir='.'
    if args>1:
        if os.path.isfile(args[1]):
            print 'Error:"%s" is a file which should be a directory, please check'
            sys.exit()
        elif not os.path.exists(args[1]):
            os.makedirs(args[1])#create the target directory
        target_dir=args[1]
    else:
        os.makedirs(fname2)#create a directory using the filename
        target_dir=fname2

    target_dir=lib.format_path(target_dir)

    cmd=''
    if fext.lower() in ('.tar','.gz','.tgz'):
        cmd+='tar zxvf "%s" -C "%s"'%(input_file,target_dir)
    elif fext.lower() in ('.bz2','.bz'):
        cmd+='tar jxvf "%s" -C "%s"'%(input_file,target_dir)
    elif fext.lower() in ('.z',):
        cmd+='tar Zxvf "%s" -C "%s"'%(input_file,target_dir)
    elif fext.lower() in ('.xz',):
        cmd+='tar Jxvf "%s" -C "%s"'%(input_file,target_dir)
    elif fext.lower() in ('.zip',):
        cmd+='unzip "%s" -d "%s"'%(input_file,target_dir)

    print cmd
    if do_execute==1:
        os.system(cmd)




