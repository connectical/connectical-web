#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

"""This hook create content for products page, feeding from different
projects hubs, like ohlot."""

from hashlib import md5
import cache
from ConfigParser import NoOptionError

Site.CONTEXT.products = []

def qa_test(project):
    if len(project.name) == 0:
        print "warning:products:QA: Malformed data, project has no name!"
        return False

    if len(project.description) == 0:
        print "warning:products:QA: Project %s has no description." % project.name
        return False

    if len(project.author) == 0:
        print "warning:products:QA: Project %s has no author." % project.name
        return False

    if len(project.url) == 0:
        print "warning:products:QA: Project %s has no URL." % project.name
        return False

    if project.updated is None:
        print "warning:products:QA: Project %s has not updated time." % project.name
        return False

    return True

def add_fields(x, author, engine):
    x["author"] = author
    x["engine"] = engine
    return AttrDict(x)

try:
    for person in Site.CONTEXT.config.staff.sections():

        try:
            engine_s, user = Site.CONTEXT.config.staff.get(person, "products").split(":")

            try:
                cache_key = os.path.join(
                        Site.CONTEXT.config.cache.get("cache","cache_dir"),
                        md5(engine_s+":"+user).hexdigest())

                code = cache.get(cache_key,
                       expires=Site.CONTEXT.config.cache.get("cache","expires"))

                if not code:
                    engine = __import__("plugin." + engine_s, globals(),
                            locals(), [ "get" ], -1)

                    code = engine.get(user)
                    cache.set(cache_key, code)

                for c in code:
                    data = add_fields(c, user, engine_s)
                    if qa_test(data) and \
                       data["name"] not in map(lambda x:x["name"], Site.CONTEXT.products):
                           Site.CONTEXT.products.append(data)

            except NotImplementedError:
                print "warning:products:skip products for %s. Not supported engine: " % person, engine

        except NoOptionError:
            print "warning:products:skip products for %s. None engine defined." % person

    # Export to the environment the products list.
    Site.CONTEXT.products.sort(
            cmp = lambda x,y:
            cmp(y.updated.replace(tzinfo=None),x.updated.replace(tzinfo=None)) )

except Exception, e:
    if Site.CONTEXT.config.debug.getboolean('debug','enabled') == True:
        raise
    else:
        print "error:products: %s" % e



