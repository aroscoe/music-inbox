Music Inbox
===========

Music Inbox is a service that gives you access to information about your music library through a REST interface. 

Installation
============

Dependencies
------------
 * [Django][1]
 * [lxml][2]

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
* [Tim Julien][3]
* [Anthony Roscoe][4]
* [Felix Berger][5]

[1]: http://www.djangoproject.com
[2]: http://codespeak.net/lxml
[3]: http://github.com/tjulien
[4]: http://github.com/aroscoe
[5]: http://github.com/fberger
