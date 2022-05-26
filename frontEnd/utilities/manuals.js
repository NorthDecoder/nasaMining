/**
 * file: manuals.js
 *
 *   process command line arguments
 *   to supply help file documents
 *
 *
 * */

const wogger = require( "./wogger.js" )

const fs = require('fs');
const process = require('process')

const current_dir = process.cwd()

exports.instruction = function(cla) {
  // where cla is command line argument
  wogger.debug( "++++++++++++++++++++++++" )
  wogger.debug( "In file manual.js in function instruction")

  var [ leftValue, rightValue ] = cla.split("=")

  switch(leftValue) {
    case '--man':
      if ( rightValue === 'help' ){
          readHelpFile(current_dir)
      }
      break

    case '--help':
      readHelpFile(current_dir)
      break

    case 'help':
      readHelpFile(current_dir)
      break

  }//end switch

}//end function instruction



function readHelpFile(current_dir) {

          manPagePath = current_dir + '/manpages/help.md'

          wogger.debug('manPagePath:' + manPagePath )

          const data = fs.readFileSync( manPagePath,
            {encoding:'utf8', flag:'r'} );

          console.log(data);

          process.kill(process.pid, 'SIGTERM')

}

