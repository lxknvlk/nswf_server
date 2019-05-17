# nswf_server

Install following the install insrutcions.txt

Use like this:

(echo -n '{"image": "'; base64 Downloads/porn.jpg; echo '"}') |
curl -H "Content-Type: application/json" -d @-  0.0.0.0:8000

Send base64 encoded image in a json field "image"
