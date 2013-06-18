import xmlrpclib
from util import *
from django.db.models import Q


def get_unread_topic(request, start_num, last_num, search_id='', filters=[]):
    data = {
        'result': True,
        'total_topic_num': 0,
        'topics': [],
        'forum_id': '',
    }

    groups = request.user.groups.all() or [] #removed after django > 1.2.3
    topics = Topic.objects.filter(
                   Q(forum__category__groups__in=groups) | \
                   Q(forum__category__groups__isnull=True))

    try:
        last_read = PostTracking.objects.get(user_id=request.user.pk).last_read
    except PostTracking.DoesNotExist:
        last_read = None
    if last_read:
        topics = topics.filter(Q(updated__gte=last_read) | Q(created__gte=last_read)).all()
    else:
        #searching more than forum_settings.SEARCH_PAGE_SIZE in this way - not good idea :]
        topics = [topic for topic in topics[:forum_settings.SEARCH_PAGE_SIZE * 5] if forum_extras.has_unreads(topic, request.user)]

    data['total_topic_num'] = len(topics)

    if start_num != 0 or last_num != 0:
        topics = topics[start_num:last_num]

    for topic in topics:
        data['topics'].append(topic.as_tapatalk())

    return data


def get_latest_topic(request, start_num=0, last_num=None, search_id='', filters=[]):

    data = {
        'result': True,
        'topics': [],
    }
    topics = Topic.objects.filter(forum__category__groups__isnull=True)
    data['total_topic_num'] = len(topics)

    if start_num != 0 or last_num != 0:
        topics = topics[start_num:last_num]

    for t in topics:
        data['topics'].append(t.as_tapatalk())

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

    topics = Topic.objects.filter(pk__in=tmp).filter(forum__category__groups__isnull=True)

    if start_num != 0 or last_num != 0:
        topics = topics[start_num:last_num]

    topic_set = []
    for topic in topics:
        topic_set.append(topic.as_tapatalk())

    data = {
        'result': True,
        'search_id': search_id,
        'total_topic_num': len(topics),
        'topics': topic_set,
    }
    print data
    return data


def get_topic(request, forum_id, start_num=0, last_num=0, mode='DATE'):
    topics = Topic.objects.filter(forum_id=forum_id).filter(forum__category__groups__isnull=True)
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
