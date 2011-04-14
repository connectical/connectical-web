#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:


from hashlib import md5
from HTMLParser import HTMLParser
import PyRSS2Gen
import datetime
import feedparser
import cache

Site.CONTEXT.planet = AttrDict()
Site.CONTEXT.planet.blog = AttrDict()
Site.CONTEXT.planet.blog.post = []
Site.CONTEXT.planet.blog.feed = []

atom_feed = PyRSS2Gen.RSS2(
        title = "Connectical Planet Feed",
        link  = "http://connectical.com/planet",
        description = "Planet for Connectical staff and collaborators",
        lastBuildDate = datetime.datetime.utcnow(),
        items = []
)


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


for person in Site.CONTEXT.config.staff.sections():

    feed = Site.CONTEXT.config.staff.get(person, "planet.blog")

    cache_key = os.path.join(
        Site.CONTEXT.config.cache.get("cache","cache_dir"),
        md5(feed).hexdigest())

    blog = cache.get(cache_key,
            expires=Site.CONTEXT.config.cache.get("cache","expires"))

    if not blog:
        blog = feedparser.parse(feed)
        cache.set(cache_key, blog)

    # Remove appeded title for category based feeds in wordpress
    if blog.feed.title.find(u"»") != -1:
        blog.feed.title = blog.feed.title.split(u"»")[0]

    Site.CONTEXT.planet.blog.feed.append(AttrDict(
        title = blog.feed.title,
        link = blog.feed.link,
        author = unicode(person,"utf-8") ))

    for e in blog.entries:
        atom_feed.items.append(PyRSS2Gen.RSSItem(
            title = e.title,
            link  = e.link,
            author = unicode(person,"utf-8"),
            description = e.content[0].value,
            pubDate = e.updated
        ))

        Site.CONTEXT.planet.blog.post.append(AttrDict(
            title = e.title,
            author = unicode(person,"utf-8"),
            author_url = blog.feed.link,
            author_avatar = Site.CONTEXT.config.staff.get(person, "about.avatar"),
            updated = e.updated_parsed,
            updated_str = e.updated,
            url = e.link,
            content = e.content[0].value,
            text_content = strip_tags(e.content[0].value)))

Site.CONTEXT.planet.blog.post.sort( cmp = lambda x,y: cmp(y.updated,x.updated) )
Site.CONTEXT.planet.blog.post = Site.CONTEXT.planet.blog.post[0:5]

atom_feed.write_xml(open("planet/feed/index.xml", "w"))

