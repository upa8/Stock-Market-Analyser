import os.path

import cherrypy


class HelloWorld:
    @cherrypy.expose
    def index(self):
        return 'Hello world!'


tutconf = os.path.join(os.path.dirname(__file__), 'tutorial.conf')

if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld(), config=tutconf)
