__author__ = 'danielby'
import tornado.web
import tornado.ioloop
import logging
from datetime import datetime

file = open('/Users/danielby/Desktop/chat_data.json', 'wb')


logging.basicConfig(level=logging.INFO)

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

        response['timestamp'] = datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")



        self.log_request(response)

        self.set_header('Access-Control-Allow-Origin', '*')


        self.write(response)

        logging.info(response)

        self.finish()



    def log_request(self, data):
        global file
        #file.write(data)

if __name__=="__main__":


    application = tornado.web.Application([
        (r'/', ChatHandler),
        (r'/Message', MessagesHandler),


    ],static_path='../static', debug=True)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()