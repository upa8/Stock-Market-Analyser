import random
import os, os.path

import cherrypy

from cherrypy.lib.static import serve_file

from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage

class StockMarketAnalyser(object):
    pass

if __name__ == '__main__':
     
     root = os.path.dirname(os.path.abspath(__file__))
     
     conf = {
         '/': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': root + '/public/',
             'tools.staticdir.index': root + '/public/index.html'
         }
     }
     
     webapp = StockMarketAnalyser()
     
     cherrypy.quickstart(webapp,'/',conf)
		