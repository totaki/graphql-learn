const express = require('express');

const port = parseInt(process.env.GRAPHIQL_PORT);
const app = express();
app.use(express.static(__dirname));

app.listen(port, function() {
  // noinspection JSAnnotator
  console.log(`Started on http://localhost:${port}/`);
});