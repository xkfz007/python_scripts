#!/bin/python
# -*- coding: utf-8 -*-
__author__ = 'hfz2597'
import re

source = "s2f程序员杂志一2d3程序员杂志二2d3程序员杂志三2d3程序员杂志四2d3"
temp = source.decode('utf8')
xx = u"([/u4e00-/u9fa5]+)"
pattern = re.compile(xx)
results = pattern.findall(temp)
for result in results:
    print result
