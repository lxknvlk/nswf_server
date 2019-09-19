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

# print("sys path: " + str(sys.path))

import keras
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color
import cv2
import tensorflow as tf

import glob
import shutil
import os
import requests
from threading import Thread
import threading as th

class Detector():
    detection_model = None
    session = None
    graph = None
    model_path = ""
    classes = [
        'BELLY',
        'BUTTOCKS',
        'F_BREAST',
        'F_GENITALIA',
        'M_GENETALIA',
        'M_BREAST',
    ]

    def __init__(self, model_path):
        self.model_path = model_path
        self.reset_graph()
        self.reset_session()

    def reset_graph(self):
        tf.reset_default_graph()
        self.graph = tf.get_default_graph()

    def reset_session(self):
        if self.session is not None: self.session.close()
        config = tf.ConfigProto()
        config.gpu_options.allow_growth=True
        config.intra_op_parallelism_threads=1
        config.inter_op_parallelism_threads=1

        self.session = tf.Session(config=config)

        with self.graph.as_default():
            with self.session.as_default():
                self.detection_model = models.load_model(self.model_path, backbone_name='resnet101')

    def detect(self, img_path, min_prob=0.6):
        with self.graph.as_default():
            with self.session.as_default():
                logTime("reading img path")
                image = read_image_bgr(img_path)
                logTime("done reading im")
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

        self.reset_graph()
        # self.reset_session()

        return json.dumps(json.loads(str(processed_boxes).replace("\'", "\"")))

def curtime():
    return int(round(time.time() * 1000))

def logTime(msg):
    global startTime
    diffTime = curtime() - startTime
    #print (">>>>> logTime: " + msg + " done in " + str(diffTime))
    startTime = curtime()

def finish_request(req, res):
    req.send_response(200)
    req.send_header('Content-type', 'application/json')
    req.end_headers()
    req.wfile.write(res.encode())

def handleRequest(req):
    start = curtime()
    threads = th.active_count()

    if threads > 10: 
        finish_request(req, "")
        return

    logTime("=================starting processing")

    length = int(req.headers['Content-Length']) #gets correct length of data
    json_data = req.rfile.read(length) #gets json   {"image": "url"}
    json_dict = json.loads(json_data)

    logTime("got json")
    #print("got json:" + str(json_dict))
    #print("got json, type:" + str(type(json_dict)))

    photoName = ""

    if 'photoName' in json_dict:
        photoName = json_dict['photoName']

    # print("got photoName: " + photoName)
    photo_path = '/home/ubuntu/s3photobucket/' + photoName
    logTime("got photo")
    #print("checking photo path: " + photo_path)

    global detector
    result = detector.detect(photo_path)

    #print ("result: " + str(result))

    logTime("detection done")

    strres = str(result)


    logTime("writing result")

    finish_request(req, strres)

    end = curtime()
    diff = end - start

    print("threads: " + str(threads) + ", request processed in " + str(diff))


class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        global startTime
        startTime = curtime()
        handleRequest(self)
        return

def init_lib(delay):
    time.sleep(delay)
    print("initializing...")

    src_dir = "/home/ubuntu/mount_efs/ai/nudenet"
    dst_dir = "/home/ubuntu/s3photobucket"
    for jpgfile in glob.iglob(os.path.join(src_dir, "pic.jpg")):
        shutil.copy(jpgfile, dst_dir)

    testres = detector.detect("/home/ubuntu/s3photobucket/pic.jpg")
    print("testres: " + str(testres))



port = int(os.environ['port'])
interface = '0.0.0.0'

if sys.argv[2:]:
    os.chdir(sys.argv[2])

global startTime
startTime = curtime()

global detector
detector = Detector('/home/ubuntu/NudeNet/detector_model')

Thread(target = init_lib, args=(5,)).start()

print('started python classification server on '+ str(port) + " with interpreter: " + platform.python_implementation())

server = ThreadingSimpleServer((interface, port), MyHandler)

try:
    while 1:
        sys.stdout.flush()
        server.handle_request()
except KeyboardInterrupt:
    print('Finished.')