class Helper:
    def __init__(self):
        ''' Help for buildDB.py '''

    def buildDB_augmented_help():
        """
         # buildDB augmented help

         This script buildDB.py generically loads a
         data.json format file from a local directory
         then builds a collection into a mongoDB
         database.

         The format of the json input file is expected
         to be like:
                    {[{},{},{}]}
         OR
                    {"dataset":{[{},{},{}]}}

         In the script the key name defaults to
         `dataset`, and the mongoDB collection
         name defaults to `dataset`, which is the
         standard for the NASA data, however the
         defaults can be overridden with a
         command line argument. This means that
         any file in the expected json format can
         be loaded into a mongoDB collection.

         ## Inputs:

          1. A `.env` file provided by devops in the current working directory
          2. A `./secrets/FILENAME_SSLCA` file contains the MongoDb secure socket
             layer certificate of authentication
          3. Command line
             --inpath  "local path to the data"
             --augmented_help
             --environment "development OR production"
             --keyname "the key name for the input json list defaults to dataset"
             --collection_name "the collection name to be added to the mongoDB,
                                defaults to dataset"
             --force_delete "allows replacing an entire collection in mongoDB,
                             yes OR no, defaults to no"

         ## Result:

          1. The data is loaded in the mongodb into a collection named
             'dataset'.  The script will exit if an existing collection
             named dataset already exists and force_delete=no.
             If force_delete=yes then the collection will be dropped and
             rewritten.

          2. Logging is to the terminal

         ## Usage:

          cd mongoWork # for all examples

          python3 buildDB.py -help   # argparse help

          OR
          python3 buildDB.py --augmented_help   # Verbose help

          OR
          * with verbose debugging messages

          python3 buildDB.py --inpath ../data/nasa_keywords.json \\
                             --environment development
          OR
          * information and warning messages only

          python3 buildDB.py --inpath ../data/nasa_keywords.json \\
                             --environment production

          OR
          * defaults to production and all default inputs
            with a message_verbocity of `quiet`

          python3 buildDB.py

          OR
          * fully customized with defaults overriden
            erases and rewrites the keywords collection in mongoDB

          python3 buildDB.py --inpath ../data/my_custom_phrases.json \\
                             --environment development \\
                             --keyname yet_another_dataset \\
                             --collection_name keywords \\
                             --force_delete yes

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

parser = argparse.ArgumentParser(description='Build a mongoDB from a local data.json file')
parser.add_argument('-i', "--inpath", type=str, default='../data/nasa_keywords.json', help='path to a data.json format file, defaults to ../data/nasa_keywords.json')
parser.add_argument('-e', "--environment", type=str, default='production', help='choose development OR production, defaults to production')
parser.add_argument('-k', "--keyname", type=str, default='dataset', help='define the keyname of the input data, defaults to dataset')
parser.add_argument('-c', "--collection_name", type=str, default='dataset', help='collection name to be created in mongoDB, defaults to dataset')
parser.add_argument('-f', "--force_delete", type=str, default='no', help='force delete allows replacing an entire collection in mongoDB, yes OR no, defaults to no')
parser.add_argument("--augmented_help", action='store_true', default="", help="Verbose help")

args               = parser.parse_args()
path_to_input_json = args.inpath
environment        = args.environment
keyname            = args.keyname
collection_name    = args.collection_name
force_delete       = args.force_delete

if args.augmented_help:
    help( Helper.buildDB_augmented_help )
    exit()

start_time = time.time()

#

msg_verbocity = ''


if (environment == 'production' ):
    logging.basicConfig( level=logging.INFO )
    msg_verbocity = "quiet"

elif (environment == 'development' ):
    logging.basicConfig( level=logging.DEBUG )
    msg_verbocity = "verbose"

else:
    # defaults to same as productions
    # in case of an input spelling error for example
    logging.basicConfig( level=logging.INFO )
    msg_verbocity = "quiet"
    logger.info( "No valid environment specified. Defaulting to production level log messages" )

#

logger = logging.getLogger(__name__)

db = authenticate_to_mongo.db_jsonfromnasa( msg_verbocity )



logger.info( "~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ " )
logger.info( "Loading data from " + path_to_input_json )
data = json.load( open( path_to_input_json ) )

logger.debug( "type(data).__name__: "  + type(data).__name__ )

if ( type(data).__name__ == "dict" ):
    logger.debug( data.keys() )
    data_list = data['dataset']
elif(type(data).__name__ == "list"):
    data_list = data






#
if hasattr(db, 'dataset') and (force_delete=='no'):
    logger.warning( "The 'dataset' collection already exists in the mongoDB." )
    logger.warning( "Exiting script '" + os.path.basename(__file__) +
                    "' without adding new, or removing old data." )
    logger.warning( "If you truly wish to delete the existing collection, " )
    logger.warning( "add command line argument --force_delete yes" )

    exit()

#

logger.info("- - - - - - - - - - - - - - - - - - - - - - - - ")
logger.info("Building the database ...")
record_count=0 # start at zero records

logger.info( "Thousands of records " )

#for d in data['dataset']:
for d in data_list:
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

end_time = time.time()
print("in ", round( ( end_time - start_time )/60  , 2 )   , " minutes.")

