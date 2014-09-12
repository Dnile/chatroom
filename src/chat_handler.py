__author__ = 'danielby'
import tornado.web
import tornado.ioloop
import logging
import tornado.auth
import tornado.gen
import uuid
import base64

authenticated_user = dict()

from datetime import datetime

file = open('/tmp/data/chat_data.json', 'wb')


logging.basicConfig(level=logging.INFO)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        return tornado.escape.json_decode(user_json)


class AuthHandler(BaseHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        global authenticated_user
        if 'dnilekkb' not in str(user['email']):
                self.redirect('http://corp.everything.me/404.html')
                print "unauthorized user trying to access"

        self.set_secure_cookie("user", tornado.escape.json_encode(user))
        authenticated_user = user
        self.redirect('/Chat')


class ChatHandler(tornado.web.RequestHandler):


    def get(self):
        self.render('chatroom.html')






class MessagesHandler(tornado.web.RequestHandler):

    def get(self):
        self.handle_message(self.request)

    def handle_message(self, request):

        global authenticated_user

        response = dict()

        request_args = request.arguments

        try:
            request_key = request_args.keys()[0]
        except IndexError:
            pass

        response['message'] = request_key

        response['timestamp'] = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        response['name'] = authenticated_user['name']



        self.log_request(response)

        self.set_header('Access-Control-Allow-Origin', '*')


        self.write(response)

        logging.info(response)

        self.finish()



    def log_request(self, data):
        global file
        file.write(str(data))

if __name__=="__main__":


    application = tornado.web.Application([
        (r'/', AuthHandler),
        (r'/Chat', ChatHandler),
        (r'/Message', MessagesHandler),


    ],static_path='../static', login_url='/',debug=True,
          cookie_secret=base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes))
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()