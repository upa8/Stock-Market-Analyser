# import random
# import os, os.path
# import argparse

# import cherrypy

# from cherrypy.lib.static import serve_file

# from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
# from ws4py.websocket import WebSocket
# from ws4py.messaging import TextMessage


# class ChatWebSocketHandler(WebSocket):
#     def received_message(self, m):
#         print "Recieved  a message "
#         print m
#         cherrypy.engine.publish('websocket-broadcast', m)

#     def closed(self, code, reason="A client left the room without a proper explanation."):
        
#         cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))


# class StockMarketAnalyser(object):
#     @cherrypy.expose
#     def index(self):
#         pass

#     @cherrypy.expose
#     def ws(self):
#         cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))


# if __name__ == '__main__':
     
#      import logging
#      from ws4py import configure_logger
#      configure_logger(level=logging.DEBUG)

#      parser = argparse.ArgumentParser(description='Echo CherryPy Server')
#      parser.add_argument('--host', default='127.0.0.1')
#      parser.add_argument('-p', '--port', default=9000, type=int)
#      parser.add_argument('--ssl', action='store_true')
#      args = parser.parse_args()

#      cherrypy.config.update({'server.socket_host': args.host,
#                             'server.socket_port': args.port
#                             })

    

#      root = os.path.dirname(os.path.abspath(__file__))
#      WebSocketPlugin(cherrypy.engine).subscribe()
#      cherrypy.tools.websocket = WebSocketTool()
#      conf = {
#          '/': {
#              'tools.staticdir.on': True,
#              'tools.staticdir.dir': root + '/public/',
#              'tools.staticdir.index': root + '/public/index.html',
#              'tools.websocket.handler_cls': ChatWebSocketHandler
#          },
#          '/ws': {
#               'tools.websocket.on': True,
#               'tools.websocket.handler_cls': ChatWebSocketHandler
#         },
#      }
     
#      webapp = StockMarketAnalyser()
     
#      cherrypy.quickstart(webapp,'/',conf)
# 		

# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
import argparse
import random
import os

import cherrypy

from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage

class ChatWebSocketHandler(WebSocket):
    def received_message(self, m):
        cherrypy.engine.publish('websocket-broadcast', m)

    def closed(self, code, reason="A client left the room without a proper explanation."):
        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))

class Root(object):
    def __init__(self, host, port, ssl=False):
        self.host = host
        self.port = port
        self.scheme = 'wss' if ssl else 'ws'

    @cherrypy.expose
    def index(self):
        return """<html>
    <head>
      <script type='application/javascript' src='https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js'></script>
      <script type='application/javascript'>
        $(document).ready(function() {

         websocket = '%(scheme)s://%(host)s:%(port)s/ws';
         //websocket = "ws://echo.websocket.org";
          //  websocket = "ws://54.242.218.128:9000/ws"
        if (window.WebSocket) {
            ws = new WebSocket(websocket);
          }
          else if (window.MozWebSocket) {
            ws = MozWebSocket(websocket);
          }
          else {
            console.log('WebSocket Not Supported');
            return;
          }

          window.onbeforeunload = function(e) {
            $('#chat').val($('#chat').val() + 'Bye bye...\\n');
            ws.close(1000, '%(username)s left the room');

            if(!e) e = window.event;
            e.stopPropagation();
            e.preventDefault();
          };
          ws.onmessage = function (evt) {
             $('#chat').val($('#chat').val() + evt.data + '\\n');
          };
          ws.onopen = function() {
             ws.send("%(username)s entered the room");
          };
          ws.onclose = function(evt) {
             $('#chat').val($('#chat').val() + 'Connection closed by server: ' + evt.code + ' \"' + evt.reason + '\"\\n');
          };

          $('#send').click(function() {
             console.log($('#message').val());
             ws.send('%(username)s: ' + $('#message').val());
             $('#message').val("");
             return false;
          });
        });
      </script>
    </head>
    <body>
    <form action='#' id='chatform' method='get'>
      <textarea id='chat' cols='35' rows='10'></textarea>
      <br />
      <label for='message'>%(username)s: </label><input type='text' id='message' />
      <input id='send' type='submit' value='Send' />
      </form>
    </body>
    </html>
    """ % {'username': "User%d" % random.randint(0, 100), 'host': self.host, 'port': self.port, 'scheme': self.scheme}

    @cherrypy.expose
    def ws(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))

if __name__ == '__main__':
    import logging
    from ws4py import configure_logger
    configure_logger(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Echo CherryPy Server')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('-p', '--port', default=9000, type=int)
    parser.add_argument('--ssl', action='store_true')
    args = parser.parse_args()

    cherrypy.config.update({'server.socket_host': args.host,
                            'server.socket_port': args.port,
                            'tools.staticdir.root': os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))})

    if args.ssl:
        cherrypy.config.update({'server.ssl_certificate': './server.crt',
                                'server.ssl_private_key': './server.key'})

    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.quickstart(Root(args.host, args.port, args.ssl), '', config={
        '/ws': {
            'tools.websocket.on': True,
            'tools.websocket.handler_cls': ChatWebSocketHandler
            },
        '/js': {
              'tools.staticdir.on': True,
              'tools.staticdir.dir': 'js'
            }
        }
    )

