const express = require('express')
const app = express()
const bodyParser = require('body-parser'); //npm install request-promise
// const request = require('request'); //npm install request
const request = require("request-promise");
const port = 8000

var servers = [8001, 8002, 8003, 8004, 8005, 8006, 8007, 8008]

app.use(bodyParser.urlencoded({ extended: true, limit: '10mb' }));
app.use(bodyParser.json({ extended: true, limit: '10mb' }));
app.use(express.methodOverride());

var processingRequest = false;
var requestProcessed = false;

app.post('/', (req, res) => {
	//console.log("processing post request in balanser");
	requestProcessed = false;
	handleRequest(req, res);
})

async function handleRequest(req, res){
	while(!requestProcessed){
		startInstance = getRandomInt(9); //servercount + 1 
		for(var i = startInstance; i < servers.length; i++){
			servport = servers[i];
			//console.log("checking server " + servport);
			var statusRes = await checkServerStatus(servport); //takes <20ms
			var available = parseInt(statusRes)
			//console.log("server on port "+ servport + " available: " + available);

			if (available == 1){
				console.log("forwarding request to server " + servport);
				var classifyResult = await sendImageToServer(servport, req.body)
				//console.log("response from server " + servport + ": " + classifyResult);
				requestProcessed = true;
				res.write(classifyResult.toString());
				res.status(200);
				res.end(); 
				return;
			}
		}

		//setTimeout(handleRequest(req, res), 50);
		await sleep(50)
		console.log("restarting server checks");
	}
}

app.use(function(err, req, res, next) {
      console.error("an error occured " + err);
})

async function checkServerStatus(servport){
	return await request.get('http://localhost:' + servport);
}

function sleep(ms){
    return new Promise(resolve=>{
        setTimeout(resolve,ms)
    })
}

async function sendImageToServer(servport, reqbody){
	return await request.post({
		url: 'http://localhost:' + servport,
		body: reqbody,
		json: true
	});
}

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

app.listen(port, (err) => {
	if (err) console.log('something bad happened', err);
	console.log('balanser app started on port ' + port);
})