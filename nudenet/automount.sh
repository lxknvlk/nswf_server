#!/bin/env dash
echo 'starting mount script'
sudo /usr/local/bin/s3fs s3antichat /home/ubuntu/s3photobucket -o allow_other -o uid=1000 -o mp_umask=002 -o multireq_max=5 -o use_path_request_style -o url=https://s3.us-east-1.amazonaws.com
echo 'mount script done'