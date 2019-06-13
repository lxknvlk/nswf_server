const express = require('express')
const app = express()
const bodyParser = require('body-parser'); //npm install request-promise
// const request = require('request'); //npm install request
const request = require("request-promise");
const port = 8000

var servers = [8001, 8002, 8003, 8004]

app.use(bodyParser.urlencoded({ extended: true, limit: '10mb' }));
app.use(bodyParser.json({ extended: true, limit: '10mb' }));

var processingRequest = false;
var requestProcessed = false;

app.post('/', (req, res) => {
	console.log("processing post request in balanser");
	requestProcessed = false;
	processingRequest = false;
	handleRequest(req, res);
	console.log("post request processed!");
})

async function handleRequest(res, req){
	while (!requestProcessed){
		if (!processingRequest){
			processingRequest = true;
			console.log("processing request in while/if");
			for(var i = 0; i < servers.length; i++){
				servport = servers[i];
				console.log("checking server " + servport);
				var statusRes = await checkServerStatus(servport);
				var available = parseInt(statusRes)
				console.log("server on port "+ servport + " available: " + available);
				
				if (available == 1){
					console.log("forwarding request to server " + servport);
					var classifyResult = await sendImageToServer(servport, req.body)
					console.log("response from server " + servport + " :" + classifyResult);
					requestProcessed = true;
					processingRequest = false;
					res.write(response.toString());
					res.status(200);
					res.end(); 
					return;
				}
			}
		}	

		console.log("restarting server checks");
		setTimeout(handleRequest(res, req), 3000);
	}
}

app.use(function(err, req, res, next) {
      console.error("an error occured " + err);
})

async function checkServerStatus(servport){
	return await request.get('http://localhost:' + servport);
}

async function sendImageToServer(servport, reqbody){
	return await request.post({
		url: 'http://localhost:' + servport,
		body: reqbody,
		json: true
	});
}

function sleep(ms){
    return new Promise(resolve=>{
        setTimeout(resolve,ms)
    })
}

app.listen(port, (err) => {
	if (err) console.log('something bad happened', err);
	console.log('balanser app started on port ' + port);
})