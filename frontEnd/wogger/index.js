/**
 *  filename index.js
 *    wogger - short for winston logger
 *
 *    Reference: https://github.com/winstonjs/winston#winston
 * */

const winston = require('winston');

const wogger = winston.createLogger({
  format: winston.format.simple(),
  transports: [new winston.transports.Console()]
});

module.exports = wogger;
