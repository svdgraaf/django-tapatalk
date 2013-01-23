from xmlrpclib import ServerProxy
from tests.transport import SessionTransport

HOST = 'http://androidworld.staging.hub.nl/forum/mobiquo/mobiquo.php'
USERNAME = 'tapatalk'
PASSWORD = 'foobar'

t = SessionTransport()
server = ServerProxy(HOST, verbose=True, transport=t)

print server.login(USERNAME, PASSWORD)
latest_topics = server.get_latest_topic(0,2)
topics = latest_topics['topics']
server.reply_post(topics[0]['forum_id'], topics[0]['topic_id'], 'subject', 'body')

