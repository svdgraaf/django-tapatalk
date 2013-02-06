from util import *
from django_messages.models import Message
import datetime


def get_box_info(request):
    boxes = {
        'inbox': Message.objects.inbox_for(request.user),
        'sent': Message.objects.outbox_for(request.user),
        'trash': Message.objects.trash_for(request.user),
    }

    data = {
        'result': True,
        'list': [],
    }

    for name, box in boxes.items():

        unread = 0
        for msg in box:
            if msg.read_at == None:
                unread += 1

        item = {
            'box_id': name,
            'box_name': name,
            'msg_count': len(box),
            'unread_count': unread,
            'box_type': name.upper(),
        }
        data['list'].append(item)

    return data


# TODO: add pager
def get_box(request, box_id='', start_num=0, end_num=0):
    if box_id == 'inbox':
        box = Message.objects.inbox_for(request.user)
    if box_id == 'sent':
        box = Message.objects.outbox_for(request.user)
    else:
        box = Message.objects.inbox_for(request.user)

    unread = 0
    for msg in box:
        if msg.read_at == None:
            unread += 1

    data = {
        'result': True,
        'total_message_count': len(box),
        'total_unread_count': unread,
        'list': [],
    }

    for msg in box:
        m = msg.as_tapatalk()
        data['list'].append(m)

    return data


def get_message(request, message_id=None, box_id='', return_html=False):
    try:
        msg = Message.objects.get(recipient=request.user, pk=message_id)
    except:
        msg = Message.objects.get(sender=request.user, pk=message_id)
    now = datetime.datetime.now()
    msg.read_at = now
    msg.save()

    data = msg.as_tapatalk()
    data['result'] = True

    return data

def delete_message(request, message_id=None, box_id=''):
    try:
        msg = Message.objects.get(recipient=request.user, pk=message_id)
    except:
        msg = Message.objects.get(sender=request.user, pk=message_id)

    try:
        msg.delete()
        data = {
            'result': True
        }
    except:
        data = {
            'result': False
        }

    return data


def create_message(request, usernames=[], subject='', text_body='', action='', pm_id=''):
    recipients = []
    for username in usernames:
        recipients.append(get_user(username))

    for recipient in recipients:
        msg = Message()
        msg.recipient = recipient
        msg.sender = request.user
        msg.subject = subject
        msg.body = text_body
        if action == 'reply':
            msg.parent_msg_id = pm_id
        msg.save()

    return {
        'result': True,
        'msg_id': msg.id,
    }
