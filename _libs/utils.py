#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from fnmatch import fnmatch
from HTMLParser import HTMLParser

class ImgHTMLParser(HTMLParser):
    ban_urls = [ "http://s?.wp.com/*", "http://stats.wordpress.com/*", "http://feeds.wordpress.com/*"  ]
    src = None
    def handle_starttag(self, tag, attrs):
        if tag == "img" and self.src is None:
            _x = dict(attrs)["src"]
            for b in self.ban_urls:
                if fnmatch(_x, b):
                    return
            if "?" in _x:
                _x = _x.split("?")[0]
            self.src=_x

def get_img(content):
    parser = ImgHTMLParser()
    parser.feed(content)
    return parser.src


