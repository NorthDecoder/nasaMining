import authenticate_to_mongo # local module
import json
import logging
import sys

msg_verbocity = ''

if len(sys.argv) > 1:
    environment  = sys.argv[1]
else:
    # default to
    environment  = "production"


if (environment == 'development' ):
    logging.basicConfig( level=logging.DEBUG )
    msg_verbocity = "verbose"

if (environment == 'production' ):
    logging.basicConfig( level=logging.INFO )
    msg_verbocity = "quiet"

logger = logging.getLogger(__name__)

db = authenticate_to_mongo.db_json_from_agency( msg_verbocity )


if __name__ == '__main__':
    path_to_data = "../data/nasa_keywords.json"
    f = open( path_to_data)
    s = f.read()

    print( "type(s):" )
    print( type(s) )

    print ( "type(f):" )
    print ( type(f) )
    f.close()

    data_list = json.loads( s )
    print( "type(data_list):" )
    print( type(data_list) )
    print( "len(data_list): " + str( len(data_list) ) )

    # where each element of data_list is json record from
    # the dataset
#    data = json.load(open('data/nasa_kw.json'))['dataset'] # original line

    logger.info("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
    logger.info( "Loaded %s records from %s", len(data_list), path_to_data )

    logger.info( "Updating the records in the database" )
    logger.info( "A dot for every thousand records" )
    for i, d in enumerate(data_list):
        if i % 1000 == 0:
            # a dot for every thousand records
            sys.stdout.write(".")
            sys.stdout.flush()
        print("\n")
        #print( "i:", i, d['identifier'] )
        print( "i:", i, d )
        if i > 5:
            exit() # debug only; prematurely exits script...

        def a_way_of_commenting_out_this_code():

            # description_ngram_np is the new name value for description_bigram_kw ?
            # this was the original code
            db.datasets.update({'identifier': d['identifier']}, {'$set': {
                'description_bigram_kw': d['description_bigram_kw'],
                'description_textrank_kw': d['description_textrank_kw']
            }})


        # trying to get above database access working somehow ...
        db.datasets.update({'identifier': d['identifier']},
            {'$set': {'description_ngram_np': d['description_ngram_np']}
            })

