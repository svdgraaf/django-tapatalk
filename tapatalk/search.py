from util import *
import xmlrpclib


def search_topic(request, search_string, start_num=0, last_num=None, search_id=''):
    t = Topic.objects.filter(name__icontains=search_string)
    topics = []
    for topic in t:
        topics.append(topic.as_tapatalk())

    return {
        'total_topic_num': len(topics),
        'topics': topics,
    }


def search_post(request, search_string, start_num=0, last_num=None, search_id=''):
    p = Post.objects.filter(body__icontains=search_string)
    posts = []
    for post in p:
        posts.append(post.as_tapatalk())

    return {
        'total_post_num': len(topics),
        'posts': topics,
    }

