#!/bin/python
# uncompress file under linux
__author__ = 'hfz2597'
import sys
import lib
import getopt
import os
import logging
gz_name_list=('.tar.gz','.tgz','.gz')
xz_name_list=('.tar.xz','.txz','.xz')
bz_name_list=('.tar.bz','.tbz','.bz',
              '.tar.bz2','.tb2','.bz2')
z_name_list=('.z',)
tar_name_list=gz_name_list+\
              xz_name_list+\
              bz_name_list+\
              z_name_list

zip_name_list=('.zip',)

compression_name_list=tar_name_list+ zip_name_list

def usage():
    msg='''USAGE:tg.py [OPTIONS] [PATH or FILE]
    OPTIONS:
      -e <string> compress files using this extension:
                    -tgz/tar.gz
                    -txz/tar.xz
                    -tbz/tar.bz
                    -tb2/tar.bz2
                    -zip
      -o <string> the output name of compressed file,include filename and extension
                  this option is useful when you want to compress several files into one
      -d          force to uncompress files to a directory
    EXAMPLES:
      tg.py a.tar.gz  : uncompress a.tar.gz to the current directory
      tg.py a.tar.gz b/ : uncompress a.tar.gz to directory b/
      tg.py a.txt : compress a.txt to a.tar.gz
      tg.py a.txt -e xz : compress a.txt to a.xz
      tg.py b/ : compress directory b/ to b.tar.gz
      tg.py a.txt b.txt c.txt -o a.zip: compress files to a.zip
  '''
    print msg
    return

def get_compr_app_cmd(ext):
    compr=''
    if ext in gz_name_list:
        compr='z'
    elif ext in xz_name_list:
        compr='J'
    elif ext in bz_name_list:
        compr='j'
    elif ext in z_name_list:
        compr='Z'
    return compr


if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
        sys.exit()

    help=lib.common_lib.HELP(usage)
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'e:o:d'+help.get_opt())
    except getopt.GetoptError as err:
        logging.error(str(err))
        sys.exit(2)
    except Exception, e:
        print e

    extension = '.zip' #default
    compress_flag=0  # <=0 for uncompress, >=1 for compress
    input_file=''

    for opt, arg in opts:
        if opt == "-e":
            extension = arg
            compress_flag=1
        elif opt == '-o':
            input_file=arg
            compress_flag=2
        elif opt=='-d':
            compress_flag=-1
        else:
            help.parse_opt(opt)

    if len(args) == 0:
        logging.error("No input is specified, please check")
        sys.exit()

    if len(input_file)==0:
        input_file=args[0]

    fname,fext=os.path.splitext(input_file)
    logging.info("fname=%s fext=%s"%(fname,fext))

    if fname.endswith('.tar'):
        fname2,fext2=os.path.splitext(fname)
        assert fext2=='.tar'
        fname=fname2
        fext=fext2+fext

    logging.info("NEW:fname=%s fext=%s"%(fname,fext))
    #if fext in compression_name_list:
    #    compress_flag=0

    cmd=''
    if compress_flag <= 0:
        logging.info("Uncompress file %s"%input_file)
        target_dir='.'
        if len(args)>1:
            if os.path.isfile(args[1]):
                logging.error('"%s" is a file which should be a directory, please check')
                sys.exit()
            target_dir=args[1]
        else:
            if compress_flag==-1:
                target_dir=fname
        target_dir=lib.format_path(target_dir)
        if not os.path.exists(target_dir):
           os.makedirs(target_dir)#create a directory using the filename

        fext=fext.lower()
        if fext in tar_name_list:
            compr=get_compr_app_cmd(fext)
            cmd+='tar %sxvf "%s" -C "%s"'%(compr,input_file,target_dir)
        elif fext in zip_name_list:
            cmd+='unzip "%s" -d "%s"'%(input_file,target_dir)

    elif compress_flag > 0:
        logging.info("Compress file %s"%input_file)
        #if len(extension)==0:
            #extension='.zip'#default compression extension
        if compress_flag ==2 :
            extension=fext
        if not extension.startswith('.'):
            extension='.'+extension

        file_list=[]
        file_list.extend(args)
        target_file=fname+extension
        if extension in tar_name_list:
            compr=get_compr_app_cmd(extension)
            cmd+='tar %scvf "%s" '%(compr,target_file)
        elif extension in zip_name_list:
            cmd+='zip -r "%s" '%target_file
        for i in file_list:
            cmd+='"%s" '%i

    else:
        logging.error('invaild value of compress_flag, please check')
        sys.exit()

    print cmd
    if help.get_do_execute()==1:
        os.system(cmd)



