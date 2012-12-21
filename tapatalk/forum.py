def get_config():
    return {
        'version': 'dev',
        'api_level': '3',
        'is_open': True,
        'guest_okay': True,
        'inbox_stat': '0',  # forum.inbox_stat
        'can_unread': '0',
        'get_latest_topic': '1',
    }


def get_forum(return_description=False, forum_id=''):
    return [{
            'forum_id': '1',
            'forum_name': 'Je moeder!',
            'parent_id': '-1',
            'sub_only': False,
        },
    ]
