import argparse,random,os,time,cherrypy,threading,redis,requests,urllib2,json

from datetime import datetime
from pytz import timezone
#from bs4 import BeautifulSoup
from threading import Thread
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage

#Stock parser
#Move to separate folder
###############################################################################

class StockParser:
    def __init__(self,url):
        self.hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
        self.url = url

    def getResults(self):
        req = urllib2.Request(self.url,headers=self.hdr)
        opener = urllib2.build_opener()
        f = opener.open(req)
        jsonData = json.loads(f.read())
        return jsonData


###############################################################################
class RedisResultSender(Thread):
    def __init__(self,threadName):
        Thread.__init__(self)
        self.DB = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.name = threadName
        self.count = 0
        url = "https://www.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json"
        self.StockParser = StockParser(url)
        #cherrypy.engine.publish('websocket-broadcast', "Thread instance created init method")

    def run(self):
        cherrypy.log("Thread started")
        #cherrypy.engine.publish('websocket-broadcast', "Thread run method")
        while True:
            if (self.DB.get('newData') == '1'):
                results = self.StockParser.getResults()
                latestData = json.dumps(results)
                self.DB.set('nifty50',latestData)
                self.DB.set('newData','0')
                cherrypy.engine.publish('websocket-broadcast', json.dumps(results))
                # CHECK WHETHER IT IS BETWEEN MONDAY TO FRIDAY
                #SLEEP TIME CODE CHECK 
                # lastResultTime = results['time']
                # cherrypy.log('Last result time '+ lastResultTime)
                # LastHours=latestData[13]+latestData[14]
                # LastMinutes=latestData[16]+latestData[17]
                # LastSeconds=latestData[19]+latestData[20]
                # console.log("Last hours "+ LastHours + "Last minutes "+ LastMinutes + " Last seconds "+ LastSeconds)
                # india = timezone('Asia/Kolkata')
                # currentTime = datetime.now(india).strftime('%H-%M-%S')
                # SLEEP FOR SAT AND SUNDAY MINUTES

                # pause for 2 and half minutes to update new data
                time.sleep(150) # CALCULATE THE TIME 
                self.DB.set('newData','1')
                

###############################################################################            
class ChatWebSocketHandler(WebSocket):
    def opened(self):
        #ack = "you are connected"
        #cherrypy.engine.publish('websocket-broadcast', ack)
        pass
    def received_message(self, m):
        pass
        #cherrypy.engine.publish('websocket-broadcast', "Thread started")

    def closed(self, code, reason="A client left the room without a proper explanation."):
        cherrypy.engine.publish('websocket-broadcast', "Closing the server")
        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))

###############################################################################

root = os.path.dirname(os.path.abspath(__file__))
def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "http://0.0.0.0:9000"

###############################################################################
class WS(object):
    @cherrypy.expose
    def ws(self):
        handler=cherrypy.request.ws_handler

# TODO: Put it in routes folder
class Static(object):
    @cherrypy.expose
    def index(self):
        pass

class Api(object):
    @cherrypy.expose
    def get_latest_data(self):
        cherrypy.log("Requested")
        DB = redis.StrictRedis(host='localhost', port=6379, db=0)
        results = DB.get('nifty50')
        cherrypy.log("Data "+ results)
        return results
###############################################################################


###############################################################################
# TODO : Add in config file and import from there 
wsConfig = {
            '/ws': {
                        'tools.websocket.on': True,
                        'tools.websocket.handler_cls': ChatWebSocketHandler,
                        'tools.log_headers.on': False,
                        'tools.log_tracebacks.on': False
                    }
            }

apiConfig = {
            '/get_latest_results': {
                        'tools.CORS.on': True
                    }
            }
# TODO : Add in config file and import from there 
staticConfig = {
                '/' :   {
                            'tools.staticdir.on': True,
                            'tools.staticdir.dir': root + '/public/',
                            'tools.staticdir.index': root + '/public/index.html',
                            'tools.log_headers.on': False,
                            'tools.log_tracebacks.on':False,
                            'tools.CORS.on': True
                        }
                }
 
###############################################################################


###############################################################################
#for CORS requests
cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS)

#Mounting static files directories
cherrypy.tree.mount(Static(),"/",staticConfig)

#Mounting the WebSocket Class with reqd conf
cherrypy.tree.mount(WS(),"/sock",wsConfig)

#Mount the api 
cherrypy.tree.mount(Api(),"/api",apiConfig)
###############################################################################

###############################################################################
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()
cherrypy.config.update({    'server.socket_host': "0.0.0.0",
                            'server.socket_port':9000})
###############################################################################
count = 1
###############################################################################
#Starting cherrypy server
cherrypy.engine.start()
###############################################################################
# Start redis thread 
redisThread = RedisResultSender(count)
redisThread.start()    
###############################################################################

cherrypy.engine.block()

