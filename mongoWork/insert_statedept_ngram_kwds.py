import authenticate_to_mongo #local module
from pymongo import MongoClient
import json

client = MongoClient('proximus.modulusmongo.net:27017')
client.tepO9seb.authenticate('nasahack', 'hacking4nasa')
db = client.tepO9seb

if __name__ == '__main__':
    data = json.load(open('data/statedept_ngram_np.json'))

    db.datasets.insert(data)