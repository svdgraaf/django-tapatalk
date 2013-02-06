from djangobb_forum.models import *
import xmlrpclib
import base64


def topic_as_tapatalk(self):
    data = {
        'forum_id': str(self.forum.id),
        'forum_name': xmlrpclib.Binary(self.forum.name),
        'topic_id': str(self.id),
        'topic_title': xmlrpclib.Binary(self.name),
        'prefix': '',
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
            'last_reply_time': xmlrpclib.DateTime(self.last_post.created),
            'post_time': xmlrpclib.DateTime(self.last_post.created),
            'time_string': self.last_post.created,
            'post_author_id': self.last_post.user.id,
            'post_author_name': xmlrpclib.Binary(self.last_post.user.username),
        })

    return data


def post_as_tapatalk(self):
    data = {
        'post_id': str(self.id),
        'post_title': xmlrpclib.Binary(''),
        'post_content': self.body,
        'post_author_id': str(self.user.id),
        'post_author_name': xmlrpclib.Binary(self.user.username),
        'post_time': xmlrpclib.DateTime(self.created),
        'is_approved': True,
        'icon_url': self.user.profile.get_avatar()
    }

    return data


# ugh, monkey patching
Topic.as_tapatalk = topic_as_tapatalk
Post.as_tapatalk = post_as_tapatalk
