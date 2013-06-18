from djangobb_forum.models import *
from django.core.cache import cache
from django_messages.models import Message
from django.utils.encoding import smart_unicode
import xmlrpclib
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from .lib import html2markdown


def get_user(username):
    username = u"" + username.__str__()  # TODO: check this
    username = username.replace("\x00", '')  # ugh, something is messing up our strings

    # username = "" + str(username)
    user = User.objects.get(username=username)

    return user


def get_avatar_for_user(user):
    # fix this to correct call from django_bb
    avatar = None
    try:
        avatar = user.profile.get_avatar()
    except:
        pass

    if avatar == None:
        avatar = ''

    return avatar


def topic_as_tapatalk(self):
    try:
        user = self.user
    except:
        user = User.objects.get(username='archive')

    avatar = get_avatar_for_user(user)

    data = {
        'forum_id': str(self.forum.id),
        'forum_name': xmlrpclib.Binary(self.forum.name),
        'topic_id': str(self.id),
        'topic_title': xmlrpclib.Binary(smart_unicode(self.name)),
        'prefix': '',
        'icon_url': avatar,
        'reply_number': self.post_count,
        'view_number': str(self.views),
        'can_post': True,
        'is_approved': True,
        'topic_author_id': str(user.id),
        'topic_author_name': xmlrpclib.Binary(user.username),
        'closed': self.closed,
    }
    if self.last_post:
        body = html2markdown(smart_unicode(self.last_post.body_html))
        data.update({
            'short_content': xmlrpclib.Binary(body[:100]),
            'last_reply_time': xmlrpclib.DateTime(str(self.last_post.created.isoformat()).replace('-','') + '+01:00'),
            'post_time': xmlrpclib.DateTime(str(self.last_post.created.isoformat()).replace('-','') + '+01:00'),
            'post_author_id': self.last_post.user.id,
            'post_author_name': xmlrpclib.Binary(self.last_post.user.username),
        })

    return data


def post_as_tapatalk(self):
    avatar = get_avatar_for_user(self.user)

    # try to get online status
    online = cache.get('djangobb_user%d' % self.user.id)
    if online == None:
        online = False

    body = html2markdown(smart_unicode(self.body_html))

    data = {
        'post_id': str(self.id),
        'post_title': xmlrpclib.Binary(''),
        'post_content': xmlrpclib.Binary(body),
        'forum_name': xmlrpclib.Binary(self.topic.forum.name),
        'forum_id': str(self.topic.forum.id),
        'topic_id': str(self.topic.id),
        'topic_title': xmlrpclib.Binary(self.topic.name),
        'post_author_id': str(self.user.id),
        'post_author_name': xmlrpclib.Binary(self.user.username),
        'post_time': xmlrpclib.DateTime(str(self.created.isoformat().replace('-','') + '+01:00')),
        'is_approved': True,
        'icon_url': avatar,
        'is_online': online,
        'reply_number': str(self.topic.post_count),
        'view_count': str(self.topic.views),
        # 'short_content': xmlrpclib.Binary(self.body_html[:100]),
    }

    return data


def message_as_tapatalk(self):
    state = 'Unread'
    if self.read_at:
        state = 'Read'
    if self.replied_at:
        state = 'Replied'

    # try to get online status
    online = cache.get('djangobb_user%d' % self.sender.id)
    if online == None:
        online = False

    data = {
        'msg_id': str(self.id),
        'msg_state': state,
        'sent_date': xmlrpclib.DateTime(str(self.sent_at).replace('-','') + '+01:00'),
        'msg_from_id': self.sender.id,
        'msg_from': xmlrpclib.Binary(self.sender.username),
        'icon_url': get_avatar_for_user(self.sender),
        'msg_subject': xmlrpclib.Binary(self.subject),
        'short_content': xmlrpclib.Binary(self.body),
        'is_online': online,
        'text_body': xmlrpclib.Binary(self.body),
        'msg_to': [
            {
                'user_id': self.recipient.id,
                'username': xmlrpclib.Binary(self.recipient.username),
            }
        ],
    }

    return data

# ugh, monkey patching
Topic.as_tapatalk = topic_as_tapatalk
Post.as_tapatalk = post_as_tapatalk
Message.as_tapatalk = message_as_tapatalk
