#!/usr/bin/env python

try:
    # Python 2.x
    from SocketServer import ThreadingMixIn
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from BaseHTTPServer import HTTPServer
except ImportError:
    # Python 3.x
    from socketserver import ThreadingMixIn
    from http.server import SimpleHTTPRequestHandler, HTTPServer


import numpy as np
import os
import sys
import argparse
import glob
import time
from PIL import Image
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import caffe
import json
from binascii import a2b_base64
from threading import Thread

def curtime():
    return int(round(time.time() * 1000))

def logTime(msg):
    global startTime
    diffTime = curtime() - startTime
    print (msg + " done in " + str(diffTime))
    startTime = curtime()


def resize_image(data, sz=(256, 256)):
    """
    Resize image. Please use this resize logic for best results instead of the 
    caffe, since it was used to generate training dataset 
    :param str data:
        The image data
    :param sz tuple:
        The resized image dimensions
    :returns bytearray:
        A byte array with the resized image
    """
    img_data = str(data)
    im = Image.open(StringIO(img_data))
    if im.mode != "RGB":
        im = im.convert('RGB')
    imr = im.resize(sz, resample=Image.BILINEAR)
    fh_im = StringIO()
    imr.save(fh_im, format='JPEG')
    fh_im.seek(0)

    return bytearray(fh_im.read())

def caffe_preprocess_and_compute(pimg, caffe_transformer=None, caffe_net=None,
    output_layers=None):
    """
    Run a Caffe network on an input image after preprocessing it to prepare
    it for Caffe.
    :param PIL.Image pimg:
        PIL image to be input into Caffe.
    :param caffe.Net caffe_net:
        A Caffe network with which to process pimg afrer preprocessing.
    :param list output_layers:
        A list of the names of the layers from caffe_net whose outputs are to
        to be returned.  If this is None, the default outputs for the network
        are returned.
    :return:
        Returns the requested outputs from the Caffe net.
    """

    if caffe_net is not None:

        # Grab the default output names if none were requested specifically.
        if output_layers is None:
            output_layers = caffe_net.outputs

        img_data_rs = resize_image(pimg, sz=(256, 256))
        logTime("resizing")
        image = caffe.io.load_image(StringIO(img_data_rs))

        H, W, _ = image.shape
        _, _, h, w = caffe_net.blobs['data'].data.shape
        h_off = max((H - h) / 2, 0)
        w_off = max((W - w) / 2, 0)
        crop = image[h_off:h_off + h, w_off:w_off + w, :]
        transformed_image = caffe_transformer.preprocess('data', crop)
        transformed_image.shape = (1,) + transformed_image.shape

        input_name = caffe_net.inputs[0]
        all_outputs = caffe_net.forward_all(blobs=output_layers,
                    **{input_name: transformed_image})

        outputs = all_outputs[output_layers[0]][0].astype(float)
        logTime("processing")
        return outputs
    else:
        return []

def classify(argv):
    # pycaffe_dir = os.path.dirname(__file__)

    # parser = argparse.ArgumentParser()
    # # Required arguments: input file.
    # parser.add_argument(
    #     "input_file",
    #     help="Path to the input image file"
    # )

    # model_def = "NsfwSqueezenet/model/deploy.prototxt"
    # pretrained_model = "NsfwSqueezenet/model/nsfw_squeezenet.caffemodel"

    # args = parser.parse_args()
    # print(args.input_file)

    # # Pre-load caffe model.
    # nsfw_net = caffe.Net(model_def, pretrained_model, caffe.TEST)

    # # Load transformer
    # # Note that the parameters are hard-coded for best results
    # caffe_transformer = caffe.io.Transformer({'data': nsfw_net.blobs['data'].data.shape})
    # caffe_transformer.set_transpose('data', (2, 0, 1))  # move image channels to outermost
    # caffe_transformer.set_mean('data', np.array([104, 117, 123]))  # subtract the dataset-mean value in each channel
    # caffe_transformer.set_raw_scale('data', 255)  # rescale from [0, 1] to [0, 255]
    # caffe_transformer.set_channel_swap('data', (2, 1, 0))  # swap channels from RGB to BGR
    # logTime("init")

    # logTime("preparing image")

    # scores = caffe_preprocess_and_compute(args.input_file, caffe_transformer=caffe_transformer, caffe_net=nsfw_net, output_layers=['prob'])
    # result = scores[1][0][0]

    # print ("result: " , result)

    #print(result)

    print("test result")
    sys.stdout.flush()

    return result


if __name__ == '__main__':
    startTime = curtime()
    classify(sys.argv)