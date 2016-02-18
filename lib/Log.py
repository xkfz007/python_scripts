#!/usr/bin/env python    
# encoding: utf-8

# copy source from http://blog.csdn.net/five3/article/details/7630295
import sys
import ctypes
import logging

if sys.platform == 'linux2':
    from termcolor import colored, cprint

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

FOREGROUND_BLACK = 0x0
FOREGROUND_BLUE = 0x01  # text color contains blue.
FOREGROUND_GREEN = 0x02  # text color contains green.
FOREGROUND_RED = 0x04  # text color contains red.
FOREGROUND_INTENSITY = 0x08  # text color is intensified.

BACKGROUND_BLUE = 0x10  # background color contains blue.
BACKGROUND_GREEN = 0x20  # background color contains green.
BACKGROUND_RED = 0x40  # background color contains red.
BACKGROUND_INTENSITY = 0x80  # background color is intensified.


class Log:
    ''''' See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winprog/winprog/windows_api_reference.asp
    for information on Windows APIs.'''
    '''
    DEBUG: 1
    ERROR:2
    WARNING: 3
    INFO:4
    '''
    ERROR=0
    WARNING=1
    INFO=2
    DEBUG=3

    def set_loglevel(self,level):
        if level==self.ERROR:
            self.logger.setLevel(logging.ERROR)
        elif level==self.DEBUG:
            self.logger.setLevel(logging.DEBUG)
        elif level==self.WARNING:
            self.logger.setLevel(logging.WARNING)
        elif level==self.INFO:
            self.logger.setLevel(logging.INFO)

    def __init__(self,name,level=2,format='[%(levelname)s]:%(message)s'):
        self.logger = logging.getLogger(name)
        #self.logger.setLevel(logging.level)
        self.hdr=logging.StreamHandler()
        self.hdr.setFormatter(logging.Formatter(format))
        self.logger.addHandler(self.hdr)
        self.set_loglevel(level)
    if sys.platform == 'linux2':
        # red_on_cyan = lambda x: colored(x, 'red', 'on_cyan')
        # print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')

        def set_cmd_color(self, color):
            return

        def reset_color(self, color):
            return

        def error(self, print_text):
            print colored(print_text, 'red')
            return

        def warn(self, print_text):
            print colored(print_text, 'green')
            return

        def info(self, print_text):
            print colored(print_text, 'grey')
            return

    elif sys.platform == "win32":
        std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

        def set_cmd_color(self, color, handle=std_out_handle):
            """(color) -> bit
            Example: set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY)
            """
            bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
            return bool

        def reset_color(self):
            self.set_cmd_color(FOREGROUND_INTENSITY)

        def error(self, print_text):
            self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY)
            #print print_text
            self.logger.error(print_text)
            self.reset_color()

        def warn(self, print_text):
            self.set_cmd_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
            #print print_text
            self.logger.warn(print_text)
            self.reset_color()

        def info(self, print_text):
            #print print_text
            self.logger.info(print_text)


if __name__ == "__main__":
    log = Log('TEST',2)
    log.info("info")
    log.warn("warn")
    log.info("info")
    log.warn("warn")
    log.error("error")
    log.info("info")
    log.warn("warn")
    log.error("error")
