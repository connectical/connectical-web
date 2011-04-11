#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from ConfigParser import NoOptionError

Site.CONTEXT.planet.tweet = AttrDict( tweets=[], links=[] )

for person in Site.CONTEXT.config.staff.sections():

    try:
        engine_s, user = Site.CONTEXT.config.staff.get(person, "planet.tweet").split(":")

        try:
            engine = __import__("plugin." + engine_s, globals(),
                    locals(), [ "get" ], -1)

            tweet = engine.get(user)

            Site.CONTEXT.planet.tweet.tweets.append(tweet)
            Site.CONTEXT.planet.tweet.links.append({"user":user,"link":tweet})

        except NotImplementedError:
            print "[build]   Skip planet tweet for %s. Not supported engine: " % person, engine

    except NoOptionError:
        print "[build]   Skip planet tweet for %s. None engine defined." % person


