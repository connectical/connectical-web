#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

identica_url = "http://identi.ca/api/statuses/user_timeline.json?screen_name=%s&count=5"

def get(user):
    return identica_url % user

