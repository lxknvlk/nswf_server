#!/usr/bin/env python

import glob
import sys
import numpy as np
from PIL import Image
from base64 import b64decode, b64encode
import json
import urllib2
from multiprocessing import Pool
from multiprocessing import Process
from threading import Thread
import time

def makeRequest(num):
	data = {'image': encoded_data}
	#data = {'image': 'none'}

	req = urllib2.Request('http://0.0.0.0:8000')
	req.add_header('Content-Type', 'application/json')

	response = urllib2.urlopen(req, json.dumps(data))

	end = int(round(time.time() * 1000))

	diff = end - start

	print num , ' request made, diff from start', diff
	print '\n'

if __name__ == '__main__':
	image_handle = open('image/image.jpg', 'rb')
	raw_image_data = image_handle.read()
	encoded_data = b64encode(raw_image_data)

	start = int(round(time.time() * 1000))

	i = int(sys.argv[1])

	print 'running loadtest with requests: ' , i

	for x in range(i):
		Thread(target = makeRequest(i)).start()

	print 'finished script'
