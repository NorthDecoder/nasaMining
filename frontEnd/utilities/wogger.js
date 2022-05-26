/**
 *  filename index.js
 *    wogger - short for winston logger
 *
 *    Reference: https://github.com/winstonjs/winston#winston
 * */

/**
 * expecting  commandLineArgs to receive an array something
 * like:
 *  [ '--loglevel=info',
 *    '--logformat=json'
 *    '--debuglevel=1',
 *    '--runlevel=production' ]
 *  OR
 *  [ '--help']
 *  OR
 *  ['help']
 *
 *  Usage:
 *
 *  node server.js --loglevel=info --logformat=json --debuglevel=1 --runlevel=production
 * */

const winston = require('winston');
const commandLineArgs = process.argv.slice(2);

var requestedLogFormat = ''
var requestedLogLevel  = 'info' // default level

commandLineArgs.forEach( argument => instruction(argument) )

//
function instruction(cla) {

  var [ leftValue, rightValue ] = cla.split("=")

  switch(leftValue) {
    case '--logformat':
      if ( rightValue === 'simple' ){
         requestedLogFormat  = winston.format.simple()
      }

      if ( rightValue === 'json' ){
         requestedLogFormat  = winston.format.json()
      }
      break;

    case '--loglevel':
      requestedLogLevel = rightValue
      break;
  }//end switch
}

//
const wogger = winston.createLogger({
  level: requestedLogLevel,
  format: requestedLogFormat,
  transports: [new winston.transports.Console()]
});

module.exports = wogger;
