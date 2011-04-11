#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

"""
This hook will read the configuration file from the "_config" directory. Any
file with ".conf" extension will be parsed."""

import os
from glob import glob
import ConfigParser as cp

Site.CONTEXT.config = AttrDict()
for x in glob( os.path.join(Site.BASE_DIR, "_config") + "/*.conf" ):
    with file(x, "rU") as f:
        basename = os.path.basename(x).split(".")[0]
        Site.CONTEXT.config[basename] = cp.ConfigParser()
        Site.CONTEXT.config[basename].readfp(f)
