from util import *
import xmlrpclib
from django.db.models import Q


def get_config(request):
    return {
        'version': 'vb40_3.9.4',
        'api_level': '3',  # level 3 for now
        'is_open': True,
        'guest_okay': True,
        'inbox_stat': True,  # forum.inbox_stat
        'can_unread': False,
        'get_latest_topic': True,
        'sys_version': '4.2.0',
        'anonymous': True,
        'goto_unread': True,
        'subscribe_forum': False,
        'disable_subscribe_forum': True,
        'get_id_by_url': False,
        'anonymous': True,
        'reg_url': 'register.php',
        'forum_signature': False,
        'get_forum': True,
        'get_participated_forum': True,
        'user_id': True,
        'disable_bbcode': False,
        'get_topic_status': True,
        'get_forum_status': True,
        'report_post': True,
        'disable_bbcode': False,
        'conversation': '0',
        'mark_pm_unread': '0',
        # 'forum_signature': True,
        # 'allow_moderate': True,
        # 'subscribe_topic_mode': '0,1,2,3',
        # 'subscribe_forum_mode': '0,2,3',
    }


def get_forum(request, return_description=False, forum_id=''):
    if request.user.is_authenticated():
        user_groups = request.user.groups.all()
    else:
        user_groups = []

    categories = Category.objects.all().filter(
            Q(groups__in=user_groups) | \
            Q(groups__isnull=True))

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
                'can_post': True,
            }

            cat['child'].append(f)

        data.append(cat)
    return data


def get_online_users(request, page=0, perpage=20, id=None, area='forum'):
    users_cached = cache.get('djangobb_users_online', {})
    users_online = users_cached and User.objects.filter(id__in = users_cached.keys()) or []
    guests_cached = cache.get('djangobb_guests_online', {})

    data = {
        'member_count': len(users_cached),
        'guest_count': len(guests_cached),
        'list': [],
    }

    for user in users_online:
        avatar = get_avatar_for_user(user)
        u = {
            'user_id': user.id,
            'username': xmlrpclib.Binary(user.username),
            'user_name': xmlrpclib.Binary(user.username),
            'icon_url': avatar,
            'display_text': '',
        }
        data['list'].append(u)

    return data
