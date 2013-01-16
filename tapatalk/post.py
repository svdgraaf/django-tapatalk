from djangobb_forum.models import *

def get_thread(topic_id, start_num, last_num, return_html=True):
    topic = Topic.objects.get(pk=topic_id)
    print topic

    data = {
        'total_post_num': topic.post_count,
        'forum_id': str(topic.forum.id),
        'forum_name': topic.forum.name,
        'topic_id': str(topic.id),
        'topic_title': topic.name,
        'posts': [],
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
        }

        data['posts'].append(p)

    return data
