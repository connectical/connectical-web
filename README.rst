===========================
Connectical Website Creator
===========================

This is a Roar [1]_ based website for the Connectical site. This site is
modular and can retrieve data from many remote locations, including Git
repositories where available.

.. [1] http://pypi.python.org/pypi/roar

Configuration
=============

The configuration files are under ``_config`` directory. There are the
following configuration files:

``staff.conf``
  Configure the staff people, address and descriptions.

``cache.conf``
  Configure the update cache, where Git repositories are saved and
  blog articles cached.

``innovation.conf``
  Configure the innovation areas.

Deployment
==========

There are many ways to deploy a Connectical website mirror. Of course you
can choice your own way, but we recommended you this one:

0. Install some useful utilities::

   apt-get install python python-virtualenv

1. Choose a production directory (``/srv/git/connectical-web``, for example),
   to save the repository and clone the git repo::

   git clone git://github.com/Connectical/connectical-web

2. Choice a *virtualenv* directory (``/srv/venv/connectical-web`` in our
   example), and install the site::

    /srv/git/connectical-web/_tools/install /srv/venv/connectical-web \
                                            /srv/git/connectical-web


.. note:: To execute the install script you need to provide a base
    directory, which is the *virtualenv* directory. The working
    directory will be created into the *virtualenv* directory.

4. Build the site (from the repository directory)::

   /srv/venv/connectical-web/bin/roar .

5. Or try the update script::

   /srv/git/connectical-web/_tools/update /srv/venv/connectical-web \
                                          /srv/git/connectical-web

6. Serve the ``_deploy`` directory and enjoy! :D

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

The planet will link not only blog post, but also tweets (and `identi.ca`__
notices too) and any commit on staff's personal repositories.

__ http://identi.ca

