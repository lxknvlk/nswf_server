#!/usr/bin/env python

from nudenet import NudeDetector
detector = NudeDetector('/home/ubuntu/NudeNet/detector_model')
result = detector.detect('/home/ubuntu/image/image_small.jpg')

print("=============RESULT BELOW============\n")
print(result)