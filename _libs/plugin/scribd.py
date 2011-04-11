#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

import urllib2

CALLBACK_PREFIX = "ScribdX.DocWidget.WIDGETS[0].callback("
CALLBACK_SUFFIX = ")"

scribd_collection_url = \
        "http://www.scribd.com/public_document_collections/%s/0.js"

def get(user):
    handle = urllib2.urlopen(scribd_collection_url % user)
    js_str = handle.read()
    d = eval(js_str[len(CALLBACK_PREFIX):-len(CALLBACK_SUFFIX)])
    return d["documents"]

