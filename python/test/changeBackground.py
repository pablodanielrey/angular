
import http.server
import socketserver

class MyHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write('ok'.encode('utf-8'))

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write('ok'.encode('utf-8'))

    def do_HEAD(self):
        self.send_error(code=403)

handler = MyHandler
httpd = socketserver.TCPServer(('',8282), handler)
httpd.serve_forever()

#import ctypes
#SPI_SETDESKWALLPAPER = 20
#ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, "image.jpg" , 0)
