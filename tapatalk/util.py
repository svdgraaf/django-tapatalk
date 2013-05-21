from djangobb_forum.models import *
from django.core.cache import cache
from django_messages.models import Message
import xmlrpclib
from django.contrib.auth.models import User


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
    avatar = get_avatar_for_user(self.user)

    data = {
        'forum_id': str(self.forum.id),
        'forum_name': xmlrpclib.Binary(self.forum.name),
        'topic_id': str(self.id),
        'topic_title': xmlrpclib.Binary(self.name),
        'prefix': '',
        'icon_url': avatar,
        'reply_number': self.post_count,
        'view_number': self.views,
        'can_post': True,
        'is_approved': True,
        'topic_author_id': self.user.id,
        'topic_author_name': xmlrpclib.Binary(self.user.username),
        'closed': self.closed,
    }
    if self.last_post:
        data.update({
            'short_content': xmlrpclib.Binary(self.last_post.body),
            'last_reply_time': xmlrpclib.DateTime(self.last_post.created.isoformat()),
            'post_time': xmlrpclib.DateTime(self.last_post.created.isoformat()),
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

    data = {
        'post_id': str(self.id),
        'post_title': xmlrpclib.Binary(''),
        'post_content': self.body,
        'forum_name': xmlrpclib.Binary(self.topic.forum.name),
        'forum_id': self.topic.forum.id,
        'topic_id': self.topic.id,
        'topic_title': xmlrpclib.Binary(self.topic.name),
        'post_author_id': str(self.user.id),
        'post_author_name': xmlrpclib.Binary(self.user.username),
        'post_time': xmlrpclib.DateTime(self.created.isoformat()),
        'is_approved': True,
        'icon_url': avatar,
        'is_online': online,
        'reply_number': self.topic.post_count,
        'view_count': self.topic.views,
        'short_content': xmlrpclib.Binary(self.body),
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
        'msg_id': self.id,
        'msg_state': state,
        'sent_date': xmlrpclib.DateTime(self.sent_at),
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
