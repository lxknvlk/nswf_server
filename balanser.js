const express = require('express')
const app = express()

var bodyParser = require('body-parser');
var request = require('request'); //npm install request
const port = 8000

var servers = [8001, 8002, 8003, 8004]

//const winston = require('winston')
// const logger = winston.createLogger({
//   level: 'info',
//   format: winston.format.json(),
//   defaultMeta: { service: 'user-service' },
//   transports: [
//     new winston.transports.File({ filename: 'combined.log' })
//   ]
// });

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
			console.log("forwarding request to server");
			//process request
			sendImageToServer(servport, function(response){
				console.log("response in balanser from sendImageToServer: " + response);
					res.status(200);
					res.end(); 
			})
		} else {
			console.log("server busy, skipping");
			res.status(200);
			res.end(); 
		}
	});



	//res.write(data);
    //res.status(200);
	//res.end(); 
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

function sendImageToServer(servport, callback){
	request.post('http://localhost:' + servport, function (err, res, body) {
	        if (err) console.log("error from processing image: " +  err);
	        callback(body);
	    }
	);
}

app.listen(port, (err) => {
	if (err) return console.log('something bad happened', err);
	console.log('balanser app started on port ' + port);
})