from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^xmlrpc/$', 'tapatalk.views.handle_xmlrpc', name='tapatalk-xmlrpc'),
)
