#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from github.github import GitHub
from datetime import datetime
try:
    import xml.utils.iso8601 as isotime

    def dateparser(s):
        return datetime.fromtimestamp(isotime.parse(s))

except ImportError:
    import dateutil.parser as isotime

    def dateparser(s):
        return isotime.parse(s)

def fixdates(d):
    d.committed_date = dateparser(d.committed_date)
    d.authored_date  = dateparser(d.authored_date)
    return d

def get_link(user):
    return "http://github.com/" + user

def get (user):
    gh = GitHub() # unauthorized user
    ret = []

    for r in gh.repos.forUser(user):
        ret.append({
            "name": r.name,                      # Repo name
            "description": r.description,        # Repo description
            "url": r.url,                        # Repo URL
            "updated": dateparser(r.pushed_at),  # Repo last updated
            "created": dateparser(r.created_at), # Repo created time
            "commits": map(fixdates, gh.commits.forBranch(user, r.name)[:5]),
            "author_url": "http://github.com/" + user,
            "author": user
        })

    return ret

