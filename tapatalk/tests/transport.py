from xmlrpclib import Transport
from xmlrpclib import *

# inspired from http://blog.godson.in/2010/09/how-to-make-python-xmlrpclib-client.html
# and updated for newer python versions


class SessionTransport(Transport):
    def __init__(self):
        Transport.__init__(self, use_datetime=0)
      
    #def request(self, r):pass
    session = ''
    def request(self, host, handler, request_body, verbose=0):
      
        # issue XML-RPC request

        h = self.make_connection(host)
        print h
        if verbose:
            h.set_debuglevel(1)

        self.send_request(h, handler, request_body)
        self.send_host(h, host)
        self.send_user_agent(h)
        self.send_content(h, request_body)

        response = h.getresponse()
        headers = response.getheaders()
        errcode = response.status
        errmsg = response.reason

        # check if we got any cookies, if so, set the session details
        cookies = response.getheader("Set-Cookie", None)
        if cookies:
            self.session = cookies.split(";")[0]
        print 'session: ', self.session

        if errcode != 200:
            raise ProtocolError(
                host + handler,
                errcode, errmsg,
                headers
                )

        self.verbose = verbose

        try:
            sock = h._conn.sock
        except AttributeError:
            sock = None

        return self.parse_response(response)

      
    def send_user_agent(self, connection):
        if self.session:          
            connection.putheader("Cookie", self.session)
        print self.session
        return Transport.send_user_agent(self, connection)
