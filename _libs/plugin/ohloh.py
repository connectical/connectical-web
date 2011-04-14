#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

import feedparser


try:
    import xml.utils.iso8601 as isotime

    def dateparser(s):
        return datetime.fromtimestamp(isotime.parse(s))

except ImportError:
    import dateutil.parser as isotime

    def dateparser(s):
        return isotime.parse(s)

RSS_URL="http://www.ohloh.net/accounts/%s/projects.atom?sort=users"

def get(user):
    ret = []

    projects = feedparser.parse(RSS_URL % user)

    # Remove appeded title for category based feeds in wordpress
    for e in projects.entries:
        ret.append({
            "name": e.title,                 # project name
            "description": e.description,    # project description
            "url": e.link,                   # project URL
            "updated": dateparser(e.pub_date), # last update
            "author_url": projects.feed.link,
            "author": user })

    return ret

