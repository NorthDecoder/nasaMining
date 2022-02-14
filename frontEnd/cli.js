/**
 * file: cli.js
 *
 *   process command line arguments
 *
 * prerequisite:
 *   expects that winston package is already required
 *
 * */



exports.instruction = function(cla) {

  [ leftValue, rightValue ] = cla.split("=")
  var requestedLogFormat

  switch(leftValue) {
    case '--logformat':
      if ( rightValue === 'simple' ){
         requestedLogFormat  = winston.format.simple()
      }

      if ( rightValue === 'json' ){
          requestedLogFormat  = winston.format.json()

      }
      break

   }//end switch

  return requestedLogFormat
}//end function instruction

