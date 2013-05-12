#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

"""This module create the innovation area, parsing the people blog and
looking for special tags, like *labs* or *idea*.
"""

from hashlib import md5
from HTMLParser import HTMLParser

import feedparser
import cache
import ConfigParser

Site.CONTEXT.about = []
Site.CONTEXT.staff = []

try:
    for section in Site.CONTEXT.config.about.sections():
        Site.CONTEXT.about.append({
            "name": unicode(section, "utf-8").lower(),
            "summary": Site.CONTEXT.config.about.get(section, "summary"),
        }
        )
    for section in Site.CONTEXT.config.staff.sections():
        _x = Site.CONTEXT.config.staff._sections[section]
        _x["name"] = unicode(_x["__name__"], "utf-8")
        _x["links"] = {}
        for k,v in _x.items():
            if k.startswith("link_"):
                _x["links"][k.split("_",2)[1]] = v
        Site.CONTEXT.staff.append(_x)

except Exception, e:
    if Site.CONTEXT.config.debug.getboolean('debug','enabled') == True:
        raise
    else:
        raise
        print "error:about: %s" % e

