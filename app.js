const express = require('express')
const app = express()
const port = 8000

//app.post('/', (request, response) => {
//  response.send('POST!')
//})

app.post('/', (req, res) => {
	console.log("got post request, processing");

    const { spawn } = require('child_process');
    const pyProg = spawn('python', ['./classify.py', "image data goes here!!!"]);

    pyProg.stdout.on('data', function(data) {
        console.log(data.toString());
        res.write(data);
        res.end('end');
    });
})


app.listen(port, (err) => {
  if (err) {
    return console.log('something bad happened', err)
  }

  console.log('server started on port ' + port)
})