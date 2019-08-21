#!/usr/bin/env python

import os
# 0 - debug
# 1 - info (still a LOT of outputs)
# 2 - warnings
# 3 - errors
os.environ['GLOG_minloglevel'] = '3' 

from nudenet import NudeDetector

from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler, HTTPServer

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

import numpy as np

import sys
import argparse
import glob
import time
from PIL import Image
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import json
from binascii import a2b_base64
import platform 
import urllib

def curtime():
    return int(round(time.time() * 1000))

def logTime(msg):
    global startTime
    diffTime = curtime() - startTime
    #print (msg + " done in " + str(diffTime))
    startTime = curtime()

def handleRequest(req):
    # length = int(req.headers.getheader('content-length')) #gets correct length of data
    # json_data = req.rfile.read(length) #gets json   {"image": "/9j/4AAQ...data"} or {"url":"https://img.antichat.me/thumb/be380ac64e6518b170c236072169ee65_photo.jpeg"}
    # logTime("reading file") #1500ms here!!

    # json_dict = json.loads(json_data)

    # binary_data = []

    # if 'image' in json_dict:
    #     image_data = json_dict['image']
    #     binary_data = a2b_base64(image_data)
    # elif 'url' in json_dict:
    #     image_url = json_dict['url']
    #     binary_data = urllib.urlopen(image_url).read()

    #logTime("preparing image")
    global detector
    result = detector.detect('/home/ubuntu/image/image_small.jpg')

    print ("result: " , result)

    req.send_response(200)
    req.send_header('Content-type', 'application/json')
    req.end_headers()

    req.wfile.write(result)


class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        global startTime
        startTime = curtime()
        handleRequest(self)
        return

port = int(os.environ['port'])
interface = '0.0.0.0'

if sys.argv[2:]:
    os.chdir(sys.argv[2])

global detector
detector = NudeDetector('/home/ubuntu/NudeNet/detector_model')

print('started python classification server on '+ str(port) + " with interpreter: " + platform.python_implementation())

server = ThreadingSimpleServer((interface, port), MyHandler)
try:
    while 1:
        sys.stdout.flush()
        server.handle_request()
except KeyboardInterrupt:
    print('Finished.')