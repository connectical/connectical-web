===========================
Connectical Website Creator
===========================

This is a growl [1]_ based website for Connectical site. This site is
modular and can retrieve data from many remote locations, including git
repos where available.

.. [1] http://furi-ku.org/+/cgit/code/growl/

Configuration
=============

The configuration files are under ``_config`` directory. There are the
following configuration files:

staff.conf
  Configure the staff people, address and descriptions.

cache.conf
  Configure the update cache, where git repos are saved and blog articles
  cached.

innovation.conf
  Configure the innovation areas.


Innovation
==========

The innovation area links a number of articles from the staff blogs, all
articles tagged with "labs" tag are candidates to be included in innovation,
but only if also has another tag which match with some research area name.
For example, if the area "cloud" exists, and an article is tagged with
"labs" and "cloud" then will be included in innovation page, into cloud research
area.

Planet
======

The planet will link not only blog post, but also tweets (and identi.ca
notices too) and any commit on staff's personal repos.

