
import SimpleHTTPServer
import SocketServer

PORT = 8000

class MyHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  def end_headers(self):
    self.send_my_headers()
    SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)
  
  def send_my_headers(self):
    self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
    self.send_header("Pragma", "no-cache")
    self.send_header("Expires", "0")


httpd = SocketServer.TCPServer(("", PORT), MyHTTPRequestHandler)

print "serving at port", PORT
httpd.serve_forever()
