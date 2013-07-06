#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

"""This hook create content for products page, feeding from different
projects hubs."""

from random import randint
from hashlib import md5
from github import Github

Site.CONTEXT.products = []

try:
    if "credentials" in Site.CONTEXT.config:
        user = Site.CONTEXT.config.credentials.get("github","username")
        pswd = Site.CONTEXT.config.credentials.get("github","password")
        credentials = (user, pswd)

    else:
        credentials = (None,None)
    gh = Github(*credentials)
    count = 0

    for person in Site.CONTEXT.config.staff.sections():
        ghid = Site.CONTEXT.config.staff.get(person, "github", None)
        if not ghid:
            continue

        cache_key = os.path.join(
                Site.CONTEXT.config.cache.get("cache","cache_dir"),
                md5("gh_%s" % ghid).hexdigest()
        )

        repos = cache.get(cache_key, expires=10800) or {}

        ret = {}
        try:
            for repo in gh.get_user(ghid).get_repos():
                count += 2
                if repo.name not in repos:
                    count += 1
                    if "whistlerbot" in [ x.login for x in repo.get_collaborators() ]:
                        try:
                            readme = repo.get_readme().content.decode("base64")
                        except:
                            readme = None

                        try:
                            patch = repo.get_commits()[0].files[0].patch
                        except:
                            patch = None

                        ret[repo.name] = {
                                "name": repo.name,
                                "url": repo.homepage or "https://github.com/%s/%s" % (ghid, repo.name,),
                                "description": repo.description,
                                "author": ghid,
                                "updated": repo.updated_at,
                                "new": True,
                                "readme": unicode(readme, "utf-8"),
                                "patch": patch,
                                "language": repo.language.lower(),
                        }
                    else:
                        ret[repo.name] = None
                    cache.set(cache_key, ret)
                    if count > 1880:
                        # Github API limit... wait an hour :'(
                        print "Prevent Github abuse. Stopping reading repos."
                        break
                else:
                    ret[repo.name]=repos[repo.name]
                    if repos[repo.name]:
                        ret[repo.name]["new"]=False

            repos = ret
        except:
            raise
            repos = {}
        Site.CONTEXT.products.extend(filter(lambda x:x is not None,repos.values()))

    # Export to the environment the products list.
    Site.CONTEXT.products.sort(
            cmp = lambda x,y:
            cmp(y["updated"].replace(tzinfo=None),x["updated"].replace(tzinfo=None)) )

except Exception, e:
    if Site.CONTEXT.config.debug.getboolean('debug','enabled') == True:
        raise
    else:
        print "error:products: %s" % e



