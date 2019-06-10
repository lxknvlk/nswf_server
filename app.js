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
		//logger.info("image data from request: " + JSON.stringify());

	    const spawn = cp.spawn;
		const pythonProcess = spawn('python',['/home/ubuntu/classify.py']);

		pythonProcess.stdin.write(req.body.image, function(err){
		//pythonProcess.stdin.write("some test data blablabla", function(err){
			pythonProcess.stdin.end();
		});

		pythonProcess.stdout.on('data', (data) => {
		    	console.log("message from python:" + data)

		        // res.write(data, function(err) { 
		        // 	res.status(200);
		        // 	res.end(); 
		        // });
			});


		pythonProcess.stdout.on("end", (data) => {
  			console.log("end received data: " + data);
			res.status(200);
		    res.end(); 
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