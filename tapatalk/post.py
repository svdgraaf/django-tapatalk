from djangobb_forum.models import *

def get_thread(request, topic_id, start_num, last_num, return_html=True):
    topic = Topic.objects.get(pk=topic_id)
    print topic

    data = {
        'total_post_num': topic.post_count,
        'forum_id': str(topic.forum.id),
        'forum_title': topic.forum.name,
        'topic_id': str(topic.id),
        'topic_title': topic.name,
        'can_reply': True,
        'posts': [],
        'is_approved': True,
        'can_upload': True,
        'prefix': '',
        'can_subscribe': False,
        # 'is_closed': False,
        # 'position': 0,
    }

    posts = Post.objects.filter(topic=topic)
    for post in posts:
        p = {
            'post_id': str(post.id),
            'post_title': '',
            'post_content': post.body,
            'post_author_id': str(post.user.id),
            'post_author_name': post.user.username,
            'post_time': post.created.isoformat(),
            'is_approved': True,

        }

        # TODO: make me work
        # if post.user.id == user.id:
        #     p['can_edit'] = True

        data['posts'].append(p)

    return data
