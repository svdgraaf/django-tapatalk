from util import *
import xmlrpclib
from django.db.models import Q


def get_config(request):
    return {
        'sys_version': '4.2.0',
        'is_open': True,
        'guest_okay': True,
        'push': '0',
        'api_level': '3',  # level 3 for now
        'reg_url': '/',
        # 'version': 'vb40_4.5.1',
        'version': 'pb30_3.8.1',
        'hide_forum_id': '',
        'forum_signature': '0',
        'support_md5': '0',
        'allow_moderate': '0',
        'disable_bbcode': '0',
        'report_post': '0',
        'report_pm': '0',
        'goto_unread': '0',
        'goto_post': '1',
        'mark_read': '1',
        'mark_forum': '1',
        'no_refresh_on_post': '0',
        'subscribe_forum': '0',
        'disable_subscribe_forum': '1',
        'get_latest_topic': '1',
        'get_id_by_url':'0',
        'delete_reason': '1',
        'mod_approve': '0',
        'mod_delete': '0',
        'anonymous': '1',
        'pm_load': '0',
        'subscribe_load': '0',
        'subscribe_topic_mode': '0',
        'mass_subscribe': '0',
        'emoji': '1',
        'searchid': '1',
        'avatar': '1',
        'multi_quote': '1',
        'inbox_stat': '0',
        'user_id': '1',
        'get_forum': '1',
        'get_forum_status': '1',
        'get_topic_status': '1',
        'get_participated_forum': '0',
        'get_smilies': '0',
        'get_online_users': '0',
        'mark_topic_read': '1',
        'mark_pm_unread': '0',
        'advanced_search': '0',
        'alert': '0',
        'push_type': 'quote',
        'min_search_length': '3',
        # 'charset': 'utf-8',
        'advanced_delete': '0',
    }


def get_forum(request, return_description=False, forum_id=''):
    # if request.user.is_authenticated():
    # user_groups = request.user.groups.all()
    # else:
    user_groups = []

    categories = Category.objects.all().filter(
            Q(groups__in=user_groups) | \
            Q(groups__isnull=True))

    # this will hold the result
    data = []

    # loop through categories, and create result
    for category in categories:
        cat = {
            'forum_id': str(category.id),
            'forum_name': xmlrpclib.Binary(category.name),
            'parent_id': '-1',
            'sub_only': True,
            'child': [],
        }


        # add all child forums to category
        fora = Forum.objects.filter(parent_id=None, category_id=category.id).filter(
                    Q(category__groups__in=user_groups) | \
                    Q(category__groups__isnull=True))

        for forum in fora:
            f = {
                'forum_id': str(forum.id),
                'forum_name': xmlrpclib.Binary(forum.name),
                'parent_id': str(category.id),
                'sub_only': False,
                'child': [],
                'can_post': True,
            }

            childs = Forum.objects.filter(parent_id=forum.pk).filter(
                    Q(category__groups__in=user_groups) | \
                    Q(category__groups__isnull=True))

            for child in childs:
                c = {
                    'forum_id': str(child.id),
                    'forum_name': xmlrpclib.Binary(child.name),
                    'parent_id': str(forum.id),
                    'sub_only': False,
                    'can_post': True,
                }

                f['child'].append(c)

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
