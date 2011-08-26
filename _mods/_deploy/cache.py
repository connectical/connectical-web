#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

"""This hooks initialize the cache properties and check than the cache
exists."""

# Set sane cache config defaults
if not Site.CONTEXT.config.cache.has_option("cache", "cache_dir"):
    Site.CONTEXT.config.cache.set("cache", "cache_dir", "_cache")

if not Site.CONTEXT.config.cache.has_option("cache", "expires"):
    Site.CONTEXT.config.cache.set("cache", "expires", 1800)

# Ensure that the cache directory exists
try:
    os.makedirs(Site.CONTEXT.config.cache.get("cache", "cache_dir"))
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

