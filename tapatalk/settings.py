from django.conf import settings 

XMLRPC_DEFAULT_METHODS = (
    ('tapatalk.forum.get_config', 'get_config'),
    ('tapatalk.forum.get_forum', 'get_forum'),
    ('tapatalk.forum.search_topic', 'search_topic'),

    ('tapatalk.user.login', 'login'),
    ('tapatalk.user.get_inbox_stat', 'get_inbox_stat'),

    ('tapatalk.topic.get_unread_topic', 'get_unread_topic'),
    ('tapatalk.topic.get_participated_topic', 'get_participated_topic'),
    ('tapatalk.topic.get_latest_topic', 'get_latest_topic'),
    ('tapatalk.topic.get_topic', 'get_topic'),

    ('tapatalk.post.get_thread', 'get_thread'),
)

try:
    TAPATALK_METHODS = XMLRPC_DEFAULT_METHODS + settings.TAPATALK_METHODS
except:
    TAPATALK_METHODS = XMLRPC_DEFAULT_METHODS
