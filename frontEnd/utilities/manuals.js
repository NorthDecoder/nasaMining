/**
 * file: manuals.js
 *
 *   process command line arguments
 *   to supply help file documents
 *
 *
 * */

const wogger = require( "./wogger.js" )


exports.instruction = function(cla) {
  wogger.info( "++++++++++++++++++++++++" )
  wogger.info( "In in file manual.js in function instruction")
  wogger.info( "cla: ", cla )

  var [ leftValue, rightValue ] = cla.split("=")

  switch(leftValue) {
    case '--man':
      if ( rightValue === 'help' ){
          wogger.info("TODO: load help file here")
      }

      process.exit(1)
      break

   }//end switch

}//end function instruction

