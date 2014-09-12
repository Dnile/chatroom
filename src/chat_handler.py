__author__ = 'danielby'
import tornado.web
import tornado.ioloop
import logging
import tornado.auth
import tornado.gen

from datetime import datetime

file = open('/tmp/data/chat_data.json', 'wb')


logging.basicConfig(level=logging.INFO)


class GoogleOAuth2LoginHandler(tornado.web.RequestHandler,
                               tornado.auth.GoogleOAuth2Mixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument('code', False):
            user = yield self.get_authenticated_user(
                redirect_uri='hhttp://ps366443.dreamhostps.com:8888/auth/google',
                code=self.get_argument('code'))
            # Save the user with e.g. set_secure_cookie
        else:
            yield self.authorize_redirect(
                redirect_uri='http://ps366443.dreamhostps.com:8888/auth/google',
                client_id=self.settings['google_oauth']['key'],
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})


class ChatHandler(tornado.web.RequestHandler):


    def get(self):
        self.render('chatroom.html')






class MessagesHandler(tornado.web.RequestHandler):

    def get(self):
        self.handle_message(self.request)

    def handle_message(self, request):

        response = dict()

        request_args = request.arguments

        try:
            request_key = request_args.keys()[0]
        except IndexError:
            pass

        response['message'] = request_key

        response['timestamp'] = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")



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
        (r'/', ChatHandler),
        (r'/Message', MessagesHandler),


    ],static_path='../static', debug=True)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()