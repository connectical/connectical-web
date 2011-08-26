#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

"""This hook provide a number of usefu filters to use in jinja
templates."""

import time, math
from hashlib import md5

@templateFilter
def uniqueid(link):
    return md5(link).hexdigest()

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

