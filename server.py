import argparse
import random
import os
import time
import cherrypy

from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage

class ChatWebSocketHandler(WebSocket):
    def opened(self):
        ack = "you are connected"
        cherrypy.engine.publish('websocket-broadcast', ack)
    def received_message(self, m):
        time.sleep(1)
        cherrypy.engine.publish('websocket-broadcast', m)
        time.sleep(1)
        cherrypy.engine.publish('websocket-broadcast', "Message send")
        time.sleep(1)
        cherrypy.engine.publish('websocket-broadcast', "New message send")

    def closed(self, code, reason="A client left the room without a proper explanation."):
        cherrypy.engine.publish('websocket-broadcast', "Closing the server")
        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))


class WS(object):
    @cherrypy.expose
    def ws(self):
        handler=cherrypy.request.ws_handler

class Static(object):
    @cherrypy.expose
    def index(self):
        pass

wsConfig = {
            '/ws': {
                        'tools.websocket.on': True,
                        'tools.websocket.handler_cls': ChatWebSocketHandler,
                        'tools.log_headers.on': False,
                        'tools.log_tracebacks.on': False
                    }
            }
root = os.path.dirname(os.path.abspath(__file__))

staticConfig = {
                '/' :   {
                            'tools.staticdir.on': True,
                            'tools.staticdir.dir': root + '/public/',
                            'tools.staticdir.index': root + '/public/index.html',
                            'tools.log_headers.on': False,
                            'tools.log_tracebacks.on':False
                        }

                }

#Mounting static files directories
cherrypy.tree.mount(Static(),"/",staticConfig)

#Mounting the WebSocket Class with reqd conf
cherrypy.tree.mount(WS(),"/sock",wsConfig)
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()
cherrypy.config.update({    'server.socket_host': "0.0.0.0",
                            'server.socket_port':9000})

#Starting cherrypy server
cherrypy.engine.start()
cherrypy.engine.block()


