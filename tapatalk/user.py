from django.contrib.auth import authenticate
import xmlrpclib
from util import *
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout


# See: http://tapatalk.com/api/api_section.php?id=2#login
def login(request, login_name=None, password=None, anonymous=False, push='1'):
    if login_name == None and password == None:
        return {
            'result': False,
        }

    # we have a username and password, let's try to login
    user = authenticate(username=str(login_name), password=str(password))

    if user is not None:
        # we only deal with active users
        if user.is_active:
            all_groups = user.groups.all()
            groups = []

            for group in groups:
                groups.append(group.id)

            auth_login(request, user)

            return {
                'result': True,
                'user_id': str(user.id),
                'username': xmlrpclib.Binary(user.username),
                'usergroup_id': groups,
                'post_count': user.forum_profile.post_count,
            }

    return {
        'result': False,
    }


# See: http://tapatalk.com/api/api_section.php?id=2#get_inbox_stat
def get_inbox_stat(request):
    topics = Topic.objects.all()
    try:
        last_read = PostTracking.objects.get(user=request.user).last_read
    except PostTracking.DoesNotExist:
        last_read = None
    try:
        topics = topics.filter(last_post__updated__gte=last_read).all()
    except:
        topics = []

    # TODO: check for django_messages
    from django_messages.models import Message
    box = Message.objects.inbox_for(request.user)
    unread = 0
    for msg in box:
        if msg.read_at == None:
            unread += 1

    return {
        'inbox_unread_count': unread,
        'subscribed_topic_unread_count': len(topics),
    }


# See: http://tapatalk.com/api/api_section.php?id=2#get_user_info
def get_user_info(request, username='', user_id=None):
    user = get_user(username)

    # try to get online status
    from django.core.cache import cache
    online = cache.get('djangobb_user%d' % user.id)
    if online == None:
        online = False

    avatar = get_avatar_for_user(user)

    # get the last post date
    last_post = ''
    try:
        last_post = user.forum_profile.last_post()
        # last_post = utc.localize(last_post)
    except:
        pass

    data = {
        'user_id': str(user.id),
        'username': xmlrpclib.Binary(user.username),
        'post_count': user.posts.count(),
        'reg_time': xmlrpclib.DateTime(user.date_joined.isoformat()),
        'last_activity_time': xmlrpclib.DateTime(last_post.isoformat()),
        'is_online': online,
        'accept_pm': True,
        'i_follow_u': False,
        'u_follow_me': False,
        'accept_follow': False,
        'following_count': 0,
        'follower': False,
        'display_text': '',
        'icon_url': avatar,
    }

    return data


# See: http://tapatalk.com/api/api_section.php?id=2#get_user_topic
def get_user_topic(request, username='', user_id=None):
    user = get_user(username)

    topics = user.topic_set.all()[:50]
    data = []
    for topic in topics:
        data.append(topic.as_tapatalk())
    return data


# See: http://tapatalk.com/api/api_section.php?id=2#get_user_reply_post
def get_user_reply_post(request, username='', user_id=None):
    user = get_user(username)

    posts = user.posts.all()
    data = []
    for post in posts:
        data.append(post.as_tapatalk())

    return data
