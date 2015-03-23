
import http.server
import http.server

"""
class MyHttpServerRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

  def end_headers(self):
    self.send_my_headers()
    SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

  def send_my_headers(self):
    self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
    self.send_header("Pragma", "no-cache")
    self.send_header("Expires", "0")
"""

class MyHttpServerRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.end_headers()
        self.wfile.write('<html><head></head><body><a href="javascript: self.close()">Requerimiento procesado correctamente</a><body></html>');
