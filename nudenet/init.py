 #!/usr/bin/env python

import os
import json
import glob
import shutil
import requests


src_dir = "/home/ubuntu/mount_efs/ai/nudenet"
dst_dir = "/home/ubuntu/s3photobucket"
for jpgfile in glob.iglob(os.path.join(src_dir, "pic.jpg")):
        shutil.copy(jpgfile, dst_dir)

send_data = {}
send_data['photoName'] = 'pic.jpg'
send_json = json.dumps(send_data)

testres = requests.post('http://127.0.0.1:80', json=send_data)
print("testres: " + str(testres))