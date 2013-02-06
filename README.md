django-tapatalk
===============
Django tapatalk API implementation

Django tapatalk tries to implement all the v3 api calls for tapatalk. The default methods are for djangobb, but are easily extended to your own methods (see settings.py TAPATALK_METHODS for the mapping).

If anything, you can use the tests to test out your implementation of the api.

Requirements
============
Djangobb-forum, django-xmlrpc. It's recommended that you also use django-messages, if you want to use PM's out of the box (or provide your own implementation, see the settings section).

Settings
========
Via the TAPATALK_METHODS setting, you can provider your own methods instead of the default calls:

TAPATALK_METHODS = (
    ('myapp.get_config', 'get_config'),
    ('myapp.get_forum', 'get_forum'),
    ('myapp.search_topic', 'search_topic'),
    ('myapp.get_online_users', 'get_online_users'),
    # etc.
)


Acknowledgement
===============
I wish no one has to endure implementing the Tapatalk 'api' as I did, the documentation is bad. The Tapatalk app makes weird assumptions and will fall back to undocumented features whenever you do something wrong, without letting you know why, and how to fix the problem. This implementation is based upon reverse engineering of the protocol over Charles and looking at the php source code for some of the plugins...

So, I know I will never get those countless days back to my life, but let's hope I can save some of yours. If you have any questions, please let me know.


TODO
====
 - [ ] Lots
 - [ ] Moar tests