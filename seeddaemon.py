#coding=utf-8
"""SeedDaemon -- Daemon program for SEED storage, 
client, name server and data server all-in-one. """
import os

import tornado.web
import tornado.template
import tornado.ioloop
import tornado.httpserver

class IndexHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ['GET']

    def get(self, path):
        """ GET method to list contents of directory or
        write index page if index.html exists."""

        # remove heading slash
        path = path[1:]

        for index in ['index.html', 'index.htm']:
            index = os.path.join(path, index)
            if os.path.exists(index):
                with open(index, 'rb') as f:
                    self.write(f.read())
                    self.finish()
                    return
        html = self.generate_index(path)
        self.write(html)
        self.finish()

    def generate_index(self, path):
        """ generate index html page, list all files and dirs."""
        if path:
            files = os.listdir(path)
        else:
            files = os.listdir(os.curdir)
        files = [filename + '/'
                if os.path.isdir(os.path.join(path, filename))
                else filename
                for filename in files]
        html_template = """
            <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html>
            <title>Directory listing for /{{ path }}</title>
            <body>
            <h2>Directory listing for /{{ path }}</h2>
            <hr>
            <ul>
            {% for filename in files %}
            <li><a href="{{ filename }}">{{ filename }}</a>
            {% end %}
            </ul>
            <hr>
            </body>
            </html>
            """
        t = tornado.template.Template(html_template)
        return t.generate(files=files, path=path)

class SeedDaemon(object):
    """SeedDaemon"""
    def __init__(self, daemonport):
        super(SeedDaemon, self).__init__()
        self.port = daemonport

    def run(self):
        """run server loop"""
        current_path = os.getcwd()
        application = tornado.web.Application([
            (r'(.*)/$', IndexHandler,),
            (r'/(.*)$', tornado.web.StaticFileHandler, {'path': current_path}),
            ])

        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(self.port)

        print 'Serving HTTP on 0.0.0.0 port %d ...' % self.port
        tornado.ioloop.IOLoop.instance().start()
