from djangobb_forum.models import *
import base64


def as_tapatalk(self):
    data = {
        'forum_id': str(self.forum.id),
        'forum_name': self.forum.name,
        'topic_id': str(self.id),
        'topic_title': self.name,
        'prefix': '',
        'post_author_id': str(self.last_post.user.id),
        'post_author_name': self.last_post.user.username,
        'last_reply_author_name': self.last_post.user.username,
        'last_reply_author_id': self.last_post.user.id,
        'reply_number': self.post_count,
        'view_number': self.views,
        # 'can_subscribe': False,  # TODO: make me work
        # 'new_post': False,  # TODO: make me work
        # 'attachment': 0,
        # 'icon_url': '',
        # 'last_reply_time': self.last_post.created.isoformat(),
        # 'post_time': self.last_post.created.isoformat(),
        # 'time_string': self.last_post.created,

        # 'topic_author_id': self.user.id,
        # 'topic_author_name': self.user.username,
        # 'is_approved': True,
        # 'closed': self.closed,
    }
    return data

Topic.as_tapatalk = as_tapatalk
