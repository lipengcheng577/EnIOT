# -*- coding: utf-8 -*-
import json
import http.client
import http.server

from urllib.parse import urlparse

class RequestHandler(http.server.BaseHTTPRequestHandler):
    '''处理请求并返回页面'''

    # 处理一个GET请求
    def do_GET(self):
         # 页面模板
        Page = '''\
            <html>
            <body>
            <p>Hello, web!</p>
            </body>
            </html>
        '''

        querypath = urlparse(self.path)
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(Page)))
        self.end_headers()
        self.wfile.write(Page)