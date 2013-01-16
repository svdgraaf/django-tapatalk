from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import base64

def login(login_name=None, password=None, anonymous=False, push='1'):
    if login_name == None and password == None:
        return {
            'result': False,
        }

    # login_name = base64.b64decode(login_name)
    # password = base64.b64decode(password)

    # we have a username and password, let's try to login
    user = authenticate(username=login_name, password=password)
    user = User.objects.get(pk=1)

    if user is not None:
        # we only deal with active users
        if user.is_active:
            all_groups = user.groups.all()
            groups = []

            for group in groups:
                groups.append(group.id)

            return {
                'result': True,
                'user_id': user.id,
                'username': user.username,
                'usergroup_id': groups,
                'post_count': user.forum_profile.post_count,
            }

    return {
        'result': False,
    }


def get_inbox_stat(pm_last_checked_time=None, subscribed_topic_last_checked_time=None):
    return {
        'inbox_unread_count': 0,
        'subscribed_topic_unread_count': 0,
    }
