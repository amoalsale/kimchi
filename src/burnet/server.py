#
# Project Burnet
#
# Copyright IBM, Corp. 2013
#
# Authors:
#  Anthony Liguori <aliguori@us.ibm.com>
#  Adam Litke <agl@linux.vnet.ibm.com>
#
# All Rights Reserved.
#

from argparse import ArgumentParser
from root import Root
import mockmodel
import config
import cherrypy

def set_no_cache():
    from time import strftime, gmtime
    h = [('Expires', 'Mon, 26 Jul 1997 05:00:00 GMT'),
         ('Cache-Control', 
          'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'),
         ('Pragma', 'no-cache'),
         ('Last-Modified', strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()))]
    hList = cherrypy.response.header_list
    if isinstance(hList, list):
        hList.extend(h)
    else:
        hList = h

class Server(object):
    CONFIG = {
        '/': { 'tools.trailing_slash.on': False,
               'tools.staticdir.root': config.get_prefix(),
               'request.methods_with_bodies': ('POST', 'PUT'),
               'tools.nocache.on': True },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'css',
            'tools.nocache.on': False },
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'js',
            'tools.nocache.on': False },
        '/images': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'images',
            'tools.nocache.on': False },
        }

    def __init__(self, args):
        cherrypy.tools.nocache = cherrypy.Tool('on_end_resource', set_no_cache)
        cherrypy.server.socket_host = args.host
        cherrypy.server.socket_port = args.port

        if hasattr(args, 'model'):
            model = args.model
        elif args.test:
            model = mockmodel.get_mock_environment()
        else:
            # All we have is MockModel so far :(
            model = mockmodel.MockModel()

        self.app = cherrypy.tree.mount(Root(model), config=self.CONFIG)

    def start(self):
        cherrypy.quickstart(self.app)

    def stop(self):
        cherrypy.engine.exit()

def main(args):
    parser = ArgumentParser()
    parser.add_argument('--host', type=str, default="localhost",
                        help="Hostname to listen on")
    parser.add_argument('--port', type=int, default=8000,
                        help="Port to listen on")
    parser.add_argument('--test', action='store_true',
                        help="Run server in testing mode")

    args = parser.parse_args(args)
    srv = Server(args)
    srv.start()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv[1:]))