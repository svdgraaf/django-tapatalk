from djangobb_forum.models import *

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
    # get categories
    categories = Category.objects.all()

    # this will hold the result
    data = []

    # loop through categories, and create result
    for category in categories:
        cat = {
            'forum_id': category.id,
            'forum_name': category.name,
            'parent_id': '-1',
            'sub_only': True,
            'child': [],
        }

        # add all child forums to category
        fora = Forum.objects.filter(category=category)
        for forum in fora:
            f = {
                'forum_id': forum.id,
                'forum_name': forum.name,
                'parent_id': category.id,
                'sub_only': False,
                'child': [],
            }

            cat['child'].append(f)

        data.append(cat)
    return data
