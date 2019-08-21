#!/usr/bin/env python

import os
# 0 - debug
# 1 - info (still a LOT of outputs)
# 2 - warnings
# 3 - errors
os.environ['GLOG_minloglevel'] = '3' 

#from nudenet import NudeDetector

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

import keras
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color
import cv2
import tensorflow as tf

class Detector():
    detection_model = None
    session = None
    graph = None
    classes = [
        'BELLY',
        'BUTTOCKS',
        'F_BREAST',
        'F_GENITALIA',
        'M_GENETALIA',
        'M_BREAST',
    ]

    def __init__(self, model_path):
        self.session = tf.Session()
        self.graph = tf.get_default_graph()
        
        with self.graph.as_default():
            with self.session.as_default():
                self.detection_model = models.load_model(model_path, backbone_name='resnet101')

    def detect(self, img_path, min_prob=0.6):
        with self.graph.as_default():
            with self.session.as_default():
                image = read_image_bgr(img_path)
                image = preprocess_image(image)
                image, scale = resize_image(image)
                boxes, scores, labels = self.detection_model.predict_on_batch(np.expand_dims(image, axis=0))
                boxes /= scale
                processed_boxes = []
                for box, score, label in zip(boxes[0], scores[0], labels[0]):
                    if score < min_prob:
                        continue
                    box = box.astype(int).tolist()
                    label = Detector.classes[label]
                    processed_boxes.append({'box': box, 'score': score, 'label': label})

        return processed_boxes

def curtime():
    return int(round(time.time() * 1000))

def logTime(msg):
    global startTime
    diffTime = curtime() - startTime
    #print (msg + " done in " + str(diffTime))
    startTime = curtime()

def handleRequest(req):
    logTime("starting detection")
    global detector
    result = detector.detect('/home/ubuntu/image/porn.jpg')

    print ("result: " , result)

    req.send_response(200)
    req.send_header('Content-type', 'application/json')
    req.end_headers()

    logTime("detection done")

    req.wfile.write(str(result).encode())


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
#detector = NudeDetector('/home/ubuntu/NudeNet/detector_model')
detector = Detector('/home/ubuntu/NudeNet/detector_model')

print('started python classification server on '+ str(port) + " with interpreter: " + platform.python_implementation())

server = ThreadingSimpleServer((interface, port), MyHandler)
try:
    while 1:
        sys.stdout.flush()
        server.handle_request()
except KeyboardInterrupt:
    print('Finished.')