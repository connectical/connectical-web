#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

import os, time
try:
    import cPickle as pickle
except ImportError:
    import pickle

def get(key, expires=1800):
    try:
        obj = pickle.load( file(key, "r") )
        if int(time.time() - obj["created"]) > int(expires):
            return None
        else:
            return obj["contents"]
    except IOError:
        return None

def set(key, value):
    obj = {"created": time.time(), "contents": value}
    pickle.dump(obj, file(key, "w"))

