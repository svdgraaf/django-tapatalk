from djangobb_forum.models import *

def get_unread_topic(start_num, last_num, search_id='', filters=[]):
    return {
        'result': True,
        'total_topic_num': 0,
        'search_id': search_id,
        'topics': [],
        'forum_id': '',
    }


def get_latest_topic(start_num, last_num, search_id='', filters=[]):
    topics = Topic.objects.all()[:10]
    data = {
        'result': True,
        'total_topic_num': 1,
        'search_id': search_id,
        'topics': [],
    }

    for topic in topics:
        t = {
            'forum_id': topic.forum.id,
            'forum_name': topic.forum.name,
            'topic_id': topic.id,
            'topic_title': topic.name,
            'post_author_name': topic.last_post.user.username,
            'post_author_id': topic.last_post.user.id,
            'can_subscribe': False,
        }
        data['topics'].append(t)

    return data


def get_topic(forum_id, start_num=0, last_num=0, mode='DATE'):
    topics = Topic.objects.filter(forum_id=forum_id)
    forum = Forum.objects.get(pk=forum_id)

    if mode == 'TOP':
        topics = topics.filter(sticky=True)

    if start_num != 0:
        topics = topics[last_num:start_num]

    data = {
        'total_topic_num': forum.topic_count,
        'forum_id': forum_id,
        'forum_name': forum.name,
        'can_post': True,
        'require_prefix': False,
        'topics': [],
    }
    for topic in topics:
        t = {
            'forum_id': forum.id,
            'topic_id': topic.id,
            'topic_title': topic.name,
            'topic_author_id': topic.user.id,
            'topic_author_name': topic.user.username,
            'last_reply_time': topic.last_post.created.isoformat(),
            'reply_number': topic.post_count,
            'view_number': topic.views,
            'closed': topic.closed,

        }
        data['topics'].append(t)

    return data
