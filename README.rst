===========================
Connectical Website Creator
===========================

This is a Roar [1]_ based website for the Connectical site. This site is
modular and can retrieve data from many remote locations, including Git
repos where available.

.. [1] http://pypi.python.org/pypi/roar

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

Deployment
==========

There are many ways to deploy a Connectical website mirror. Of course you
can choice your own way, but we recommended you this one:

0. Install some useful utilities::

   apt-get install python python-virtualenv growl

.. note:: The growl package which some minor modifications (such as yml
    remplacement) is available in http://apt.igalia.com

1. Choice a production directory for save the repository and clone the
   git repo::

   git clone git://github.com/Connectical/connectical-web

2. Choice a virtualenv directory (``/var/venv/connectical-web`` in our
   example), and install virtualenv::

   virtualenv /srv/venv/connectical-web

3. Join into git repository and execute the following command to install the
   requirements into the venv::

   /srv/venv/connectical-web/bin/pip install -r requirements.txt

.. note:: Some modules can be use any native module, so a combo of
    gcc/make is a good idea to improve performance. If you do not provide
    this tools, modules just take a pure python implementation.


4. Build the site (from the repository directory)::

   /srv/venv/connectica-web/bin/roar .

5. Serve the ``_deploy`` directory and enjoy! :D

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

