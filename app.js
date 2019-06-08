const express = require('express')
const app = express()
const port = 8000

app.post('/', (request, response) => {
  response.send('POST!')
})

app.listen(port, (err) => {
  if (err) {
    return console.log('something bad happened', err)
  }

  console.log('server started on port ' + port)
})