def get_unread_topic(start_num, last_num, search_id='', filters=[]):
    return {
        'result': True,
        'total_topic_num': 0,
        'search_id': search_id,
        'topics': [],
        'forum_id': '',
    }

def get_latest_topic(start_num, last_num, search_id='', filters=[]):
    return {
        'result': True,
        'total_topic_num': 1,
        'search_id': search_id,
        'topics': [
            {
                'forum_id': '1',
                'forum_name': 'foobar',
                'topic_id': '1',
                'topic_title': 'Je Moeder!',
                'post_author_name': 'Foobar',
                'post_author_id': '1',
                'can_subscribe': False,
            }
        ]
    }

def get_topic(forum_id, start_num=0, last_num=0, mode=''):
    return {
        'total_topic_num': 1,
        'forum_id': forum_id,
        'forum_name': 'Je Moeder!',
        'can_post': True,
        'require_prefix': False,
        'topics': [
            {
                'forum_id': forum_id,
                'topic_id': 1,
                'topic_title': 'Je moeder topic',
                'topic_author_id': 1,
                'topic_author_name': 'Je moeder',
            },
        ]
    }