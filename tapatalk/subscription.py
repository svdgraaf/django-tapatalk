from util import *


def get_subscribed_topic(request, start_num=0, last_num=20):
    topics = request.user.subscriptions.all()

    data = {
        'total_topic_num': len(topics),
        'topics': []
    }

    for topic in topics:
        data['topics'].append(topic.as_tapatalk())

    return data
