#!/usr/bin/env python
#
# vim:syntax=python:sw=4:ts=4:expandtab

"""
This module provide an HTML optimization, that is, whitespace removal and
merge all in one large line... Not useful to humans, but save a couple of
Kbits in bandwith terms."""

import sys
from slimmer import xhtml_slimmer

@wrap(Page.render)
def optimize(forig, self, **kwargs):
    return xhtml_slimmer(forig(self, **kwargs))

