===============
django-tapatalk
===============
Django tapatalk API implementation

Django tapatalk tries to implement all the v3 api calls for tapatalk. The default methods are for djangobb, but are easily extended to your own methods (see settings.py TAPATALK_METHODS for the mapping).

If anything, you can use the tests to test out your implementation of the api.

Requirements
============
[Djangobb-forum](http://djangobb.org/), [django-xmlrpc](http://pypi.python.org/pypi/django-xmlrpc). It's recommended that you also use [django-messages](http://code.google.com/p/django-messages/), if you want to use PM's out of the box (or provide your own implementation, see the 'settings' section).

Installation
============
The easiest way is via pip:

  $ pip install django-tapatalk

Or you could retrieve the source from github or pypy, and install it via the setup.py.

Usage
=====
Register **tapatalk** in your INSTALLED_APPS section of your project' settings, and add these urls to your installation:

    (r'^tapatalk/', include('tapatalk.urls')),
    (r'^forum/mobiquo/', include('tapatalk.urls')),

The 2nd line is optional, but that is the default directory Tapatalk will look for, so I recommend you add it.

Customization
=============
If you want to customize some methods, for instance, your login procedure, you define your own methods. Every method gets the request variable as first argument, and it's recommended that you use the standard request.user for referencing the current logged in user.

You can register extra methods or custom methods via the TAPATALK_METHODS variable:

  TAPATALK_METHODS = (
    ('my.awesome.login', 'login'),
    ('myapp.get_config', 'get_config'),
    ('myapp.get_forum', 'get_forum'),
    ('myapp.search_topic', 'search_topic'),
    ('myapp.get_online_users', 'get_online_users'),
    ('moar.awesomeness.ponies', 'ponies'),
    # etc.
  )


Features
========
- Login via standard Django/djangobb login
- Participated topics
- List all topics
- Read topic
- Create topic
- Reply to topic
- Edit post
- Forum listings
- Stickie listings
- Announcements
- Subscriptions (Post)
- Search (Post/Topic)
- Private Messages, inbox/sent
- Send, replying and reading of Private Messages
- Online users
- User profiles
- User posts, user topics

Missing:
- Mark all as read
- Pagination(!)
- Subscriptions (Forum) (djangobb doesn't support forum subscriptions afaik)
- The user avatars are not implemented correctly
- Moar tests

Help!
=====
Please help out by sending a pull request, or send me a github message


Acknowledgement
===============
I wish no one has to endure implementing the Tapatalk api as I did, the documentation is bad. The Tapatalk app makes weird assumptions and will fall back to undocumented features whenever you do something wrong, without letting you know why, or how to fix the problem. This implementation is based upon reverse engineering of the protocol over Charles and looking at the php source code for some of the plugins...

So, I know I will never get those countless hours back to my life, but let's hope I can save some of yours. If you have any questions, please let me know, as I will be glad to help. Also, be sure to checkout the tapatalk forums, as there are some nice and smart people there :)
