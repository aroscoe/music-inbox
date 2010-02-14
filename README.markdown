Music Inbox
===========

Music Inbox is a service that gives you access to information about your music library through a REST interface. 

Installation
============

*You will need [Django][1] to run this application.*

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
* [Tim Julien][2]
* [Anthony Roscoe][3]
* [Felis Berger][4]
[1]: http://www.djangoproject.com
[2]: http://github.com/tjulien
[3]: http://github.com/aroscoe
[4]: http://github.com/fberger
