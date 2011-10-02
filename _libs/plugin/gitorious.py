#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from datetime import datetime
from xml.dom import minidom as dom
import git, shutil, urllib, os

try:
    import xml.utils.iso8601 as isotime

    def dateparser(s):
        return datetime.fromtimestamp(isotime.parse(s))

except ImportError:
    import dateutil.parser as isotime

    def dateparser(s):
        return isotime.parse(s)

class Commit(object):
    def __init__(self,d):
        for key in d.keys():
            setattr(self,key,d[key])

def fixdates(d):
    d["committed_date"] = datetime.fromtimestamp(d["committed_date"])
    d["authored_date"]  = datetime.fromtimestamp(d["authored_date"])
    return Commit(d)

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def get_link(user):
    return "http://gitorious.org/~%s" % user

def get (user):

    fd = urllib.urlopen("http://gitorious.org/~%s/repositories.xml" % user)
    d = dom.parse(fd)
    ret = []

    for node in d.getElementsByTagName("repository"):
        created_at   = node.getElementsByTagName("created-at")[0].childNodes[0].nodeValue
        last_update  = node.getElementsByTagName("last-pushed-at")[0].childNodes
        if len(last_update) < 1:
            continue
        last_update  = last_update[0].nodeValue
        project_name = node.getElementsByTagName("project")[0].childNodes[0].nodeValue
        project_line = node.getElementsByTagName("name")[0].childNodes[0].nodeValue
        if len(node.getElementsByTagName("description")[0].childNodes):
            description  = node.getElementsByTagName("description")[0].childNodes[0].nodeValue
        else:
            description = ""
        project_url  = "http://gitorious.org/%s" % project_name
        git_url      = node.getElementsByTagName("clone-url")[0].childNodes[0].nodeValue


        # TODO: Move repo cache path to config file.
        if not os.path.isdir("_cache"):
            os.mkdir("_cache")

        if not os.path.isdir("_cache/" + project_name):
            git_repo = git.repo.Repo.init("_cache/" + project_name)
            git_repo.create_remote('test', git_url)
        else:
            git_repo = git.repo.Repo("_cache/" + project_name)

        test = git_repo.remotes.test
        commits = []
        for info in test.fetch():
            commit = info.commit
            commits.append({
                "id": commit.hexsha,
                "url": "http://gitorious.org/%s/%s/commit/%s" \
                    % ( project_name, project_line, commit.hexsha),
                "message": commit.message,
                "committed_date": commit.committed_date,
                "authored_date": commit.authored_date });

        updated = dateparser(last_update)
        created = dateparser(created_at)
        if len(project_line) >0 and project_line != "mainline":
            project_name = project_name + "/" + project_line

        ret.append({
            "name": project_name,                # Repo name
            "description": description  ,        # Repo description
            "url": project_url,                  # Repo URL
            "updated": updated.replace(tzinfo=None),  # Repo last updated
            "created": created.replace(tzinfo=None),   # Repo created time
            "commits": map(fixdates, commits[:5]),
            "author_url": "http://gitorious.org/~%s" % user,
            "author": user
        })

    return ret

