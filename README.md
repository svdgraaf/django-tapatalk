django-tapatalk
===============
Django tapatalk API implementation

Django tapatalk tries to implement all the v3 api calls for tapatalk. The default methods are for djangobb, but are easily extended to your own methods (see settings.py TAPATALK_METHODS for the mapping).

If anything, you can use the tests to test out your implementation of the api.

Acknowledgement
===============
I wish no one has to endure implementing the Tapatalk 'api' as I did, the documentation is bad. The Tapatalk app makes weird assumptions and will fall back to undocumented features whenever you do something wrong, without letting you know why, and how to fix the problem. This implementation is based upon reverse engineering of the protocol over Charles and looking at the php source code for some of the plugins...

So, I know I will never get those countless days back to my life, but let's hope I can save some of yours. If you have any questions, please let me know.


TODO
====
 - [ ] Lots
 - [ ] Moar tests