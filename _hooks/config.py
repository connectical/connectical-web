#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

"""
This hook will read the configuration file from the "_config" directory. Any
file with ".conf" extension will be parsed."""

import os, errno
from glob import glob
import ConfigParser as cp

Site.CONTEXT.config = AttrDict()
for x in glob( os.path.join(Site.BASE_DIR, "_config") + "/*.conf" ):
    with file(x, "rU") as f:
        basename = os.path.basename(x).split(".")[0]
        Site.CONTEXT.config[basename] = cp.ConfigParser()
        Site.CONTEXT.config[basename].readfp(f)

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

