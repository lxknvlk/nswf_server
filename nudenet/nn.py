#!/usr/bin/env python

import keras
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color

import cv2
import numpy as np
import tensorflow as tf

class Detector():
	detection_model = None
	classes = [
		'BELLY',
		'BUTTOCKS',
		'F_BREAST',
		'F_GENITALIA',
		'M_GENETALIA',
		'M_BREAST',
	]

	def __init__(self, model_path):
		Detector.detection_model = models.load_model(model_path, backbone_name='resnet101')

	def detect(self, img_path, min_prob=0.6):
		image = read_image_bgr(img_path)
		image = preprocess_image(image)
		image, scale = resize_image(image)

		graph = tf.get_default_graph()
		with graph.as_default():
			boxes, scores, labels = Detector.detection_model.predict_on_batch(np.expand_dims(image, axis=0))

		boxes /= scale
		processed_boxes = []
		for box, score, label in zip(boxes[0], scores[0], labels[0]):
			if score < min_prob:
				continue
			box = box.astype(int).tolist()
			label = Detector.classes[label]
			processed_boxes.append({'box': box, 'score': score, 'label': label})

		return processed_boxes


#from nudenet import NudeDetector
#detector = NudeDetector('/home/ubuntu/NudeNet/detector_model')
detector = Detector('/home/ubuntu/NudeNet/detector_model')
result = detector.detect('/home/ubuntu/image/image_small.jpg')

print("GPU Available: ", tf.test.is_gpu_available())
print("Built with cuda: ", tf.test.is_built_with_cuda())
sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
print("=============RESULT BELOW============\n")
print(result)