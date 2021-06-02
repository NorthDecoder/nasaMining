var express = require('express'),
	docs = require('./routes/docs'),/*,
	bodyParser = require('body-parser');*/
	setImmediate = global.setImmediate;

const process = require('process');

const current_dir = process.cwd()

var app = express();
app.get('/', function (req, res) {
	//res.send('Hello world')
	res.sendFile( current_dir +'/public/index.html' );
});
app.get('/getDatasets', docs.getDatasets);
app.get('/getCoOccuringKWs', docs.getCoOccuringKWs);
app.get('/getCoOccuringKWsFlat', docs.getCoOccuringKWsFlat);
app.get('/getCoOccuringKWsMulti', docs.getCoOccuringKWsMulti);
app.get('/getEdges', docs.getEdges);
app.get('/getRelatedDatasets', docs.getRelatedDatasets);
app.get('/getDatasetsByIdentifier', docs.getDatasetsByIdentifier);
app.get(/^(.+)$/, function(req,res){
	res.sendFile( current_dir + '/public/' + req.params[0]);
});

var server = app.listen(3000, function () {

  var host = server.address().address;
  var port = server.address().port;

  console.log('Spacetag app listening at http://%s:%s', host, port);
  console.log(" ")
});
