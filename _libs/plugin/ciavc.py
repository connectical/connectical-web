#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

import urllib
from xml.dom import minidom as dom
from datetime import datetime

def get(user):
    user = unicode(user, "utf-8")
    cia_user_url    = "http://cia.vc/stats/author/%s/.xml" % user
    cia_project_url = "http://cia.vc/stats/project/%s/.xml"

    print user
    fd = urllib.urlopen(cia_user_url)
    d = dom.parse(fd)

    ret = []
    revised = []
    for node in d.getElementsByTagName("message"):
        project = node.getElementsByTagName("source")[0] \
                      .getElementsByTagName("project")[0] \
                      .childNodes[0].nodeValue

        timestamp = node.getElementsByTagName("timestamp")[0].childNodes[0].nodeValue
        updated = datetime.fromtimestamp(int(timestamp))

        join=True

        if project in revised:
            continue

        revised.append(project)

        fp = urllib.urlopen(cia_project_url % project)
        p = dom.parse(fp)

        meta = p.getElementsByTagName("metadata")
        if len(meta) == 0 or len(meta[0].childNodes) == 0:
            continue

        for item in meta[0].getElementsByTagName("item"):
            if item.hasAttribute("name"):

                if item.getAttribute("name") == "description":
                   description = item.getElementsByTagName("value")[0].childNodes[0].nodeValue

                if item.getAttribute("name") == "url":
                   project_url = item.getElementsByTagName("value")[0].childNodes[0].nodeValue

        ret.append({
            "name": project,                # project name
            "description": description,     # project description
            "url": project_url,             # project URL
            "updated": updated.replace(tzinfo=None),   # last updated
            "author_url": "http://cia.vc/stats/author/%s" % user,
            "author": user })


    return ret

