const express = require('express')
const app = express()

var bodyParser = require('body-parser');
var request = require('request'); //npm install request
const port = 8000

var servers = [8001, 8002, 8003, 8004]

app.use(bodyParser.urlencoded({ extended: true, limit: '10mb' }));
app.use(bodyParser.json({ extended: true, limit: '10mb' }));

app.post('/', (req, res) => {
	console.log("processing post request in balanser");
	//req.body.image or just forward req

	// var processed = false;
	// while (!processed){
	// 	for (servers){
	// 		if (server.idle) call function and return result and set processed = true
	// 	}
	// 	pause 150
	// }
	requestProcessed = false;
	servport = 8001;

	checkServerStatus(servport, function(response){
		console.log("server on port "+ servport + " available: " + response);
		available = parseInt(response)

		if (available == 1){
			console.log("forwarding request to server " + servport);
			sendImageToServer(servport, req.body, function(response){
				console.log("response from server " + servport + " :" + response);
				res.write(response.toString());
				res.status(200);
				res.end(); 
			})
		} else {
			res.status(200);
			res.end(); 
		}
	});
})

app.use(function(err, req, res, next) {
      console.error("an error occured " + err);
})

function checkServerStatus(servport, callback){
	request.get('http://localhost:' + servport, function(err, res, body){
		if(err) console.log("error from python: " + err);
		callback(body);
	});
}

function sendImageToServer(servport, reqbody, callback){
	request.post({
		url: 'http://localhost:' + servport,
		body: reqbody,
		json: true
	}, function(error, response, body){
        if (error) console.log("error from processing image: " +  error);
        //if (body) console.log("body from python: " + body);
        callback(body);
	});
}


app.listen(port, (err) => {
	if (err) console.log('something bad happened', err);
	console.log('balanser app started on port ' + port);
})