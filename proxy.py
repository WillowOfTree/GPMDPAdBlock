# -*- coding: utf-8 -*-
import sys
import os
import socket
import ssl
import select
import threading
import re
import subprocess
import psutil
import time
import urllib2
from multiprocessing.dummy import Pool as ThreadPool
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
procNum = []
blhosts = []
for i in urllib2.urlopen("https://raw.githubusercontent.com/TheFauxFox/GPMDPAdBlock/master/blacklist").readlines():
  blhosts.append(i.strip("\n\r"))

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
  address_family = socket.AF_INET6
  daemon_threads = True

  def handle_error(self, request, client_address):
    cls, e = sys.exc_info()[:2]
    print cls
    print e
    if cls is socket.error or cls is ssl.SSLError:
      pass
    else:
      return HTTPServer.handle_error(self, request, client_address)

class ProxyRequestHandler(BaseHTTPRequestHandler):
  timeout = 20

  def __init__(self, *args, **kwargs):
    self.tls = threading.local()
    self.tls.conns = {}
    BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

  def log_error(self, format, *args):
    if isinstance(args[0], socket.timeout):
      return
    self.log_message(format, *args)

  def matchBL(self,url):
     return True

  def do_CONNECT(self):
    address = self.path.split(':', 1)
    address[1] = int(address[1]) or 443
    if address[0] in blhosts:
      self.send_response(404, 'Not Found')
      self.end_headers()
      self.close_connection = 1
      return
    try:
      s = socket.create_connection(address, timeout=self.timeout)
    except Exception as e:
      self.send_error(502)
      return
    self.send_response(200, 'Connection Established')
    self.end_headers()

    conns = [self.connection, s]
    self.close_connection = 0
    while not self.close_connection:
      rlist, wlist, xlist = select.select(conns, [], conns, self.timeout)
      if xlist or not rlist:
        break
      for r in rlist:
        other = conns[1] if r is conns[0] else conns[0]
        data = r.recv(8192)
        if not data:
          self.close_connection = 1
          break
        other.sendall(data)

def findPID(name):
  global procNum
  while True:
    procNum = [proc for proc in psutil.process_iter() if proc.name() == "Google Play Music Desktop Player.exe"]
    if len(procNum) < 1:
      print "Shutting Down..."
      httpd.server_close()
      break
    time.sleep(1)

if __name__ == '__main__':
  server_address = ('::1', 0)
  HandlerClass = ProxyRequestHandler
  HandlerClass.protocol_version = "HTTP/1.1"
  httpd = ThreadingHTTPServer(server_address, HandlerClass)
  sa = httpd.socket.getsockname()
  subprocess.call('C:\Users\%s\AppData\Local\GPMDP_3\Update.exe --processStart "Google Play Music Desktop Player.exe" --process-start-args "--proxy-server=localhost:%d"'%(os.path.expandvars("%USERNAME%"),int(sa[1])), creationflags=0x00000008)
  t = threading.Thread(target = findPID, args = ["Google Play Music Desktop Player.exe"])
  t.daemon = True
  t.start()
  while len(procNum) == 0:
    pass
  print "Serving HTTP Proxy on", sa[0], "port", sa[1]
  while len(procNum) > 0:
    httpd.handle_request()
