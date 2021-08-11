const MongoClient = require('mongodb').MongoClient;
require('dotenv').config();

const currentWorkingDirectory = `${__dirname}/`

// expecting to find that the nasaMining/frontEnd/.env file
// has the following secrets and options for the MongoDB
const adminName     = process.env.ADMIN_NAME
const adminPassword = process.env.ADMIN_PASSWORD
const serverMongo   = process.env.SERVER_MONGO
const filenameSSLCA = process.env.FILENAME_SSLCA
const pathToSSLCA   = `${__dirname}/`.replace("routes","secrets")
                      + filenameSSLCA
// options
const connectTimeoutMS = process.env.CONNECT_TIMEOUT_MS.replace(/['"]+/g, '')
const debugLevels = [1,2,3]

// Database Name
const dbName = 'jsonfromnasa'

debugLevelOne   = debugLevels.filter( level => level === 1 )
debugLevelTwo   = debugLevels.filter( level => level === 2 )
debugLevelThree = debugLevels.filter( level => level === 3 )

if ( debugLevelOne[0] != undefined ){
   console.log("\ndebug level 1")
   console.log("serverMongo:", serverMongo)
}

// Inputs must be defined and nonblank
if ( (adminName === undefined) || (adminName === "") ){
  console.log(`Error in ${__filename} . `, "Expecting variable ADMIN_NAME to be defined and not blank in the .env file." )
  process.exit(1)
}
if ( (adminPassword === undefined) || (adminPassword === "") ){
  console.log(`Error in ${__filename} . `, "Expecting variable ADMIN_PASSWORD to be defined in the .env file.")
    process.exit(1)
}
if ( (serverMongo === undefined) || (serverMongo === "") ){
  console.log(`Error in ${__filename} . `, "Expecting variable SERVER_MONGO to be defined in the .env file.")
  process.exit(1)
}
if( (filenameSSLCA === undefined) || (filenameSSLCA === "") ) {

  console.log(`Error in ${__filename} . `, "Expecting variable FILENAME_SSLCA to be defined in the .env file.")
  process.exit(1)
}

/*  See articles discussing securing secrets
  https://movingfast.io/articles/environment-variables-considered-harmful/

  ie, .env not a secure production method of storing the secrets?!
 */

var urlToMongo  = 'mongodb://'
                   + adminName + ':' + adminPassword
                   + '@' + serverMongo + '?'
                   + 'tls=true'
                   + '&tlsCAFile=' + pathToSSLCA
                   + '&connectTimeoutMS=' + connectTimeoutMS
                   + '&replicaSet=' + 'spacetags'

if ( debugLevelTwo[0] != undefined ){
   console.log("\ndebug level 2")
   console.log( "urlToMongo:" + urlToMongo )
}

const collections = ['datasets', 'keywords', 'kw_pair_freq', 'nasa_np_strengths_b', 'related_datasets']


// Ref: https://github.com/mongodb/node-mongodb-native#connect-to-mongodb
const clientMongo = new MongoClient(urlToMongo, {
                   useNewUrlParser: true,
	           useUnifiedTopology: true
               } )

// copy pasta from link referenced above
async function dbConnect( client ) {
  // Use connect method to connect to the server
  await client.connect()
  console.log('\nConnected successfully to MongoDb server')
  const db = client.db(dbName)
  const collection = db.collection('documents')

  // the following code examples can be pasted here...

  return 'done.'
}

dbConnect( clientMongo )
  .then(console.log)
  .catch(console.error)
  .finally(() => clientMongo.close())





// Reference:
//   https://docs.mongodb.com/drivers/node/current/fundamentals/connection/


//* * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
exports.getDatasets = function (req, res) {
    var query = req.query.q;
    var using = req.query.field;
    var field = (using == undefined) ? 'keyword' : using;
    //console.log(field);
    var theQuery = {};
    theQuery[field] = query;
    //console.log(theQuery);
    var theFields = {
        'title': 1,
        'issued': 1,
        'identifier': 1,
        'keyword': 1,
        'description_ngram_np': 1,
        'title_ngram_np': 1,
        'description': 1,
        'landingPage': 1,
        'publisher.name': 1,
        'distribution': 1,
        'source': 1
    };
    if (query == undefined) res.send({'error': 'you must pass in a query, of form q='})
    else {
        db.datasets.find(theQuery, theFields, function (err, docs) {
            if (docs.length == 0) {
                theQuery[field] = query.toUpperCase();
                db.datasets.find(theQuery, theFields, function (err, docs) {
                    res.send(docs);
                })
            }
            else {
                res.send(docs);
            }
        })
    }
};

exports.getEdges = function (req, res) {
    var keywords = JSON.parse(req.query.kws);
    var threshold = (req.query.threshold == undefined) ? -0.5 : req.query.threshold;
    var using = req.query.field;
    var field = (using == undefined) ? 'keyword' : using;

    var query = {'keyword': {"$in": keywords}, 'count': {'$gt': 1}, 'pmi_doc': {'$gte': +threshold}};

    if (field == 'keyword') {
        db.kw_pair_freq.find(query, {'_id': 0}, function (err, docs) {
            var names = [];
            var nameDict = {};
            var counter = 0;
            var edges = [];
            for (var dx in docs) {
                var d = docs[dx];
                if (d['pmi_doc'] < threshold) continue;

                var t1 = d['keyword'][0];
                var t2 = d['keyword'][1];
                if (nameDict[t1] == undefined) {
                    nameDict[t1] = counter;
                    counter += 1;
                    names.push({'name': t1, 'num': d['a']});
                }
                if (nameDict[t2] == undefined) {
                    nameDict[t2] = counter;
                    counter += 1;
                    names.push({'name': t2, 'num': d['b']});
                }
                edges.push({'source': nameDict[t1], 'target': nameDict[t2], 'value': d['pmi_doc'] + 1});
            }
            res.send({'nodes': names, 'links': edges});
        })
    }
    else {
        db.nasa_np_strengths_b.find(query, {'_id': 0}, function (err, docs) {
            var names = [];
            var nameDict = {};
            var counter = 0;
            var edges = [];
            for (var dx in docs) {
                var d = docs[dx];
                //if (d['pmi_doc'] < threshold) continue;

                var t1 = d['keyword'][0];
                var t2 = d['keyword'][1];
                if (nameDict[t1] == undefined) {
                    nameDict[t1] = counter;
                    counter += 1;
                    names.push({'name': t1, 'num': d['a']});
                }
                if (nameDict[t2] == undefined) {
                    nameDict[t2] = counter;
                    counter += 1;
                    names.push({'name': t2, 'num': d['b']});
                }
                edges.push({'source': nameDict[t1], 'target': nameDict[t2], 'value': d['pmi_doc'] + 1});
            }
            res.send({'nodes': names, 'links': edges});
        })
    }
};

exports.getCoOccuringKWs = function (req, res) {
    var query = req.query.q;
    console.log(query);
    var using = req.query.field;
    var field = (using == undefined) ? 'keyword' : using;
    var searches = {
        'keyword': function (curr, result) {
            for (var kx in curr['keyword']) {
                var kw = curr['keyword'][kx];
                if (result[kw] == undefined) {
                    result[kw] = 1;
                }
                else {
                    result[kw] += 1;
                }
            }
        },
        'description_textrank_kw': function (curr, result) {
            for (var kx in curr['description_textrank_kw']) {
                var kw = curr['description_textrank_kw'][kx];
                if (result[kw] == undefined) {
                    result[kw] = 1;
                }
                else {
                    result[kw] += 1;
                }
            }
        },
        'description_bigram_kw': function (curr, result) {
            for (var kx in curr['description_bigram_kw']) {
                var kw = curr['description_bigram_kw'][kx];
                if (result[kw] == undefined) {
                    result[kw] = 1;
                }
                else {
                    result[kw] += 1;
                }
            }
        },
        'description_ngram_np': function (curr, result) {
            for (var kx in curr['description_ngram_np']) {
                var kw = curr['description_ngram_np'][kx];
                if (result[kw] == undefined) {
                    result[kw] = 1;
                }
                else {
                    result[kw] += 1;
                }
            }
        }
    }

    var theQuery = {
        'key': {},
        'cond': {"source": "http://data.nasa.gov/data.json"},
        'reduce': searches[field],
        'initial': {}
    };
    theQuery['cond'][field] = {"$regex": new RegExp('^' + query, 'i')};

    if (query == undefined) res.send({'error': 'you must pass in a query, of form q='})
    else {
        db.datasets.group(theQuery, function (err, docs) {
            if (err | !docs) res.send({'error': 'no documents found'});
            else {
                var values = docs[0];
                var results = [];
                for (var k in values) {
                    results.push({'kw': k, 'count': values[k]});
                }
                results.sort(function (a, b) {
                    return +b.count - a.count;
                });

                res.send(results);
            }
        })
    }
};

exports.getCoOccuringKWsFlat = function (req, res) {
    var query = req.query.q;
    if ( (query === undefined) || (query === "") ){
      res.send({ 'error': 'you must pass in a query, of form q=' })
      console.log( new Error("Expecting query to be defined and not blank") )
    }
    else {
        db.keywords.find(
            {"source": "http://data.nasa.gov/data.json", "keyword": {"$regex": new RegExp('^' + query, 'i')}},
            {"_id": 0},
            function (err, docs) {
                //console.log(docs);
                if (err || !docs) res.send({'error': 'no documents found: ' + docs});
                else {
                    var keywords = [];

                    var k;
                    for (k in docs) {
                        var d = docs[k];
                        for (var kw in d['keywords_full']) {
                            if (keywords[d['keywords_full'][kw]] == undefined) {
                                keywords[d['keywords_full'][kw]] = 1
                            } else {
                                keywords[d['keywords_full'][kw]] += 1
                            }
                        }
                    }

                    var results = [];
                    for (k in keywords) {
                        results.push({'kw': k, 'count': keywords[k]});
                    }

                    results.sort(function (a, b) {
                        return +b.count - a.count;
                    });

                    //console.log(results);

                    res.send(results);
                }
            })
    }
};

exports.getCoOccuringKWsMulti = function (req, res) {
    var keywords = JSON.parse(req.query.kws);
    var using = req.query.field;
    var field = (using == undefined) ? 'keyword' : using;
    var searches = {
        'keyword': function (curr, result) {
            for (var kx in curr['keyword']) {
                var kw = curr['keyword'][kx];
                if (result[kw] == undefined) {
                    result[kw] = 1;
                }
                else {
                    result[kw] += 1;
                }
            }
        },
        'description_textrank_kw': function (curr, result) {
            for (var kx in curr['description_textrank_kw']) {
                var kw = curr['description_textrank_kw'][kx];
                if (result[kw] == undefined) {
                    result[kw] = 1;
                }
                else {
                    result[kw] += 1;
                }
            }
        },
        'description_bigram_kw': function (curr, result) {
            for (var kx in curr['description_bigram_kw']) {
                var kw = curr['description_bigram_kw'][kx];
                if (result[kw] == undefined) {
                    result[kw] = 1;
                }
                else {
                    result[kw] += 1;
                }
            }
        },
        'description_ngram_np': function (curr, result) {
            for (var kx in curr['description_ngram_np']) {
                var kw = curr['description_ngram_np'][kx];
                if (result[kw] == undefined) {
                    result[kw] = 1;
                }
                else {
                    result[kw] += 1;
                }
            }
        }
    };

    var theQuery = {
        'key': {},
        'cond': {"source": "http://data.nasa.gov/data.json"},
        'reduce': searches[field],
        'initial': {}
    };
    theQuery['cond'][field] = {"$in": keywords};

    if (keywords == undefined) res.send({'error': 'you must pass in a query, of form q='});
    else {
        db.datasets.group(theQuery, function (err, docs) {
            var values = docs[0];
            var results = [];
            for (var k in values) {
                results.push({'kw': k, 'count': values[k]});
            }
            results.sort(function (a, b) {
                return +b.count - a.count;
            });

            res.send(results);
        })
    }

};

exports.getRelatedDatasets = function (req, res) {
    var identifier = req.query.identifier;

    db.related_datasets.find({'identifier': identifier}, {'_id': 0}, {"sort": [['sim','desc']]}, function (err, docs) {
        res.send(docs)
    })
};

exports.getDatasetsByIdentifier = function (req, res) {
    var identifiers = JSON.parse(req.query.ids);

    db.datasets.find({'identifier': {'$in': identifiers}}, {"_id": 0, "landingPage": 1, "title": 1}, function (err, docs) {
        res.send(docs);
    });
}
