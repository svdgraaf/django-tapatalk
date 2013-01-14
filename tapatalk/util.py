from djangobb_forum.models import *
import base64


def as_tapatalk(self):
    data = {
        'forum_id': self.forum.id,
        'forum_name': self.forum.name,
        'topic_id': self.id,
        'post_author_name': self.last_post.user.username,
        'last_reply_author_name': self.last_post.user.username,
        'last_reply_author_id': self.last_post.user.id,
        'post_author_id': self.last_post.user.id,
        'can_subscribe': False,  # TODO: make me work
        'icon_url': '',
        'post_time': self.last_post.created.isoformat(),
        'new_post': False,  # TODO: make me work
        'topic_title': self.name,
        'topic_author_id': self.user.id,
        'topic_author_name': self.user.username,
        'last_reply_time': self.last_post.created.isoformat(),
        'post_time': self.last_post.created.isoformat(),
        'time_string': self.last_post.created,
        'is_approved': True,
        'reply_number': self.post_count,
        'view_number': self.views,
        'closed': self.closed,
        'short_content': 'Foobar',
    }
    return data

Topic.as_tapatalk = as_tapatalk
