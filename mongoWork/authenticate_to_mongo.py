from dotenv import load_dotenv
load_dotenv()
import logging
import os
from pathlib import Path
from pymongo import MongoClient

logger = logging.getLogger(__name__)


def db_json_from_agency( verbocity = 'quiet' ):
    '''function name: db_json_from_agency

    To keep other scripts DRY, include this function to access
    the mongoDB with an authenticated client.

        Inputs:
                1) mongoDB credentials from the .env file available
                   to python module getenv.
                2) ssl certificate from the secrets directory.
                3) verbocity as an argument to this function,
                   where 'verbose' yields more messages and
                   'quiet' fewer.

        Output: returns the authenticated client and database name

        Usage:
            import authenticate_to_mongo
            db = authenticate_to_mongo.db_json_from_agency()

            db.datasets. { some mongo command here }
    '''

    admin_name     = os.getenv('ADMIN_NAME')
    admin_password = os.getenv('ADMIN_PASSWORD')
    server_mongo   = os.getenv('SERVER_MONGO')   # server urls
    sslca          = os.getenv('FILENAME_SSLCA') # certificate
    relative_path_sslca= "secrets/"+sslca


    parent_directory = str( Path(__file__).parent )
    absolute_path_object_to_sslca = Path( os.path.join( parent_directory, relative_path_sslca ) )
    absolute_path_to_sslca_string = str( absolute_path_object_to_sslca.resolve() )




    logger.info("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
    logger.info("Environment variables loaded.")

    if ( verbocity == "verbose" ):
        logger.debug( "  admin_name: %s",     admin_name )
        logger.debug( "  admin_password: %s", admin_password )
        logger.debug( "  server_mongo: %s",   server_mongo )
        logger.debug( "  sslca: %s",          sslca )
        #logger.debug( "  full_path_sslca: %s",full_path_sslca )
        logger.debug( "  :absolute_path_to_sslca_string %s", absolute_path_to_sslca_string )


    client = MongoClient( server_mongo,
                                  tls=True,
                                  tlsCAFile=absolute_path_to_sslca_string )
    if ( verbocity == "verbose"):
        logger.debug(  "  client: %s", client )

    client.admin.authenticate( admin_name, admin_password )

    return client.json_from_agency

