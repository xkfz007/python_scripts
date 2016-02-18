#!/usr/bin/env python    
# encoding: utf-8

# copy source from http://blog.csdn.net/five3/article/details/7630295
import sys
import ctypes
import logging

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

#FOREGROUND_BLACK = 0x0
#FOREGROUND_BLUE = 0x01  # text color contains blue.
#FOREGROUND_GREEN = 0x02  # text color contains green.
#FOREGROUND_CYAN= 0x03
#FOREGROUND_RED = 0x04  # text color contains red.
#FOREGROUND_PINK= 0x05
#FOREGROUND_YELLOW = 0x06
#FOREGROUND_INTENSITY = 0x08  # text color is intensified.

#BACKGROUND_BLUE = 0x10  # background color contains blue.
#BACKGROUND_GREEN = 0x20  # background color contains green.
#BACKGROUND_RED = 0x40  # background color contains red.
#BACKGROUND_INTENSITY = 0x80  # background color is intensified.

LEVELS={'debug':   logging.DEBUG,
        'info':    logging.INFO,
        'warning': logging.WARNING,
        'error':   logging.ERROR,
        'critical':logging.CRITICAL,
        }
if sys.platform in ('cygwin','linux2'):
    COLORS={'red'   : '\033[1;31;40m',
            'green' : '\033[1;32;40m',
            'yellow': '\033[1;33;40m',
            'blue'  : '\033[1;34;40m',
            'pink'  : '\033[1;35;40m',
            'cyan'  : '\033[1;36;40m',
            'none'  : '\033[0m',
            }
elif sys.platform in ('win32',):
    COLORS={'red'   : 0x04,
            'green' : 0x02,
            'yellow': 0x06,
            'blue'  : 0x01,
            'cyan'  : 0x03,
            'pink'  : 0x05,
            'none'  : 0x08,#FOREGROUND_INTENSITY
    }

class Log:
    ''''' See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winprog/winprog/windows_api_reference.asp
    for information on Windows APIs.'''
    def set_level(self,level):
        self.logger.setLevel(LEVELS[level])

    def __init__(self,name,level='info',format='[%(levelname)s]:%(message)s'):
        self.logger = logging.getLogger(name)
        #self.logger.setLevel(logging.level)
        self.hdr=logging.StreamHandler()
        self.hdr.setFormatter(logging.Formatter(format))
        self.logger.addHandler(self.hdr)
        self.set_level(level)

    if sys.platform in ('cygwin','linux2'):
        def set_cmd_color(self, color):
            sys.stdout.write(COLORS[color])#print without line feed
            sys.stdout.flush()
    elif sys.platform in ('win32',):
        def set_cmd_color(self, color):
            ctypes.windll.kernel32.SetConsoleTextAttribute(
               ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE), COLORS[color])

    def reset_color(self):
        #print '\033[0m'','
        #sys.stdout.write(COLORS['none'])
        #sys.stdout.flush()
        self.set_cmd_color('none')
        return

    def error(self, text):
        self.set_cmd_color('red')
        self.logger.error(text)
        self.reset_color()

    def warning(self, text):
        self.set_cmd_color('yellow')
        self.logger.warning(text)
        self.reset_color()

    def info(self, text):
        self.set_cmd_color('green')
        self.logger.info(text)
        self.reset_color()



if __name__ == "__main__":
    log = Log('TEST','info')
    log.info("info")
    log.warning("warn")
    log.info("info")
    log.warning("warn")
    log.error("error")
    log.info("info")
    log.warning("warn")
    log.error("error")
