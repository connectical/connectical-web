#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

"""This module generate contents for planet page, feeding with the blogs
definitions."""

from hashlib import md5
from HTMLParser import HTMLParser
import datetime
import feedparser
import cache

Site.CONTEXT.talks = []

class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


try:

    for person in Site.CONTEXT.config.staff.sections():

        if not Site.CONTEXT.config.staff.has_option(person, "talks"):
            continue

        feed = Site.CONTEXT.config.staff.get(person, "talks")

        cache_key = os.path.join(
            Site.CONTEXT.config.cache.get("cache","cache_dir"),
            md5(feed).hexdigest())

        blog = cache.get(cache_key,
                expires=Site.CONTEXT.config.cache.get("cache","expires"))

        if not blog:
            blog = feedparser.parse(feed)
            if not blog.has_key("status") or int(blog["status"]) != 200:
                print "warning:talks:feed %s returns a non valid status" % feed
                continue
            cache.set(cache_key, blog)

        if len(blog.feed) == 0:
            print "warning:talks:feed %s is not available" % feed
            continue

        for e in blog.entries:
            try:
                content = e.content[0].value
            except AttributeError:
                content = e.summary_detail.value
            atom_feed.items.append(PyRSS2Gen.RSSItem(
                title = e.title,
                link  = e.link,
                author = unicode(person,"utf-8"),
                description = content,
                pubDate = e.updated
            ))
 
            Site.CONTEXT.talks.append(AttrDict(
                title = e.title,
                image = e.slideshare_thumbnail if getattr(e,"slideshare_thumbnail", False) else "",
                author = unicode(person,"utf-8"),
                author_url = blog.feed.link,
                updated = e.updated_parsed,
                updated_str = e.updated,
                url = e.link,
                embed = e.slideshare_embed if getattr(e, "slideshare_embed", False) else "",
                content = content
            ))


    Site.CONTEXT.talks.sort( cmp = lambda x,y: cmp(y.updated,x.updated) )

except Exception, e:
    if Site.CONTEXT.config.debug.getboolean('debug','enabled') == True:
        raise
    else:
        print "error:talks: %s" % e

