##
# Reference:
#  https://pymongo.readthedocs.io/en/stable/examples/tls.html#tls-ssl-and-pymongo
#  https://docs.mongodb.com/drivers/pymongo/

# Inputs:
#  a `../data/nasa.json` file is expected to be available
#  a `.env` file provided by devops in the current working directory
#  a `./secrets/FILENAME_SSLCA` file contains the MongoDb secure socket
#     layer certificate of authentication

# Result:
#  The nasa.json data is loaded into the mongodb as a database named
#  `jsonfromnasa`

# Usage:
#  python3 buildDB.py

debug_level=1  # 1 is verbose, 0 is quiet

# make no user changes below here

from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv
load_dotenv()

path_to_data = "../data/nasa.json"
print("Loading data from", path_to_data , " ." )
data = json.load( open( path_to_data ) ) # returns a dictionary
if (debug_level == 1):
    print( "  type(data)", type(data) )
    print( "  data.keys():", data.keys() )

# for MongoDB
admin_name     = os.getenv('ADMIN_NAME')
admin_password = os.getenv('ADMIN_PASSWORD')
server_mongo   = os.getenv('SERVER_MONGO')   # server urls
sslca          = os.getenv('FILENAME_SSLCA') # certificate
full_path_sslca= "secrets/"+sslca

print("\nEnvironment variables loaded.")
if (debug_level == 1):
   print( "  admin_name: ",     admin_name )
   print( "  admin_password: ", admin_password )
   print( "  server_mongo: ",   server_mongo )
   print( "  sslca: ",          sslca )
   print( "  full_path_sslca: ",full_path_sslca )



client = MongoClient(server_mongo,
                              tls=True,
                              tlsCAFile=full_path_sslca)

if (debug_level == 1):
    try:
        print("\n  client.server_info():")
        print( client.server_info() )
    except Exception:
        print( "Unable to connect to the server." )


# command insert requires authentication
# note the `admin` database may be different in your install
client.admin.authenticate( admin_name, admin_password )
db=client.jsonfromnasa

print("\n- - - - - - - - - - - - - - - - - - - - - - - - ")
print("Building the database ...")
limit=0 # start at zero records

for d in data['dataset']:
    if (debug_level == 1):
        if limit < 1:# only print first record
            print(d)
            limit += 1

    db.datasets.insert_one(d)
