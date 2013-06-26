from djangobb_forum.models import *
import xmlrpclib

def get_thread(request, topic_id, start_num, last_num, return_html=True):
    topic = Topic.objects.get(pk=topic_id)

    if request.user.is_authenticated():
        topic.update_read(request.user)

    data = {
        'total_post_num': topic.post_count,
        'forum_id': str(topic.forum.id),
        'forum_title': xmlrpclib.Binary(topic.forum.name),
        'topic_id': str(topic.id),
        'topic_title': xmlrpclib.Binary(topic.name),
        'can_reply': True,
        'posts': [],
        'is_approved': True,
        'can_upload': True,
        'prefix': '',
        'can_subscribe': False,
        'is_closed': topic.closed,
    }

    posts = Post.objects.filter(topic=topic)

    if start_num != 0 or last_num != 0:
        posts = posts[start_num:last_num]

    for post in posts:
        p = post.as_tapatalk()

        # TODO: make me work
        if post.user.id == request.user.id:
            p['can_edit'] = True

        data['posts'].append(p)

    return data


def reply_post(request, forum_id, topic_id, subject='', text_body='', attachments=[], group_id='', return_html=False):
    p = Post()
    t = Topic.objects.get(pk=topic_id)
    if t.closed:
        return {
            'result': False,
            'post_id': str(p.id),
        }

    p.user_id = request.user.id
    p.body = str(text_body)
    p.topic = t
    p.save()

    return {
        'result': True,
        'post_id': str(p.id),
    }


def get_raw_post(request, post_id):
    p = Post.objects.get(pk=post_id)

    return p.as_tapatalk()


def save_raw_post(request, post_id, post_title='', post_content='', return_html=False, prefix_id=''):
    p = Post.objects.get(pk=post_id, user=request.user)
    p.post_content = post_content
    p.save()

    return {
        'result': True,
    }
