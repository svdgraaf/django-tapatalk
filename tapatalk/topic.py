from util import *

def get_unread_topic(start_num, last_num, search_id='', filters=[]):
    return {
        'result': True,
        'total_topic_num': 0,
        'topics': [],
        'forum_id': '',
    }


def get_latest_topic(start_num, last_num, search_id='', filters=[]):
    topics = Topic.objects.all()[:2]
    data = {
        'result': True,
        'search_id': '1127401',
        'topics': [],
    }

    for topic in topics:
        data['topics'].append(topic.as_tapatalk())

    data['total_topic_num'] = len(data['topics'])
    data['total_unread_num'] = 0
    return data

# TODO: Pagination
def get_participated_topic(user_name='', start_num=0, last_num=None, search_id='', user_id=''):
    user = User.objects.get(username=user_name)
    posts = Post.objects.filter(user=user)

    topics = []
    tmp = []
    # for post in posts:
    #     if post.topic.id not in tmp:
    #         tmp.append(post.topic.id)
    #         data = {
    #             'forum_id': post.topic.forum.id,
    #             'forum_name': post.topic.forum.name,
    #             'topic_id': post.topic.id,
    #             'topic_title': post.topic.name,
    #             'post_author_id': post.user.id,
    #             'post_author_name': post.user.username,
    #             'post_time': post.created.isoformat() + '+01:00',
    #             'reply_number': post.topic.post_count,
    #             'new_post': False,  # TODO: make me work
    #             'view_number': post.topic.views,

    #         }

    return {
        'result': True,
        'search_id': search_id,
        'total_topic_num': len(topics),
        'total_unread_num': 0,  # TODO: make me work
        'topics': topics,
    }


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
