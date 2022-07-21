#!/usr/bin/env python3

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

          1. A `.env` file provided by devops in the current working directory.
             see ../docs/installation.md#add-environment-variables-file-1
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
          OR

          * an example to be run by unittest

          python3 buildDB.py --inpath ../test/data/list_10_documents.json \\
                             --environment development \\
                             --keyname dataset \\
                             --collection_name list_10 \\
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
from pathlib import Path
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

args                        = parser.parse_args()
relative_path_to_input_json = args.inpath
environment                 = args.environment
keyname                     = args.keyname
collection_name             = args.collection_name
force_delete                = args.force_delete

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

logger.debug( "~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ " )
logger.debug( "Script: " + str( Path(__file__).name ) )

# In order to run the script from a location other than at the
# script location, while running unittest for example, need to
# translate relative into an absolute path.

# relative path in reference to script location in directory structure
# for example this script in     ~/nasaMining/mongoWork/buildDB.py
# relative path for data in                ../data/nasa_keywords.json
# parent_directory    /home/myname/nasaMining/mongoWork
# resolved absolute path to input json string
#                     /home/myname/nasaMining/data/nasa_keywords.json

parent_directory = str( Path(__file__).parent )
absolute_path_object_to_input_json= Path( os.path.join( parent_directory, relative_path_to_input_json ) )
absolute_path_to_input_json_string = str( absolute_path_object_to_input_json.resolve() )

logger.debug( "script parent directory: " + parent_directory )
logger.debug( "absolute_path_to_input_json_string: " + absolute_path_to_input_json_string )



logger.info( "~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ " )
logger.info( "Loading data from " + absolute_path_to_input_json_string )
data = json.load( open( absolute_path_to_input_json_string ) )

logger.debug( "type(data).__name__: "  + type(data).__name__ )

if ( type(data).__name__ == "dict" ):
    logger.debug( data.keys() )
    data_list = data['dataset']
elif(type(data).__name__ == "list"):
    data_list = data







#
if hasattr(db, collection_name ) and (force_delete=='no'):
    logger.warning( "The '"+ collection_name + "' collection already exists in the mongoDB." )
    logger.warning( "Exiting script '" + os.path.basename(__file__) +
                    "' without adding new, or removing old data." )
    logger.warning( "If you truly wish to delete the existing collection, " )
    logger.warning( "add command line argument --force_delete yes" )

    collection_document_count = db[collection_name].count_documents({})

    logger.info( "Collection '" + collection_name + "' in mongoDB contains "
                 + str( collection_document_count ) + " documents."  )
    exit()


if hasattr(db, collection_name ):
    if (force_delete=='yes'):
        logger.info("Since --force_delete is yes, collection '"
                        + collection_name + "'")
        logger.info("will be dropped from mongoDB")

        drop_result = db.drop_collection( collection_name )

        if drop_result is not None:
            logger.info( "Collection '" + collection_name +
                         "' drop_result: " + str( drop_result ) )

        elif drop_result is None:
            logger.info( "Collection '" + collection_name + "' drop_result: " + "failed..." )
            exit()

#

logger.info("- - - - - - - - - - - - - - - - - - - - - - - - ")
logger.info("Writing thousands of documents to the mongoDB collection " + collection_name)
record_count=0 # start at zero records

for d in data_list:
    if (msg_verbocity == "verbose"):
        if record_count < 1:# only print first record
            logger.debug("Debug level 'verbose'; printng the first record for example: ")
            logger.debug("- - - - - - - - - - - - - - - - - - - - - - - - ")
            logger.debug( d )
            logger.debug("- - - - - - - - - - - - - - - - - - - - - - - - ")

    if record_count % 1000 == 0:
        # a dot for every thousand records
        sys.stdout.write(".")
        sys.stdout.flush()

    db[collection_name].insert_one(d)
    record_count += 1

print( "" ) # a newline after all the dots

collection_document_count = db[collection_name].count_documents({})



end_time = time.time()

logger.info("Build copied " + str(record_count) + " documents")
logger.info("in " + str( round( ( end_time - start_time )/60  , 2 ) )  + " minutes.")
logger.info( "Collection '" + collection_name + "' now contains " + str( collection_document_count ) + " documents")

