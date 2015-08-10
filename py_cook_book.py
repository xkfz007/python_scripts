#!/bin/python
__author__ = 'hfz2597'
import string
# Checking Whether a String Is Text or Binary

def istext(s, threshold=0.30):
    text_characters = "".join(map(chr, range(32, 127))) + "\n\r\t\b"
    _null_trans = string.maketrans("", "")
    # if s contains any null, it's not text:
    if "\0" in s:
        return False
    # an empty string is "text" (arbitrary but reasonable choice):
    if not s:
        return True
    # Get the substring of s made up of non-text characters
    t = s.translate(_null_trans, text_characters)
    # s is 'text' if less than 30% of its characters are non-text ones:
    return len(t) / len(s) <= threshold


def istextfile(filename, blocksize=512, **kwds):
    return istext(open(filename).read(blocksize), **kwds)
