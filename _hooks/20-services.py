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

Site.CONTEXT.services = []

try:
    for service in Site.CONTEXT.config.services.sections():
        _e = []
        if Site.CONTEXT.config.services.has_option(service, "elements"):
            _x = Site.CONTEXT.config.services.get(service, "elements")
            _x = unicode(_x, "utf-8")
            for element in _x.split("|"):
                element = element.split(",")
                _e.append({
                    "link": element[0],
                    "name": element[1],
                    "description": ",".join(element[2:])
                })

        Site.CONTEXT.services.append({
            "name": unicode(service, "utf-8").lower(),
            "icon": Site.CONTEXT.config.services.get(service, "icon"),
            "summary": Site.CONTEXT.config.services.get(service, "summary"),
            "elements": _e
        })
except Exception, e:
    if Site.CONTEXT.config.debug.getboolean('debug','enabled') == True:
        raise
    else:
        print "error:services: %s" % e

