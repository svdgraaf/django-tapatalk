from django.conf.urls import patterns, url

print 'foop'
urlpatterns = patterns('',
    url(r'^xmlrpc/$', 'tapatalk.views.handle_xmlrpc', name='xmlrpc'),
)
