import xmlrpclib
from util import *


def get_unread_topic(request, start_num, last_num, search_id='', filters=[]):
    return {
        'result': True,
        'total_topic_num': 0,
        'topics': [],
        'forum_id': '',
    }


def get_latest_topic(request, start_num, last_num, search_id='', filters=[]):
    topics = Topic.objects.all()

    if start_num != 0 or last_num != 0:
        topics = topics[start_num:last_num]

    data = {
        'result': True,
        'topics': [],
    }

    for t in topics:
        data['topics'].append(t.as_tapatalk())

    data['total_topic_num'] = len(data['topics'])
    data['total_unread_num'] = 0
    return data


# TODO: Pagination
def get_participated_topic(request, user_name='', start_num=0, last_num=None, search_id='', user_id=''):
    user = request.user
    posts = Post.objects.filter(user=user)

    topics = []
    tmp = []
    for post in posts:
        if post.topic.id not in tmp:
                tmp.append(post.topic_id)

    topics = Topic.objects.filter(pk__in=tmp)

    if start_num != 0 or last_num != 0:
        topics = topics[start_num:last_num]

    topic_set = []
    for topic in topics:
        topic_set.append(topic.as_tapatalk())

    data = {
        'result': True,
        'search_id': search_id,
        'total_topic_num': len(topics),
        'total_unread_num': 0,  # TODO: make me work
        'topics': topic_set,
    }
    print data
    return data


def get_topic(request, forum_id, start_num=0, last_num=0, mode='DATE'):
    topics = Topic.objects.filter(forum_id=forum_id)
    forum = Forum.objects.get(pk=forum_id)

    if mode == 'TOP':
        topics = topics.filter(sticky=True)

    if start_num != 0 or last_num != 0:
        topics = topics[start_num:last_num]

    data = {
        'total_topic_num': forum.topic_count,
        'forum_id': str(forum_id),
        'forum_name': xmlrpclib.Binary(forum.name),
        'can_post': True,
        'can_upload': False,
        'require_prefix': False,
        'topics': [],
    }

    subscriptions = []
    if request.user.is_authenticated():
        subscriptions = request.user.subscriptions.all()

    for topic in topics:
        t = topic.as_tapatalk()
        if request.user.is_authenticated():
            t['can_subscribe'] = True
            if topic in subscriptions:
                t['is_subscribed'] = True

        data['topics'].append(t)

    return data


def new_topic(request, forum_id, subject, text_body, prefix_id='', attachment_id_array=[], group_id=''):
    from djangobb_forum.models import Topic, Post
    t = Topic()
    t.forum_id = int(forum_id)
    t.name = str(subject)
    t.user_id = request.user.pk
    t.save()

    p = Post()
    p.user_id = request.user.pk
    p.topic_id = t.id
    p.body = str(text_body)
    p.save()

    return {
        'result': True,
        'topic_id': t.id,
    }
