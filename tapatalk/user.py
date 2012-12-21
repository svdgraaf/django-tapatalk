def login(login_name, password, anonymous=False, push='1'):
    return {
        'result': True,
        'user_id': 1,
        'username': login_name,
        'usergroup_id': ['foo',],
        'icon_url': 'http://example.com/foobar.gif',
    }