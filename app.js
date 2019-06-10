const express = require('express')
const app = express()
const winston = require('winston')
var bodyParser = require('body-parser');
const port = 8000
const cp = require("child_process")

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
		console.log("processing post request");
		//logger.info("image data from request: " + JSON.stringify());

	    const spawn = cp.spawn;
		const pythonProcess = spawn('python',['/home/ubuntu/classify.py']);

		console.log("after spawns");

		//pythonProcess.stdin.write(req.body.image);
		pythonProcess.stdin.write("some test data blablabla");
		pythonProcess.stdin.end();

		console.log("written stdin");

		pythonProcess.stdout.on('data', (data) => {
	    	console.log("python responsed with: " + data)

	    	res.write(data);
	    	res.status(200);
	        res.end();
		});

		pythonProcess.stdout.on("end", data => {
  			console.log("end received, closing connection.");
		});
	})

app.use(function(err, req, res, next) {
      console.error("an error occured " + err)
})


app.listen(port, (err) => {
  if (err) {
    return console.log('something bad happened', err)
  }

  console.log('server started on port ' + port)
})