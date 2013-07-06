#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

"""This hook provide a number of usefu filters to use in jinja
templates."""

import time, math
from random import randint
from hashlib import md5

@templateFilter
def uniqueid(link):
    return md5(link.encode('utf8','replace')).hexdigest()

@templateFilter
def toMonName(dt):
    return time.strftime("%b",dt)

@templateFilter
def dateFormat(dt, format='%Y-%m-%d'):
    try:
        return dt.strftime(format)
    except AttributeError:
        return time.strftime(format, dt)

@templateFilter
def tounicode(dt):
    return unicode(dt,"utf-8")

@templateFilter
def cutText(dt, l=255):
    if len(dt) > l:
        return dt[:l] + "..."
    else:
        return dt

@templateFilter
def toFontSize(count,maxm=5):
    return 100*(1.0+(1.5*count-maxm/2)/maxm)

@templateFilter
def toSpaceList(items):
    return " ".join(map(lambda x:x['term'],items))

@templateFilter
def firstword(s):
    if " " in s:
        return s.split(" ")[0]
    else:
        return s

@templateFilter
def tags(o):
    return ",".join(map(lambda x:"tag_%s" % x.replace(" ","_"), o.tags))

@templateFilter
def randomLines(o):
    if "\n" not in o:
        return o + "\n&nbsp;"*4
    o = o.split("\n")
    if len(o) > 5:
        _x = randint(0,len(o)-6)
        return "\n".join(o[_x:_x+5])
    while len(o) < 5:
        o.append("&nbsp;")
    return "\n".join(o)


