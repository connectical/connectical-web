#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

"""This hook create content for planet page, feeding code repositories
logs."""

from hashlib import md5
import cache
from ConfigParser import NoOptionError

Site.CONTEXT.planet.code = AttrDict(commits=[], links=[])

def add_fields(x, author, engine):
    x["author"] = author
    x["engine"] = engine
    return AttrDict(x)

try:
    for person in Site.CONTEXT.config.staff.sections():

        try:
            engine_s, user = Site.CONTEXT.config.staff.get(person, "planet.code").split(":")

            try:
                cache_key = os.path.join(
                        Site.CONTEXT.config.cache.get("cache","cache_dir"),
                        md5(engine_s+":"+user).hexdigest())

                code = cache.get(cache_key,
                       expires=Site.CONTEXT.config.cache.get("cache","expires"))

                engine = __import__("plugin." + engine_s, globals(),
                            locals(), [ "get" ], -1)

                if not code:
                    code = engine.get(user)
                    cache.set(cache_key, code)

                for c in code:
                    l = []
                    for commit in c["commits"]:
                        if commit["commit"]["committer"]["date"] >= c["updated"]:
                            l.append(commit)
                    if not l:
                        l = [ c["commits"][0] ]

                    c["commits"] = l

                code = map(lambda x:add_fields(x,unicode(person,"utf-8"),engine_s), code)
                Site.CONTEXT.planet.code.commits.extend(code)
                Site.CONTEXT.planet.code.links.append({"user":user,"link":engine.get_link(user),"engine":engine_s})

            except NotImplementedError:
                print "warning:planet_code:skip planet code for %s. Not supported engine: " % person, engine

        except NoOptionError:
            print "warning:planet_code:skip planet code for %s. None engine defined."  % person


    #Site.CONTEXT.planet.code.commits.sort(
    #        cmp = lambda x,y:
    #        cmp(y.updated.replace(tzinfo=None),x.updated.replace(tzinfo=None)) )

except Exception,e:
    if Site.CONTEXT.config.debug.getboolean('debug','enabled') == True:
        raise
    else:
        print "error:planet_code: %s" % e

