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

config_field = "rss"

Site.CONTEXT.innovation = []

class MLStripper(HTMLParser):
    """A parser to strip html elements from a text.
    """

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    """This function remove HTML tags from a text.
    """
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def get_articles(area):
    ret = []
    for person in Site.CONTEXT.config.staff.sections():
        feed = Site.CONTEXT.config.staff.get(person, config_field)

        cache_key = os.path.join(
            Site.CONTEXT.config.cache.get("cache","cache_dir"),
            md5(feed).hexdigest())

        blog = cache.get(cache_key,
                expires=Site.CONTEXT.config.cache.get("cache","expires"))

        if not blog:
            blog = feedparser.parse(feed)
            if not blog.has_key("status") or blog["status"] != 200:
                print "warning:innovation:%s:feed %s return a non valid status. Skipping..." % (area, feed)
                continue
            cache.set(cache_key, blog)

        if len(blog.feed) == 0:
            print "warning:innovation:%s:feed %s is not available" % (
                    area, feed
            )
            continue

        # Remove appeded title for category based feeds in wordpress
        if blog.feed.title.find(u"»") != -1:
            blog.feed.title = blog.feed.title.split(u"»")[0]

        for e in blog.entries:
            if getattr(e,"tags", False):
                terms =  map(lambda x:x["term"].lower(),e.tags)
                if "idea" in terms or "labs" or "lab" in terms:
                    if "%s" % area in terms:
                        ret.append({"link":e.link,"title":e.title})

    return ret

try:
    for area in Site.CONTEXT.config.innovation.sections():
        Site.CONTEXT.innovation.append({
            "name": unicode(area, "utf-8").lower(),
            "summary": Site.CONTEXT.config.innovation.get(area, "summary"),
            "articles": get_articles(area.lower())
        })
except Exception, e:
    if Site.CONTEXT.config.debug.getboolean('debug','enabled') == True:
        raise
    else:
        print "error:innovation: %s" % e

