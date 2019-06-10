const express = require('express')
const app = express()
const port = 8000
const cp = require("child_process")

//app.post('/', (request, response) => {
//  response.send('POST!')
//})

app.post('/', (req, res) => {
	console.log("got post request, processing");

	var image_data = "some image data"

    const spawn = cp.spawn;
	const pythonProcess = spawn('python',['/home/ubuntu/classify.py', image_data]);
	console.log("after spawns");

	pythonProcess.stdout.on('data', (data) => {
    	console.log("got some data in listener: " + data)

    	res.write(data);
    	res.status(200);
        res.end();
	});
})


app.listen(port, (err) => {
  if (err) {
    return console.log('something bad happened', err)
  }

  console.log('server started on port ' + port)
})