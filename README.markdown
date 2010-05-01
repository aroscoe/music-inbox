Music Inbox
===========

Music Inbox is a service that gives you access to information about your music library through a REST interface. 

Installation
============

Dependencies
------------
 * [Django][1]
 * [lxml][2]
 * [celery][6]

These can be pip installed using the REQUIREMENTS file.

 * [RabbitMQ][7]

We recommend using a package management tool to install RabbitMQ.
    

Setup
-----

    $ git clone git://github.com/aroscoe/music-inbox.git
    $ cd music-inbox/
    music-inbox $ git submodule update --init
    music-inbox $ pip install -r REQUIREMENTS
    music-inbox $ sudo rabbitmqctl add_user musicinbox musicinbox
    music-inbox $ sudo rabbitmqctl add_vhost musicinbox
    music-inbox $ sudo rabbitmqctl set_permissions -p musicinbox musicinbox "" ".*" ".*"
    mysql> create database musicinbox default character set utf8;
    music-inbox $ ./manage.py syncdb
    music-inbox $ ./manage.py celeryd -B
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
[6]: http://github.com/ask/celery
[7]: http://www.rabbitmq.com