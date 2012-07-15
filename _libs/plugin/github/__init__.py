#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from .github3 import client
from .github3.client import Repo
from datetime import datetime

try:
    import xml.utils.iso8601 as isotime

    def dateparser(s):
        return datetime.fromtimestamp(isotime.parse(s))

except ImportError:
    import dateutil.parser as isotime

    def dateparser(s):
        return isotime.parse(s)

def get_commits(repo, maxn=5):
    count = 0
    ret = []
    for x in repo.commits():
        ret.append(fixcommit(x))
        count +=1
        if count == maxn:
            return ret

    return ret


def fixcommit(d):
    #d.committed_date = dateparser(d.committed_date)
    #d.authored_date  = dateparser(d.authored_date)
    #d.url = "http://github.com" + d.url
    d["commit"]["author"]["date"] = dateparser(d["commit"]["author"]["date"])
    d["commit"]["committer"]["date"] = dateparser(d["commit"]["committer"]["date"])
    return d

def get_link(user):
    return "http://github.com/" + user

def get (user):
    gh = client.Client() # unauthorized user
    ret = []

    for r in gh.list_repo(user=user):
        repo = Repo(gh, user, r["name"])
        ret.append({
             "name": r["name"],                      # Repo name
             "description": r["description"],        # Repo description
             "url": r["url"],                   # Repo URL
             "updated": dateparser(r["pushed_at"]),  # Repo last updated
             "created": dateparser(r["created_at"]), # Repo created time
             "commits": get_commits(repo),
             "author_url": "http://github.com/" + user,
             "author": user
        })

    return ret

