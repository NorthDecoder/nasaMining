/**
 *  filename index.js
 *    wogger - short for winston logger
 *
 *    Reference: https://github.com/winstonjs/winston#winston
 * */

const winston = require('winston');
const commandLineArgs = process.argv.slice(2);

var requestedLogFormat = ''

commandLineArgs.forEach( argument => instruction(argument) )

function instruction(cla) {

  lvrvArray = cla.split("=") // right and left val

  switch(lvrvArray[0]) {
    case '--logformat':
      if ( lvrvArray[1]=== 'simple' ){
         requestedLogFormat  = winston.format.simple()
      }

      if ( lvrvArray[1]=== 'json' ){
         requestedLogFormat  = winston.format.json()
      }
      break;
  }//end switch
}
/**
 * expecting  commandLineArgs to receive an array as follows
 *  [ '--loglevel=info', '--debuglevel=1', '--runlevel=production' ]
 *  OR
 *  [ '--help']
 *  OR
 *  ['']
 *
 *  Usage:
 *
 *  node server.js --loglevel=info --logformat=json --debuglevel=1 --runlevel=production
 * */

const wogger = winston.createLogger({
  format: requestedLogFormat,
  transports: [new winston.transports.Console()]
});

module.exports = wogger;
