class Helper:
    def __init__(self):
        ''' Help for buildDB.py '''

    def buildDB_help():
        """
         Inputs:
          1. A `../data/nasa.json` file is expected to be available
          2. A `.env` file provided by devops in the current working directory
          3. A `./secrets/FILENAME_SSLCA` file contains the MongoDb secure socket
             layer certificate of authentication

         Result:
          1. The nasa.json data is loaded into the mongodb as a database named
             `jsonfromnasa` into a collection named 'dataset'.  The script will
             exit if an existing dataset already exists; it will not be
             overwritten.
          2. Logging is to the terminal

         Usage:
          python3 buildDB.py help   # returns this message
          OR
          python3 buildDB.py development # verbose debugging messages
          OR
          python3 buildDB.py production  # information and warning messages only
          OR
          python3 buildDB.py        # defaults to production
                                      with a message_verbocity of `quiet`



         Reference:
          https://pymongo.readthedocs.io/en/stable/examples/tls.html#tls-ssl-and-pymongo
          https://docs.mongodb.com/drivers/pymongo/
        """

#

import argparse
import authenticate_to_mongo #local module
from pymongo import MongoClient
import json
import logging
import os
import sys
from dotenv import load_dotenv
load_dotenv()
import time

#

msg_verbocity = ''

if len(sys.argv) > 1:
    environment  = sys.argv[1]
else:
    # default to
    environment  = "production"


if (environment == 'production' ):
    logging.basicConfig( level=logging.INFO )
    msg_verbocity = "quiet"

elif (environment == 'development' ):
    logging.basicConfig( level=logging.DEBUG )
    msg_verbocity = "verbose"

elif ( environment == 'help' ):
    help( Helper.buildDB_help )
    exit()

else:
    # defaults to same as productions
    logging.basicConfig( level=logging.INFO )
    msg_verbocity = "quiet"

#

logger = logging.getLogger(__name__)

db = authenticate_to_mongo.db_jsonfromnasa( msg_verbocity )



path_to_data = "../data/nasa.json"
logger.info( "~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ " )
logger.info( "Loading data from" + path_to_data )
data = json.load( open( path_to_data ) ) # returns a dictionary

logger.debug( "type(data):"  + type(data).__name__ )
logger.debug( data.keys() )
'''
if (msg_verbocity == "verbose"):
    try:
        print("\n  client.server_info():")
        print( client.server_info() )
    except Exception:
        print( "Unable to connect to the server." )
'''


#
if hasattr(db, 'dataset'):
    logger.warning( "The 'dataset' collection already exists." )
    logger.warning( "Exiting script '" + os.path.basename(__file__) +
                    "' without adding new, or removing old data." )
    exit()

#

logger.info("- - - - - - - - - - - - - - - - - - - - - - - - ")
logger.info("Building the database ...")
record_count=0 # start at zero records

logger.info( "Thousands of records " )

for d in data['dataset']:
    if (msg_verbocity == "verbose"):
        if record_count < 1:# only print first record
            logger.debug("Debug level 'verbose'; printng the first record for example: ")
            logger.debug("- - - - - - - - - - - - - - - - - - - - - - - - ")
            logger.debug(d,"\n")
            logger.debug("- - - - - - - - - - - - - - - - - - - - - - - - ")

    if record_count % 1000 == 0:
        # a dot for every thousand records
        sys.stdout.write(".")
        sys.stdout.flush()

    db.datasets.insert_one(d)
    record_count += 1

print("\nBuild completed with", record_count, "records.")

