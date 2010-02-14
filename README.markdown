Music Inbox
===========

Music Inbox is a service that gives you access to information about your music library through a REST interface. 

Installation
============

Dependencies
------------
 * [Django][1]
 * [Django-registration][2]
 * [lxml][3]

Setup
-----

    $ git clone git://github.com/aroscoe/music-inbox.git
    $ cd music-inbox/
    music-inbox $ git submodule update --init
    music-inbox $ ./manage.py syncdb
    music-inbox $ ./manage.py runserver

Your local Django server should be running now. Upload a library and try out some of the following REST calls.

REST API
========

*Coming soon...*

Authors
=======
* [Tim Julien][4]
* [Anthony Roscoe][5]
* [Felix Berger][6]

[1]: http://www.djangoproject.com
[2]: http://code.google.com/p/django-registration
[3]: http://codespeak.net/lxml
[4]: http://github.com/tjulien
[5]: http://github.com/aroscoe
[6]: http://github.com/fberger
